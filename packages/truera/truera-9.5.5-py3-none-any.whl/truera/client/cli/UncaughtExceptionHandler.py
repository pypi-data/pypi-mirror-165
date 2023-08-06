import sys

import click

from truera.artifactrepo.arlib import artifactrepolib as lib
from truera.client.client_utils import BadTimestampException
from truera.client.client_utils import InvalidArgumentCombinationException
from truera.client.client_utils import InvalidQuantityOfInterestError
from truera.client.client_utils import TextFormatNotSupportedError
import truera.client.client_utils as client_utils
from truera.client.errors import AuthorizationDenied
from truera.client.errors import DirectoryAlreadyExistsException
from truera.client.errors import FileDoesNotExistException
from truera.client.errors import InvalidFrameworkWrapperException
from truera.client.errors import MetadataNotFoundException
from truera.client.errors import MissingEnvironmentSpecException
from truera.client.errors import NotFoundError
from truera.client.errors import PackageVerificationException
import truera.client.feature_client as feature_client
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.public.communicator.http_communicator import \
    AuthenticationFailedError
from truera.client.public.communicator.http_communicator import \
    NotSupportedError
from truera.client.public.communicator.http_communicator import \
    UnauthorizedAccessError
from truera.client.public.communicator.http_communicator import UnknownRpcError
import truera.client.services.artifact_interaction_client as cl
from truera.client.services.artifactrepo_client import DeleteFailedException
from truera.client.services.artifactrepo_client import \
    LabelIngestionFailedException
from truera.utils.truera_status import TruEraPermissionDeniedError


class UncaughtExceptionHandler():

    @staticmethod
    def wrap(f, *args):
        try:
            f(*args)
            return
        except AlreadyExistsError as e:
            click.echo(e.message)
        except NotFoundError as e:
            click.echo(e.message)
        except DeleteFailedException as e:
            click.echo(e.message)
        except DirectoryAlreadyExistsException as e:
            click.echo(e.message)
        except FileDoesNotExistException as e:
            click.echo(e.message)
        except InvalidFrameworkWrapperException as e:
            click.echo(e.message)
        except MissingEnvironmentSpecException as e:
            click.echo(e.message)
        except PackageVerificationException as e:
            click.echo(e.message)
        except client_utils.NotSupportedFileTypeException as e:
            click.echo(e.message)
        except feature_client.InvalidMapException as e:
            click.echo(e.message)
        except InvalidQuantityOfInterestError as e:
            click.echo(e.message)
        except TextFormatNotSupportedError as e:
            click.echo(e.message)
        except BadTimestampException as e:
            click.echo(e.message)
        except InvalidArgumentCombinationException as e:
            click.echo(e.message)
        except MetadataNotFoundException as e:
            click.echo(e.message)
        except cl.SplitTooLargeError as e:
            click.echo(e.message)
        except AuthenticationFailedError as e:
            click.echo(e.message)
        except UnauthorizedAccessError as e:
            click.echo(e.message)
        except UnknownRpcError as e:
            click.echo(e.message)
        except NotSupportedError as e:
            click.echo(e.message)
        except cl.InvalidModelFolderException as e:
            click.echo(e.message)
        except lib.EmptyIteratorError as e:
            click.echo(e.message)
        except cl.MissingParameterException as e:
            click.echo(e.message)
        except cl.InvalidColumnInfoFileException as e:
            click.echo(e.message)
        except cl.RowsetNotPersistableException as e:
            click.echo(e.message)
        except client_utils.ContextSetupException as e:
            click.echo(e.message)
        except client_utils.VersionMismatchError as e:
            click.echo(e.message)
        except cl.InvalidFilterError as e:
            click.echo(e.message)
        except LabelIngestionFailedException as e:
            click.echo(e.message)
        except AuthorizationDenied as e:
            click.echo(e.message)
        except TruEraPermissionDeniedError as e:
            click.echo(e.message)
        except Exception as e:
            click.echo(e)
            raise

        sys.exit(1)
