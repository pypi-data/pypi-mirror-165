import datetime
import functools
import inspect
import logging
import os
from distutils.util import strtobool
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import colorama
import pandas as pd
from typeguard import typechecked
from typing_extensions import Literal

from gantry.const import DEFAULT_ENV, PROD_API_URL
from gantry.exceptions import ClientNotInitialized
from gantry.logger.client import Gantry
from gantry.logger.stores import APILogStore

colorama.init(autoreset=True)
logger_obj = logging.getLogger(__name__)
logger_obj.addHandler(logging.NullHandler())

_CLIENT: Optional[Gantry] = None


def _client_alias(f):
    doc = "Alias for :meth:`gantry.logger.client.Gantry.{}`".format(f.__name__)
    orig_doc = inspect.getdoc(getattr(Gantry, f.__name__))

    if orig_doc:
        doc += "\n\n{}".format(orig_doc)

    f.__doc__ = doc

    # This decorator also checks that the _CLIENT
    # has been initialized
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if _CLIENT is None:
            raise ClientNotInitialized()

        return f(*args, **kwargs)

    return wrapper


LOGGING_LEVEL_T = Literal["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]


@typechecked
def _resolve_params(
    api_key: Optional[str] = None,
    logs_location: Optional[str] = None,
    logging_level: Optional[LOGGING_LEVEL_T] = None,
    environment: Optional[str] = None,
    bypass_firehose: Optional[bool] = None,
    send_in_background: Optional[bool] = None,
) -> Tuple[str, str, LOGGING_LEVEL_T, str, bool, bool]:
    api_key = api_key or os.environ.get("GANTRY_API_KEY")
    if api_key is None:
        raise ValueError("logger was not initialized with API Key")

    logs_location = cast(str, logs_location or os.environ.get("GANTRY_LOGS_LOCATION", PROD_API_URL))
    logging_level = cast(
        LOGGING_LEVEL_T, logging_level or os.environ.get("GANTRY_LOGGING_LEVEL", "INFO")
    )
    environment = cast(str, environment or os.environ.get("GANTRY_ENVIRONMENT", DEFAULT_ENV))

    # TODO: use urlparse to grab the scheme instead
    if not (logs_location.startswith("http://") or logs_location.startswith("https://")):
        logger_obj.error("Currently only HTTP logs location supported")
        raise ValueError(
            "logger was not initialized with http endpoint. Only HTTP logs locations supported."
        )

    if bypass_firehose is None:
        bypass_firehose = bool(strtobool(os.environ.get("GANTRY_BYPASS_FIREHOSE", "false")))

    if send_in_background is None:
        if "GANTRY_SEND_IN_BACKGROUND" in os.environ:
            send_in_background = bool(strtobool(os.environ["GANTRY_SEND_IN_BACKGROUND"]))
        else:
            # Set sync behavior in case app is running in a lambda (scenario in which
            # we can't start a thread).
            # https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
            send_in_background = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is None

    return api_key, logs_location, logging_level, environment, bypass_firehose, send_in_background


def init(
    api_key: Optional[str] = None,
    logs_location: Optional[str] = None,
    logging_level: Optional[LOGGING_LEVEL_T] = None,
    environment: Optional[str] = None,
    bypass_firehose: Optional[bool] = None,
    send_in_background: Optional[bool] = None,
):
    """
    Initialize the logger. Initialization should happen before submitting any data to Gantry.

    Example:

    .. code-block:: python

       import gantry
       gantry.init(api_key="foobar")


    Args:
        api_key (optional, str): The Gantry API Key. You can also set this parameter by setting
            the env variable GANTRY_API_KEY.
        logs_location (optional, str): URL where Gantry records will be sent. You can also
            set this parameter by setting the env variable GANTRY_LOGS_LOCATION. If not specified,
            it will default to the prod SaaS URL. DO NOT SPECIFY THIS PARAMETER unless indicated.
        logging_level (str): Set logging level for Gantry system logging. You can also set this
            parameter by setting the env variable GANTRY_LOGGING_LEVEL.
            If not specified, it defaults to INFO.
        environment (str): Set the value for the environment label attached to data instrumented.
            You can also set this parameter by setting the env variable GANTRY_ENVIRONMENT.
            If not provided, it defaults to "dev".
        bypass_firehose (bool, defaults to False): when in development mode, optionally turn
            this on to send raw events to the worker rather than going through Firehose.
            You can also set this parameter by setting the env variable GANTRY_BYPASS_FIREHOSE
            If not provided, it defaults to False.
            USE THIS PARAMETER ONLY FOR DEVELOPMENT PURPOSES.
        send_in_background (optional, bool): set whether Gantry logging methods should
            run synchronously or not. You can also set this value by setting
            the env variable GANTRY_SEND_IN_BACKGROUND.
            If not provided, it defaults to True unless running in an AWS lambda.

    """
    (
        api_key,
        logs_location,
        logging_level,
        environment,
        bypass_firehose,
        send_in_background,
    ) = _resolve_params(
        api_key, logs_location, logging_level, environment, bypass_firehose, send_in_background
    )

    global _CLIENT

    log_store = APILogStore(
        location=logs_location,
        api_key=api_key,
        bypass_firehose=bypass_firehose,
        send_in_background=send_in_background,
    )
    _CLIENT = Gantry(log_store, environment, logging_level)

    logger_obj.debug("Gantry logger initialized")

    if not _CLIENT.ping():
        logger_obj.warning(
            "Gantry services not reachable. Check provided URL "
            f"[{logs_location}] is pointing to the correct address"
        )
        return

    if not _CLIENT.ready():
        logger_obj.warning("Gantry services won't receive traffic. Check if API Key is valid")


@_client_alias
def instrument(*args, **kwargs):
    return _CLIENT.instrument(*args, **kwargs)


@_client_alias
def ping():
    return _CLIENT.ping()


@_client_alias
def ready():
    return _CLIENT.ready()


@_client_alias
def log_feedback_event(*args, **kwargs):
    return _CLIENT.log_feedback_event(*args, **kwargs)


@_client_alias
def log_feedback(*args, **kwargs):
    return _CLIENT.log_feedback(*args, **kwargs)


@_client_alias
def log_file(
    application: str,
    filepath: str,
    version: Optional[Union[int, str]] = None,
    timestamp: Optional[str] = None,
    inputs: List[str] = [],
    outputs: List[str] = [],
    feedbacks: List[str] = [],
    tags: List[str] = [],
    feedback_id: List[str] = [],
    feedback_keys: Optional[List[str]] = None,
):
    return _CLIENT.log_file(**locals())  # type: ignore[union-attr]


@_client_alias
def log_record(
    application: str,
    version: Optional[Union[int, str]] = None,
    inputs: Optional[Dict[Any, Any]] = None,
    outputs: Optional[Any] = None,
    feedback_id: Optional[Dict[Any, Any]] = None,
    feedback: Optional[Dict[Any, Any]] = None,
    feedback_keys: Optional[List[str]] = None,
    ignore_inputs: Optional[List[str]] = None,
    timestamp: Optional[datetime.datetime] = None,
    sample_rate: float = 1.0,
    tags: Optional[Dict[str, str]] = None,
) -> None:
    return _CLIENT.log_record(**locals())  # type: ignore[union-attr]


@_client_alias
def log_records(
    application: str,
    version: Optional[Union[int, str]] = None,
    inputs: Optional[Union[List[Dict[Any, Any]], pd.DataFrame]] = None,
    outputs: Optional[Union[List[Dict[Any, Any]], pd.DataFrame]] = None,
    feedback_keys: Optional[List[str]] = None,
    feedback_ids: Optional[List[Dict[Any, Any]]] = None,
    feedbacks: Optional[Union[List[Dict[Any, Any]], pd.DataFrame]] = None,
    ignore_inputs: Optional[List[str]] = None,
    timestamps: Optional[List[datetime.datetime]] = None,
    sort_on_timestamp: bool = True,
    sample_rate: float = 1.0,
    as_batch: bool = False,
    tags: Optional[Dict[str, str]] = None,
) -> None:
    return _CLIENT.log_records(**locals())  # type: ignore[union-attr]


@_client_alias
def log_prediction_event(*args, **kwargs):
    return _CLIENT.log_prediction_event(*args, **kwargs)


@_client_alias
def log_predictions(*args, **kwargs):
    return _CLIENT.log_predictions(*args, **kwargs)


def get_client():
    return _CLIENT


def setup_logger(level: str = "INFO"):
    return Gantry.setup_logger(level)
