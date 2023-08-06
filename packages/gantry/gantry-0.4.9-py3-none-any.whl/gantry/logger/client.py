import datetime
import functools
import inspect
import json
import logging
import math
import os
import random
import sys
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from warnings import warn

import pandas as pd
import requests
from tqdm import tqdm
from typeguard import typechecked

from gantry.exceptions import GantryBatchCreationException, GantryLoggingException
from gantry.logger.constants import CHUNK_SIZE, BatchType
from gantry.logger.event_builder import (
    _build_data_link,
    _build_feedback_event,
    _build_prediction_and_feedback_events,
    _build_prediction_event,
    _build_prediction_events,
    _create_timestamp_idx,
)
from gantry.logger.stores import APILogStore
from gantry.logger.types import DataLink
from gantry.logger.utils import (
    _batch_fail_msg,
    _batch_success_msg,
    _build_batch_iterator,
    _check_sample_rate,
    _is_empty,
    _is_not_empty,
    _log_exception,
)
from gantry.serializers import EventEncoder, serializable_value

logger = logging.getLogger(__name__)


class Gantry:
    def __init__(
        self,
        log_store: APILogStore,
        environment: str,
        logging_level: str = "INFO",
    ):
        """
        Initializes a new Gantry client to log predictions and feedback.
        Full list of arguments is defined by :class:`gantry.config.ConfigSchema`.

        Args:
            logs_store (BaseLogStore): The log store to use.
            environment (optional, str): Set the value for the environment label attached to data
                instrumented by this client. This value can be overridden for each record using
                tags.
            logging_level (options: str): Configure logging level for Gantry system.
        """
        self.context = {"environment": environment}
        self.log_store = log_store
        self.environment = environment
        self.setup_logger(level=logging_level)

    def instrument(
        self,
        application: str,
        version: Optional[int] = None,
        feedback_keys: Optional[List[str]] = None,
        ignore_inputs: Optional[List[str]] = None,
        sample_rate: float = 1.0,
    ):
        """
        Function decorator to be used on an inference function that should be instrumented
        by Gantry.

        Example:

        .. code-block:: python

           import gantry

           gantry.init(...)

           @gantry.instrument("loan_pred", feedback_keys=['loan_id'], ignore_inputs=['loan_id'])
           def _predict(
               loan_id: str,  # id of loan, important metadata but not used in predicting
               college_degree: bool,  # if applicant has college degree
               loan_amount: float,  # in $1,000s
           ):
               ...

        Args:
            application (str): Application name. Gantry validates and monitors data by function.
            version (optional, int): Version of the function schema to use for validation by Gantry.
                If not provided, Gantry will use the latest version. If the version doesn't exist
                yet, Gantry will create it by auto-generating the schema based on data it has seen.
            feedback_keys (optional, list): A list of names of input features to use for feedback
                lookup. When you later provide a feedback event or label for performance metric
                calculation, you will provide the values of the features in this list for
                Gantry to look up the corresponding prediction.
            ignore_inputs (optional, list): A list of names of input features that should not be
                monitored.
            sample_rate (optional, float): Set a sampling rate to control the fraction of events
                logged by Gantry. E.g. if sample_rate is 0.3, only 30% of events are logged.
        """

        def outer(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                outputs = func(*args, **kwargs)

                if random.random() > sample_rate:
                    return outputs

                try:
                    bound_args = inspect.signature(func).bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    raw_inputs = dict(bound_args.arguments)

                    ev = _build_prediction_event(
                        self.context,
                        self.environment,
                        raw_inputs,
                        outputs,
                        application,
                        version,
                        feedback_keys,
                        ignore_inputs,
                    )
                    self.log_store.log(application, ev)
                except GantryLoggingException as le:
                    # this is caused by a user error
                    # log the error without the stacktrace
                    logger.error("Error logging data to Gantry: %s", le)
                except Exception as e:
                    # make sure our logging errors don't cause exceptions in main program
                    logger.exception("Internal exception in Gantry client: %s", e)

                return outputs

            return wrapper

        return outer

    @_log_exception
    @typechecked
    def log_file(
        self,
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
        data_link = _build_data_link(
            application,
            self.environment,
            version,
            timestamp,
            inputs,
            outputs,
            feedbacks,
            tags,
            feedback_id,
            feedback_keys,
            filepath=filepath,
            batch_type=BatchType.RECORD,  # TODO: Determine this by the data_link request.
        )
        object_size = os.path.getsize(filepath)  # in bytes
        path = Path(filepath)
        with open(filepath, "r") as f_in:
            block_read = functools.partial(f_in.read, CHUNK_SIZE)
            block_iterator = iter(block_read, "")
            self._handle_upload(
                block_iterator, data_link, object_size, f"{uuid.uuid4()}_{path.name}"
            )

    def _handle_upload(
        self, data_batch_iterator: Iterable, data_link: DataLink, object_size: int, filename: str
    ):
        # Calculate part counts and generate presigned s3 urls.
        total_num_parts = math.ceil(object_size / CHUNK_SIZE)

        logger.info("Initializing upload to Gantry")
        preupload_res = self.log_store._api_client.request(
            "GET",
            "/api/v1/ingest/file-preupload",
            params={
                "filename": filename,
                "num_parts": total_num_parts,
                "filetype": data_link.file_type,
            },
        )
        if "upload_urls" not in preupload_res:
            raise GantryBatchCreationException(
                "Failed to start batch upload. Please check your API key."
            )
        signed_urls = preupload_res["upload_urls"]
        upload_id = preupload_res["upload_id"]
        file_key = preupload_res["key"]

        # Upload the parts.
        parts = []
        part_num = 1  # AWS S3 needs part num to start with 1.
        for block in tqdm(
            data_batch_iterator, desc="Uploading to Gantry Bucket: ", total=total_num_parts
        ):
            # TODO: parallelize this client side?
            response = requests.put(signed_urls[part_num - 1], data=block)
            etag = str(response.headers["ETag"])
            parts.append({"ETag": etag, "PartNumber": part_num})
            part_num += 1

        logger.info("Starting Gantry Ingestion")
        # Submit file completion to gantry API.
        complete_res = self.log_store._api_client.request(
            "POST",
            "/api/v1/ingest/file",
            json={
                "upload_id": upload_id,
                "key": file_key,
                "parts": parts,
                "data_link": asdict(data_link),
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        if "batch_id" not in complete_res:
            raise GantryBatchCreationException(
                "Failed to complete upload. Please contact Gantry support."
            )
        batch_id = complete_res["batch_id"]
        _batch_success_msg(batch_id, data_link.application, self.log_store)

    @_log_exception
    @typechecked
    def log_records(
        self,
        application: str,
        version: Optional[Union[int, str]] = None,
        inputs: Optional[Union[List[dict], pd.DataFrame]] = None,
        outputs: Optional[Union[List[Any], List[dict], pd.DataFrame]] = None,
        feedback_keys: Optional[List[str]] = None,
        feedback_ids: Optional[List[dict]] = None,
        feedbacks: Optional[Union[List[dict], pd.DataFrame]] = None,
        ignore_inputs: Optional[List[str]] = None,
        timestamps: Optional[Union[List[datetime.datetime], pd.DatetimeIndex]] = None,
        sort_on_timestamp: bool = True,
        sample_rate: float = 1.0,
        as_batch: bool = False,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Function to record a batch of events containing predictions (inputs and outputs),
        feedback, or both simultaneously.

        To log predictions using this method, both inputs and outputs must be passed.
        To log feedbacks using this method, both feedback_ids and feedbacks must be passed.

        User can alternatively use :meth:`gantry.logger.client.Gantry.log_predictions`
        to log batches of predictions only or :meth:`gantry.logger.client.Gantry.log_feedback`
        to log batches of feedbacks only.

        Example:

        .. code-block:: python

           # Record an application's feedback
            gantry.log_records(
                application='foobar',
                inputs=[{'A': 100}, {'A': 101}],
                outputs=[{'B': 'foo'}, {'B': 'bar'}],
                version=1,
                feedback_keys=["A"],
                feedbacks=[{'B': 'bar'}, {'B': 'foo'}],
                tags={"env": "environment1"}
            )
                ...

        Args:
            application (str): Name of the application. Gantry validates and monitors data
                by function.
            version (optional, Union[int, str]): Version of the function schema to use for
                validation by Gantry.
                If not provided, Gantry will use the latest version. If the version doesn't exist
                yet, Gantry will create it by auto-generating the schema based on data it has seen.
            inputs (Union[List[dict], pd.Dataframe]): A list of prediction inputs. `inputs[i]`
                is a dict of the features for the i-th prediction to be logged.
            outputs (Union[List[dict], pd.Dataframe]): A list of prediction outputs. `outputs[i]`
                should be the application output for the prediction with features `inputs[i]`.
            feedback_keys (optional, List[str]): A list of names of input features to use for
                feedback lookup. When you later provide a feedback event or label for
                performance metric calculation, you will provide the values of the features
                in this list for Gantry to look up the corresponding prediction.
            feedback_ids (optional, List[dict]): A list of prediction feedback ids. The i-th entry
                corresponds to the argument `feedback_ids` in
                :meth:`gantry.client.Gantry.log_predictions` for the i-th prediction event.
            feedbacks (Union[List[dict], pd.DataFrame]): A list of feedbacks. `feedbacks[i]`
                is a dict of the features for the i-th prediction to be logged.
            ignore_inputs (optional, List[str]): A list of names of input features that should not
                be monitored.
            timestamps (optional, Union[List[datetime.datetime], pd.DatetimeIndex): A list of
                prediction timestamps. If specified, `timestamps[i]` should be the timestamps
                for the i-th prediction. If timestamps = None (default), then the prediction
                timestamp defaults to the time when `log_records` is called.
            sort_on_timestamp (bool, defaults to True): Works when timestamps are provided.
                Sort using the given timestamp. Default to True.
            sample_rate: Used for down-sampling. The probability as a float that each record
                will be sent to Gantry.
            as_batch (bool, defaults to False): Whether to add batch metadata and tracking
                in the 'batch' section of the dashboard
            tags (optional, Optional[Dict[str, str]]): A tag is a label that you assign to your
                data. E.g. you can specify which environment the data belongs to by setting "env"
                tag like this tags = {"env": "environment1"} if not assigned we will use Gantry
                client's environment value as the default environment.

        """
        some_preds_exist = _is_not_empty(inputs) or _is_not_empty(outputs)
        preds_exist = _is_not_empty(inputs) and _is_not_empty(outputs)
        feedbacks_exist = _is_not_empty(feedbacks)

        if not preds_exist and some_preds_exist:
            raise ValueError(
                "Tried to log records with incomplete prediction "
                "(both inputs and outputs should be provided)"
            )

        if preds_exist and feedbacks_exist:
            return self._log_predictions_and_feedbacks(
                application=application,
                inputs=inputs,
                outputs=outputs,
                feedbacks=feedbacks,
                version=version,
                feedback_keys=feedback_keys,
                ignore_inputs=ignore_inputs,
                timestamps=timestamps,
                sort_on_timestamp=sort_on_timestamp,
                sample_rate=sample_rate,
                as_batch=as_batch,
                tags=tags,
            )
        elif preds_exist:
            return self.log_predictions(
                application,
                inputs,
                outputs,
                version,
                feedback_keys,
                ignore_inputs,
                feedback_ids,
                timestamps,
                sort_on_timestamp,
                sample_rate,
                as_batch,
                tags,
            )
        elif feedbacks_exist:
            return self.log_feedback(
                application,
                feedback_ids,
                feedbacks,
                version,
                timestamps,
                sort_on_timestamp,
                sample_rate,
                as_batch,
                tags,
            )
        else:
            logger.error("Tried to log_records without prediction and without feedback")

    @_log_exception
    def ping(self) -> bool:
        """
        Pings the log store API server to check if it is alive.
        Returns True if alive, False if there is an error during ping process.
        """
        return self.log_store.ping()

    def _get_env_and_context(self, tags: Optional[Dict]) -> Tuple[str, Dict]:
        if tags and tags.get("env"):
            return tags["env"], {"environment": tags.get("env")}
        else:
            return self.environment, self.context

    @_log_exception
    def ready(self) -> bool:
        """
        Checks if API is ready to receive traffic.
        Returns True if ready, False otherwise.
        """
        return self.log_store.ready()

    @_log_exception
    def _log_predictions_and_feedbacks(
        self,
        application: str,
        inputs: Union[List[dict], pd.DataFrame],
        outputs: Union[List[dict], pd.DataFrame],
        feedbacks: Union[List[dict], pd.DataFrame],
        version: Optional[Union[int, str]] = None,
        feedback_keys: Optional[List[str]] = None,
        ignore_inputs: Optional[List[str]] = None,
        timestamps: Optional[Union[List[datetime.datetime], pd.DatetimeIndex]] = None,
        sort_on_timestamp: bool = True,
        sample_rate: float = 1.0,
        as_batch: bool = False,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """Internal method to log batch of predictions AND feedbacks"""
        if any(_is_empty(d) for d in [inputs, outputs, feedbacks]):
            raise GantryLoggingException(
                "In order to use log_records method, inputs/outputs/feedbacks need to be provided"
            )

        if not (len(inputs) == len(outputs) == len(feedbacks)):
            raise GantryLoggingException(
                "Size mismatch in data: {} inputs, {} outputs, {} feedbacks".format(
                    len(inputs), len(outputs), len(feedbacks)
                )
            )

        size = len(inputs)

        if timestamps is not None and len(timestamps) != size:
            raise GantryLoggingException(
                "Size mismatch in timestamps: {} data points, {} timestamps".format(
                    size, len(timestamps)
                )
            )

        inputs = serializable_value(inputs)
        outputs = serializable_value(outputs)
        feedbacks = serializable_value(feedbacks)
        version = serializable_value(version)

        environment, context = self._get_env_and_context(tags)

        timestamp_idx = _create_timestamp_idx(sort_on_timestamp, timestamps, size)

        events = _build_prediction_and_feedback_events(
            application=application,
            context=context,
            environment=environment,
            timestamp_idx=timestamp_idx,
            tags=tags,
            version=version,
            inputs=inputs,
            outputs=outputs,
            feedback_keys=feedback_keys,
            feedbacks=feedbacks,
            ignore_inputs=ignore_inputs,
            sample_rate=sample_rate,
        )

        if events:
            if as_batch:
                self._upload_data_as_batch(
                    application, environment, version, events, BatchType.RECORD
                )
            else:
                self.log_store.log_batch(application, events)
        else:
            logger.info("No events to log")

    @_log_exception
    @typechecked
    def log_record(
        self,
        application: str,
        version: Optional[Union[int, str]] = None,
        inputs: Optional[dict] = None,
        outputs: Optional[Any] = None,
        feedback_id: Optional[dict] = None,
        feedback: Optional[dict] = None,
        feedback_keys: Optional[List[str]] = None,
        ignore_inputs: Optional[List[str]] = None,
        timestamp: Optional[datetime.datetime] = None,
        sample_rate: float = 1.0,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Function to record an event, regardless of inputs. Allows client to pass in inputs,
        predictions, and/or feedback for one record.

        Logs error for any individual failures, but does not fail unless method called with
        invalid parameters.

        To log predictions using this method, both inputs and outputs must be passed.
        To log feedback using this method, both feedback_id and feedback must be passed.

        Example:

        .. code-block:: python

           # Record an application's feedback
            gantry.log_record(
                application='foobar',
                inputs={'A': 100},
                outputs={'value': 'bar'},
                version=1,
                feedback_keys=["A"],
                feedback_id={'A': 100},
                tags = {"env":"environment1"}
            )
                ...

        Args:
            application (str): Name of the application. Gantry validates and monitors data by
                function.
            version (optional, int): Version of the function schema to use for validation by Gantry.
                If not provided, Gantry will use the latest version. If the version doesn't exist
                yet, Gantry will create it by auto-generating the schema based on data it has seen.
            inputs (optional, dict): Inputs to the prediction. A dict where the keys are the feature
                names and the values are the feature values.
            outputs (optional, Any): application output on the prediction.
            feedback_id (optional, Dict[str, Any]): A dictionary mapping string keys to values on
                which the feedback id is computed for matching prediction and feedback events.
                Should be the same as the argument `feedback_id` to
                :meth:`gantry.client.Gantry.log_feedback_event` for the matching feedback event.
            feedback (optional, dict): application feedback object.
            feedback_keys (optional, list[str]): A list of names of input features to use for
                feedback lookup. When you later provide a feedback event or label for performance
                metric calculation, you will provide the values of the features in this list for
                Gantry to look up the corresponding prediction.
            ignore_inputs (optional, list[str]): A list of names of input features that should not
                be monitored.
            timestamp (optional, datetime.datetime): Specify a custom timestamp for the when the
                prediction occured. Useful for recording predictions from the past. If not
                specified, then the prediction timestamp defaults to when `log_record` was
                called.
            sample_rate (optional, float): Specify the probability as a float that the event will
                be sent to Gantry.
            tags (optional, Optional[Dict[str, str]]): A tag is a label that you assign to your
                data. E.g. you can specify which environment the data belongs to by setting "env"
                tag like this tags = {"env": "environment1"} if not assigned we will use Gantry
                client's environment value as the default environment.
        """
        some_pred_exist = _is_not_empty(inputs) or _is_not_empty(outputs)
        pred_exist = _is_not_empty(inputs) and _is_not_empty(outputs)
        feedback_exist = _is_not_empty(feedback)

        if (not pred_exist) and some_pred_exist:
            raise ValueError(
                "Tried to log records with incomplete prediction "
                "(both inputs and outputs should be provided)"
            )

        if pred_exist and feedback_exist:
            return self._log_prediction_and_feedback_event(
                application=application,
                version=version,
                inputs=inputs,
                outputs=outputs,
                feedback=feedback,
                feedback_keys=feedback_keys,
                ignore_inputs=ignore_inputs,
                timestamp=timestamp,
                sample_rate=sample_rate,
                tags=tags,
            )
        elif pred_exist:
            return self.log_prediction_event(
                application=application,
                inputs=inputs,
                outputs=outputs,
                version=version,
                feedback_keys=feedback_keys,
                ignore_inputs=ignore_inputs,
                feedback_id=feedback_id,
                timestamp=timestamp,
                sample_rate=sample_rate,
                tags=tags,
            )
        elif feedback_exist:
            return self.log_feedback_event(
                application=application,
                feedback_id=feedback_id,
                feedback=feedback,
                feedback_version=version,
                timestamp=timestamp,
                sample_rate=sample_rate,
                tags=tags,
            )
        else:
            logger.error("Tried to log record without prediction and without feedback")

    @_log_exception
    def _log_prediction_and_feedback_event(
        self,
        application: str,
        inputs: dict,
        outputs: Any,
        feedback: Optional[dict],
        version: Optional[Union[int, str]] = None,
        feedback_keys: Optional[List[str]] = None,
        ignore_inputs: Optional[List[str]] = None,
        timestamp: Optional[datetime.datetime] = None,
        sample_rate: float = 1.0,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """Internal method to log an event with prediction AND feedback"""
        _check_sample_rate(sample_rate)
        if random.random() > sample_rate:
            return

        ev = {}

        # don't require feedback_id if they gave us all the info to compute it
        feedback_id = {k: inputs[k] for k in (feedback_keys or [])}  # type: ignore

        environment, context = self._get_env_and_context(tags)

        ev.update(
            _build_prediction_event(
                context,
                environment,
                inputs,  # type: ignore
                outputs,
                application,
                version,
                feedback_keys,
                ignore_inputs,
                feedback_id=None,
                custom_timestamp=timestamp,
                tags=tags,
            )
        )

        fev = _build_feedback_event(
            context,
            application,
            feedback_id,  # type: ignore
            feedback,  # type: ignore
            version,
            timestamp,
        )

        ev["metadata"].update(fev.pop("metadata"))  # update nested dict separately
        ev.update(fev)
        self.log_store.log(application, ev)

    @_log_exception
    @typechecked
    def log_feedback_event(
        self,
        application: str,
        feedback_id: dict,
        feedback: dict,
        feedback_version: Optional[Union[str, int]] = None,
        timestamp: Optional[datetime.datetime] = None,
        sample_rate: float = 1.0,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        DEPRECATION WARNING:
        This method will be deprecated soon. Please use `log_record` instead.

        Endpoint to directly register a single feedback with Gantry.

        Example:

        .. code-block:: python

           # Record an application's feedback
           gantry.log_feedback_event(
               "loan_pred",
               {"loan_id": "00014"}
               {"label": True}
            )
                ...

        Args:
            feedback_id (dict): A dict where the keys are feedback keys (as specified in
                the `feedback_keys` arg of `gantry.instrument` or `log_prediction_event(s)` and
                the value matches the value in the corresponding prediction. The feedback event
                is matched to the prediction event using the values of the feedback keys.
            feedback (dict): application feedback object.
            feedback_version (optional, int or str): Specify application version.
            timestamp (optional, datetime.datetime): Record timestamp.
            sample_rate (optional, float): Specify the probability as a float that the event will
                be sent to Gantry.
        """
        warn(
            "Deprecated: this method will be soon deprecated. Use `log_record` instead",
            DeprecationWarning,
        )

        _check_sample_rate(sample_rate)
        if random.random() > sample_rate:
            return

        _, context = self._get_env_and_context(tags)

        ev = _build_feedback_event(
            context, application, feedback_id, feedback, feedback_version, timestamp
        )
        self.log_store.log(application, ev)

    @_log_exception
    @typechecked
    def log_feedback(
        self,
        application: str,
        feedback_ids: List[dict],
        feedbacks: Union[List[dict], pd.DataFrame],
        feedback_version: Optional[Union[str, int]] = None,
        timestamps: Optional[Union[List[datetime.datetime], pd.DatetimeIndex]] = None,
        sort_on_timestamp: bool = True,
        sample_rate: float = 1.0,
        as_batch: bool = False,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        DEPRECATION WARNING:
        This method will be deprecated soon. Please use `log_records` instead.

        Endpoint to register a batch of feedbacks.
        Logs error for any individual failures, but does not fail unless method called with
        invalid parameters.

        Args:
            feedback_ids (list): A list of dicts. dict where the keys are feedback keys
                (as specified in the `feedback_keys` arg of `gantry.instrument` or
                `log_prediction_event(s)`) and the value matches the value in the
                corresponding prediction. The feedback event is matched to the prediction
                event using the values of the feedback keys. The i-th feedback_id maps to
                the i-th feedback.
            feedback (list): List of application feedback objects.
            feedback_version (optional, int or str): Specify application version.
            timestamps (optional, datetime.datetime): Record timestamps. The i-th timestamp
                maps to the i-th feedback.
            sort_on_timestamp (optional, boolean): Specify whether result should sort on timestamp.
            sample_rate (optional, float): Specify the probability as a float that the event will
                be sent to Gantry.
        """
        warn(
            "Deprecated: this method will be soon deprecated. Use `log_records` instead",
            DeprecationWarning,
        )

        batch_id = None
        try:
            feedback_ids = serializable_value(feedback_ids)
            feedbacks = serializable_value(feedbacks)
            serialized_version: Union[str, int] = serializable_value(feedback_version)

            timestamp_idx = _create_timestamp_idx(sort_on_timestamp, timestamps, len(feedbacks))

            if len(feedback_ids) == len(feedbacks):
                events = []
                environment, context = self._get_env_and_context(tags)

                for idx, timestamp in timestamp_idx:
                    try:
                        if random.random() > sample_rate:
                            continue

                        events.append(
                            _build_feedback_event(
                                context,
                                application,
                                feedback_ids[idx],
                                feedbacks[idx],
                                serialized_version,
                                timestamp,
                                batch_id=batch_id,
                            )
                        )
                    except GantryLoggingException as le:
                        # this is caused by a user error
                        # log the error without the stacktrace
                        logger.error("Error logging data to Gantry: %s", le)
                    except Exception as e:
                        logger.error(
                            "Failed to log feedback with id {} due to {}".format(
                                feedback_ids[idx], e
                            )
                        )

                if events:
                    if as_batch:
                        self._upload_data_as_batch(
                            application, environment, serialized_version, events, BatchType.FEEDBACK
                        )
                    else:
                        batch_id = None
                        self.log_store.log_batch(application, events)
                        _batch_success_msg(batch_id, application, self.log_store)
                else:
                    logger.info("No events to log")
            else:
                raise GantryLoggingException(
                    "Feedback_ids and feedbacks lists don't have same length."
                )
        except Exception as e:
            _batch_fail_msg(batch_id)

            raise e

    @_log_exception
    @typechecked
    def log_prediction_event(
        self,
        application: str,
        inputs: dict,
        outputs: Any,
        version: Optional[Union[int, str]] = None,
        feedback_keys: Optional[List[str]] = None,
        ignore_inputs: Optional[List[str]] = None,
        feedback_id: Optional[dict] = None,
        timestamp: Optional[datetime.datetime] = None,
        sample_rate: float = 1.0,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        DEPRECATION WARNING:
        This method will be deprecated soon. Please use `log_record` instead.

        Endpoint to directly register a prediction with Gantry. This endpoint includes many
        of the same arguments as :meth:`gantry.client.Gantry.instrument`, but allows the user to
        specify a custom event timestamp with the `timestamp` argument to make it possible to record
        predictions from the past. While :meth:`gantry.client.Gantry.instrument` is useful
        for capturing future predictions from an application function, this method is useful
        to record previous predictions to Gantry: for example old predictions stored in a
        database.

        Example:

        .. code-block:: python

           import gantry

           gantry.init(...)

           # Record a prediction from the previous day
           gantry.log_prediction_event(
               "loan_pred",
               inputs = {"college_degree": False, "loan_amount": 6000},
               outputs = 0,
               feedback_id = {"loan_id": "00014"},
               timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
            )
                ...

        Args:
            inputs (dict): Inputs to the prediction. A dict where the keys are the feature names
                and the values are the feature values.
            outputs (Any): application output on the prediction.
            feedback_id (optional, Dict[str, Any]): A dictionary mapping string keys to values on
                which the feedback id is computed for matching prediction and feedback events.
                Should be the same as the argument `feedback_id` to
                :meth:`gantry.client.Gantry.log_feedback_event` for the matching feedback event.
            timestamp (optional, datetime.datetime): Specify a custom timestamp for the when the
                prediction occured. Useful for recording predictions from the past. If not
                specified, then the prediction timestamp defaults to when `log_prediction_event` was
                called.
            **kwargs: The rest of the arguments are the same as in
                :meth:`gantry.client.Gantry.instrument`.
        """
        warn(
            "Deprecated: this method will be soon deprecated. Use `log_record` instead",
            DeprecationWarning,
        )
        _check_sample_rate(sample_rate)
        if random.random() > sample_rate:
            return

        if not isinstance(inputs, dict):
            logger.error("inputs is not a dict.")
            return

        environment, context = self._get_env_and_context(tags)

        ev = _build_prediction_event(
            context,
            environment,
            inputs,
            outputs,
            application,
            version,
            feedback_keys,
            ignore_inputs,
            feedback_id=feedback_id,
            custom_timestamp=timestamp,
            tags=tags,
        )
        self.log_store.log(application, ev)

    @_log_exception
    @typechecked
    def log_predictions(
        self,
        application: str,
        inputs: Union[List[dict], pd.DataFrame],
        outputs: Union[List[dict], List[Any], pd.DataFrame],
        version: Optional[Union[int, str]] = None,
        feedback_keys: Optional[List[str]] = None,
        ignore_inputs: Optional[List[str]] = None,
        feedback_ids: Optional[List[dict]] = None,
        timestamps: Optional[Union[List[datetime.datetime], pd.DatetimeIndex]] = None,
        sort_on_timestamp: bool = True,
        sample_rate: float = 1.0,
        as_batch: bool = False,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        DEPRECATION WARNING:
        This method will be deprecated soon. Please use `log_records` instead.

        Endpoint for a batch version of :meth:`gantry.client.Gantry.log_prediction_event`.
        Allows for a list of predictions and registers them 1 at a time.

        Args:
            inputs (List[dict]): A list of prediction inputs. `inputs[i]` is a dict of the
                features for the i-th prediction to be logged.
            outputs (List[Any]): A list of prediction outputs. `outputs[i]` should be the
                application output for the prediction with features `inputs[i]`.
            timestamps (optional, List[datetime.datetime]): A list of prediction timestamps.
                If specified, `timestamps[i]` should be the timestamp for the i-th prediction.
                If timestamps = None (default), then the prediction timestamp defaults to the
                time when `log_predictions` is called.
            feedback_ids (optional, List[dict]): A list of prediction feedback ids. The i-th entry
                corresponds to the argument `feedback_id` in
                :meth:`gantry.client.Gantry.log_prediction_event` for the i-th prediction event.
            **kwargs: The rest of the arguments are the same as in
                :meth:`gantry.client.Gantry.instrument`.
        """
        warn(
            "Deprecated: this method will be soon deprecated. Use `log_records` instead",
            DeprecationWarning,
        )
        batch_id = None
        try:
            inputs = serializable_value(inputs)
            outputs = serializable_value(outputs)
            version = serializable_value(version) if version is not None else None

            if len(inputs) == len(outputs):
                if timestamps is not None and not len(timestamps) == len(inputs):
                    raise GantryLoggingException(
                        "timestamps don't have same length as inputs and outputs"
                    )
                if feedback_ids and not len(feedback_ids) == len(inputs):
                    raise GantryLoggingException(
                        "feedback_ids don't have same length as inputs and outputs"
                    )
                if version and isinstance(version, list) and not len(version) == len(inputs):
                    raise GantryLoggingException(
                        "if version is an array, it should have same length as inputs and outputs."
                        "Instead, version has length {} and inputs has length {}.".format(
                            len(version), len(inputs)
                        )
                    )

                environment, context = self._get_env_and_context(tags)

                timestamp_idx = _create_timestamp_idx(sort_on_timestamp, timestamps, len(inputs))

                events = _build_prediction_events(
                    application=application,
                    inputs=inputs,
                    outputs=outputs,
                    timestamp_idx=timestamp_idx,
                    context=context,
                    environment=environment,
                    tags=tags,
                    version=version,
                    feedback_keys=feedback_keys,
                    ignore_inputs=ignore_inputs,
                    feedback_ids=feedback_ids,
                    sample_rate=sample_rate,
                    batch_id=batch_id,
                )

                if events:
                    if as_batch:
                        self._upload_data_as_batch(
                            application, environment, version, events, BatchType.PREDICTION
                        )
                    else:
                        batch_id = None
                        self.log_store.log_batch(application, events)
                        _batch_success_msg(batch_id, application, self.log_store)
                else:
                    logger.info("No events to log")
            else:
                raise GantryLoggingException("Inputs and outputs list don't have same length.")
        except Exception as e:
            _batch_fail_msg(batch_id)

            raise e

    def _upload_data_as_batch(
        self,
        application: str,
        environment: str,
        version: Optional[Union[str, int]],
        events: List,
        batch_type: BatchType,
    ):
        data_link: DataLink = _build_data_link(
            application,
            environment=environment,
            version=version,
            events=events,
            batch_type=batch_type,
        )
        events_bytesize = sys.getsizeof(json.dumps(events, cls=EventEncoder).encode("utf-8"))
        batch_count = int(
            CHUNK_SIZE / (events_bytesize / data_link.num_events)
        )  # max file chunk size / average event size -> count of batch events to get to chunk.
        self._handle_upload(
            _build_batch_iterator(events, batch_count),
            data_link,
            events_bytesize,
            f"{application}_{uuid.uuid4()}",
        )

    @staticmethod
    def setup_logger(level="INFO"):
        if not level:
            return

        pkg_logger = logging.getLogger("gantry")
        pkg_logger.setLevel(level)

        existing_handlers = pkg_logger.handlers
        for handler in existing_handlers:
            if isinstance(handler, logging.StreamHandler):
                return
        formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        pkg_logger.addHandler(handler)
