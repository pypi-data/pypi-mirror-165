from collections import defaultdict
import logging
from typing import Optional

import pandas as pd

from truera.analytics.loader.metarepo_client import MetarepoClient
from truera.client.private.communicator.query_service_communicator import \
    GrpcQueryServiceCommunicator
from truera.client.public.auth_details import AuthDetails
import truera.protobuf.public.aiq.intelligence_service_pb2 as i_s_proto
import truera.protobuf.public.common.data_locator_pb2 as dl_pb
import truera.protobuf.public.common_pb2 as common_pb
from truera.protobuf.public.qoi_pb2 import QuantityOfInterest
from truera.protobuf.queryservice import query_service_pb2 as qs_pb
from truera.utils.truera_status import TruEraInternalError

value_extractors = {
    "BYTE": lambda x: x.byte_value,
    "INT16": lambda x: x.short_value,
    "INT32": lambda x: x.int_value,
    "INT64": lambda x: x.long_value,
    "FLOAT": lambda x: x.float_value,
    "DOUBLE": lambda x: x.double_value,
    "STRING": lambda x: x.string_value,
    "BOOLEAN": lambda x: x.bool_value,
    "TIMESTAMP": lambda x: x.timestamp_value.seconds
}

dtype_conversion_dict = {
    "BYTE": "Int8",
    "INT16": "Int16",
    "INT32": "Int32",
    "INT64": "Int64",
    "FLOAT": "float32",
    "DOUBLE": "float64",
    "STRING": "string",
    "BOOLEAN": "bool",
    "TIMESTAMP":
        "int64"  # Note: treated as int64 (only 'seconds' filed is used)
}


class QueryServiceClient(object):

    def __init__(
        self,
        connection_string: str,
        metarepo_client: MetarepoClient,
        auth_details: AuthDetails = None,
        logger=None
    ):
        self.communicator = GrpcQueryServiceCommunicator(
            connection_string, auth_details, logger
        )
        self.metarepo_client = metarepo_client
        self.logger = logger or logging.getLogger(__name__)
        self.value_extractors_dict = value_extractors
        self.dtypes_dict = dtype_conversion_dict

    def echo(self, request_id: str, message: str) -> qs_pb.EchoResponse:
        self.logger.info(
            f"QueryServiceClient::echo request_id={request_id}, message={message}"
        )
        request = qs_pb.EchoRequest(request_id=request_id, message=message)
        response = self.communicator.echo(request)
        return response

    def getPreprocessedData(
        self, data_collection_id: str, input_spec: i_s_proto.ModelInputSpec,
        request_id: str
    ) -> Optional[pd.DataFrame]:
        return self._read_static_data(
            data_collection_id=data_collection_id,
            split_name=input_spec.split_id,
            expected_data_kind="DATA_KIND_PRE",
            request_id=request_id
        )

    def getProcessedOrPreprocessedData(
        self, data_collection_id: str, input_spec: i_s_proto.ModelInputSpec,
        request_id: str
    ) -> Optional[pd.DataFrame]:
        processed_data = self._read_static_data(
            data_collection_id=data_collection_id,
            split_name=input_spec.split_id,
            expected_data_kind="DATA_KIND_POST",
            request_id=request_id
        )

        return processed_data if not None else self._read_static_data(
            data_collection_id=data_collection_id,
            split_name=input_spec.split_id,
            expected_data_kind="DATA_KIND_PRE",
            request_id=request_id
        )

    def getLabels(
        self, data_collection_id: str, input_spec: i_s_proto.ModelInputSpec,
        request_id: str
    ) -> Optional[pd.DataFrame]:
        return self._read_static_data(
            data_collection_id=data_collection_id,
            split_name=input_spec.split_id,
            expected_data_kind="DATA_KIND_LABEL",
            request_id=request_id
        )

    def getExtraData(
        self, data_collection_id: str, input_spec: i_s_proto.ModelInputSpec,
        request_id: str
    ) -> pd.DataFrame:
        return self._read_static_data(
            data_collection_id=data_collection_id,
            split_name=input_spec.split_id,
            expected_data_kind="DATA_KIND_EXTRA",
            request_id=request_id
        )

    def getModelPredictions(
        self,
        project_id: str,
        request_id: str,
        qoi: QuantityOfInterest,
        input_spec: i_s_proto.ModelInputSpec,
        model_id: Optional[str] = None,
        include_system_data: bool = False
    ) -> Optional[pd.DataFrame]:
        # TODO:
        return None

    def getModelInfluences(
        self,
        project_id: str,
        request_id: str,
        input_spec: i_s_proto.ModelInputSpec,
        model_id: Optional[str] = None,
        include_system_data: bool = False
    ) -> Optional[pd.DataFrame]:
        # TODO:
        return None

    def _read_static_data(
        self, data_collection_id: str, split_name: str, expected_data_kind: str,
        request_id: str
    ) -> Optional[pd.DataFrame]:
        # really yapf3?
        data_locator = self._get_table_data_locator(
            data_collection_id, expected_data_kind, "TABLE_CATALOG_ICEBERG",
            request_id
        )
        if data_locator is None:
            return None

        sql_query = self._generate_query(data_locator, split_name)
        response_stream = self._do_query(request_id, sql_query)
        dataframe = self._pb_stream_to_dataframe(response_stream)
        return dataframe

    def _get_table_data_locator(
        self, data_collection_id: str, data_kind: str, catalog: str,
        request_id: str
    ) -> Optional[dl_pb.DataLocator]:

        try:
            locators = self.metarepo_client.search_table_data_locators(
                data_collection_id, data_kind, catalog
            )
        except Exception as ex:
            self.logger.error(
                f"encountered error while searching for table data locators: data_collection_id={data_collection_id}, data_kind={data_kind}, request_id={request_id}, error={str(ex)}"
            )
            raise ex

        locators_count = len(locators)
        if locators_count == 0:
            self.logger.info(
                f"could not find table data locators: data_collection_id={data_collection_id}, data_kind={data_kind}, request_id={request_id}"
            )
            return None

        if locators_count == 1:
            return locators[0]

        # locators_count > 1
        error_msg = f"found {locators_count} table data locators: data_collection_id={data_collection_id}, data_kind={data_kind}, request_id={request_id}"
        self.logger.error(error_msg)
        raise TruEraInternalError(error_msg)

    @staticmethod
    def _generate_query(
        data_locator: dl_pb.DataLocator, split_name: str
    ) -> str:
        # convert enum name to what we really want (naming conventions...)
        catalog = common_pb.TableCatalog.Name(data_locator.table.catalog)
        if catalog != 'TABLE_CATALOG_ICEBERG':  # defined in: protocol/truera/protobuf/public/common.proto
            raise TruEraInternalError(f"Unknown catalog name: {catalog}")
        catalog = "iceberg"
        schema = data_locator.table.schema
        table = data_locator.table.name
        return f"""SELECT * FROM "{catalog}"."{schema}"."{table}" WHERE __truera_split_name__ = '{split_name}'"""

    def _do_query(self, request_id: str, sql_query: str) -> qs_pb.QueryResponse:
        request = qs_pb.QueryRequest(
            request_id=request_id,
            sql_query=qs_pb.SQLQueryRequest(sql=sql_query)
        )
        return self.communicator.query(request)

    def _pb_stream_to_dataframe(
        self, response_stream: qs_pb.QueryResponse
    ) -> pd.DataFrame:
        first_element = True
        dataframes = []
        extractors = None
        dtypes = None
        table_metadata = None

        for stream_element in response_stream:
            self._check_response(stream_element)
            table = stream_element.row_major_value_table
            # only the first element contains the table's metadata
            if first_element:
                first_element = False
                extractors, dtypes, table_metadata = self._process_metadata(
                    table, stream_element.request_id
                )
            # create a dataframe from single pb message/stream element
            list_of_dicts = [
                self._extract_row_values(table_metadata, row, extractors)
                for row in table.rows
            ]
            df = pd.DataFrame(list_of_dicts)
            dataframes.append(df)

        if len(dataframes) == 0:
            raise TruEraInternalError(
                "QueryServiceClient::_pb_stream_to_dataframe got empty response from query service"
            )

        dataframe = pd.concat(dataframes, ignore_index=True, copy=False)
        return dataframe.astype(dtypes, copy=False)

    def _process_metadata(
        self, table: qs_pb.QueryResponse.row_major_value_table, request_id: str
    ) -> (dict, dict):
        if len(table.metadata) == 0:
            raise TruEraInternalError(
                "table metadata is not available. request_id={}.".
                format(request_id)
            )
        # python formatter is a gift that keeps on giving
        return self._value_extractors_for_response(
            table
        ), self._dtypes_for_response(table), table.metadata

    @staticmethod
    def _extract_row_values(table_metadata, row, extractors) -> dict:
        row_dict = defaultdict()
        for column_meta in table_metadata:
            cell = row.columns[column_meta.index]
            value_extractor = extractors.get(column_meta.index)
            value = value_extractor(cell)
            row_dict[column_meta.index] = value
        return row_dict

    # use qs_pb.ValueType and self.value_extractors_dict to assign a value extractor to each column based on response metadata
    def _value_extractors_for_response(
        self, table: qs_pb.QueryResponse.row_major_value_table
    ) -> dict:
        return {
            column_meta.index: self.value_extractors_dict.get(
                qs_pb.ValueType.Name(column_meta.type)
            ) for column_meta in table.metadata
        }

    # use qs_pb.ValueType and self.dtypes_dict to get dtypes for the dataframe based on response metadata
    def _dtypes_for_response(
        self, table: qs_pb.QueryResponse.row_major_value_table
    ) -> dict:
        return {
            column_meta.index:
            self.dtypes_dict.get(qs_pb.ValueType.Name(column_meta.type))
            for column_meta in table.metadata
        }

    @staticmethod
    def _check_response(response: qs_pb.QueryResponse):
        if response.error.code == qs_pb.Error.Code.NO_ERROR:
            return
        elif response.error.code == qs_pb.Error.Code.INTERNAL_SERVER_ERROR:
            raise TruEraInternalError(
                "could not obtain data. error=INTERNAL_SERVER_ERROR, message={}, request_id={}."
                .format(response.error.message, response.request_id)
            )
        else:
            raise TruEraInternalError(
                "could not obtain data. error=UNKNOWN_ERROR, message={}, request_id={}."
                .format(response.error.message, response.request_id)
            )
