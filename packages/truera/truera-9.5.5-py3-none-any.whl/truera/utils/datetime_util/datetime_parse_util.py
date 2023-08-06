import datetime
from typing import Optional

import pandas as pd

# Separate util from datetime_helper because it uses pandas which is not available in CLI (and is
# only there becuse other utils are used from that file.)


def get_datetime_from_string(time_string: str) -> datetime.datetime:
    return pd.to_datetime(time_string).to_pydatetime()


def get_datetime_from_proto_string(
    time_string: Optional[str]
) -> datetime.datetime:
    return get_datetime_from_string(
        time_string
    ) if time_string else datetime.datetime.min
