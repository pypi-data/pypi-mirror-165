import datetime

import pytest
from freezegun import freeze_time

from gantry.utils import _is_offset_naive, check_event_time_in_future

CURRENT_TIME = datetime.datetime(2022, 5, 23, 0, 0, 0)
CLOSE_CURRENT_TIME = datetime.datetime(2022, 5, 23, 1, 0, 0)
FUTURE_TIME = datetime.datetime(2042, 5, 23, 0, 0, 0)
SOME_TIME = datetime.datetime(2022, 5, 10, 17, 50, 32)
ANOTHER_TIME = datetime.datetime(2022, 5, 11, 17, 50, 32)

SOME_TIMEDELTA = datetime.timedelta(hours=-5)
SOME_TIMEZONE = datetime.timezone(SOME_TIMEDELTA)


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize(
    "timestamp",
    [
        FUTURE_TIME,
        FUTURE_TIME.astimezone(datetime.timezone.utc),
        CLOSE_CURRENT_TIME,
        CLOSE_CURRENT_TIME.astimezone(SOME_TIMEZONE),
    ],
)
def test_check_event_time_in_future(timestamp):
    """All passed timestamps will be assumed UTC"""
    assert check_event_time_in_future(timestamp) is True


@freeze_time(CURRENT_TIME)
@pytest.mark.parametrize(
    "timestamp", [SOME_TIME, ANOTHER_TIME, ANOTHER_TIME.astimezone(SOME_TIMEZONE)]
)
def test_check_event_time_in_past(timestamp):
    """All passed timestamps will be assumed UTC"""
    assert check_event_time_in_future(timestamp) is False


@pytest.mark.parametrize(
    ["timestamp", "expected"],
    [
        (CURRENT_TIME, True),
        (FUTURE_TIME, True),
        (CURRENT_TIME.astimezone(datetime.timezone.utc), False),
        (FUTURE_TIME.astimezone(), False),
        (ANOTHER_TIME.astimezone(SOME_TIMEZONE), False),
    ],
)
def test_is_offset_naive(timestamp, expected):
    assert _is_offset_naive(timestamp) is expected
