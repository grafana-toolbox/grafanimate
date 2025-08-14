# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional, Union

import dateutil.parser
from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, HOURLY, MINUTELY, MONTHLY, SECONDLY, WEEKLY, YEARLY
from pytimeparse2 import parse as parse_human_time


@dataclasses.dataclass
class RecurrenceInfo:
    """
    For feeding data to `dateutil.rrule.rrule`.
    """

    # One of `rrules`s DAILY, HOURLY, ...
    frequency: Literal[0, 1, 2, 3, 4, 5, 6]

    # The segment duration in seconds.
    interval: int

    # The segment duration, expressed as `relativedelta`.
    duration: relativedelta

    # Original interval/windowing label.
    every: Optional[str] = None


@dataclasses.dataclass
class Timerange:
    start: datetime
    stop: datetime
    recurrence: RecurrenceInfo


def get_freq_delta(every: str) -> RecurrenceInfo:
    rr_freq: Literal[0, 1, 2, 3, 4, 5, 6] = MINUTELY
    rr_interval = 1

    # 1. Attempt to parse time using `pytimeparse` module.
    # https://pypi.org/project/pytimeparse/
    duration = parse_human_time(every)
    if duration:
        delta = get_relativedelta(seconds=duration)

        if delta.years:
            rr_freq = YEARLY
            rr_interval = delta.years
        elif delta.months:
            rr_freq = MONTHLY
            rr_interval = delta.months
        elif delta.days:
            rr_freq = DAILY
            rr_interval = delta.days
        elif delta.hours:
            rr_freq = HOURLY
            rr_interval = delta.hours
        elif delta.minutes:
            rr_freq = MINUTELY
            rr_interval = delta.minutes
        else:
            rr_freq = SECONDLY
            rr_interval = delta.seconds

        if rr_freq != SECONDLY:
            delta -= relativedelta(seconds=1)

        return RecurrenceInfo(
            every=every,
            frequency=rr_freq,
            interval=rr_interval,
            duration=delta,
        )

    # 2. Compute parameters from specific labels, expression periods.

    # Secondly
    if every == "secondly":
        rr_freq = SECONDLY
        delta = timedelta(seconds=1)

    # Minutely
    elif every == "minutely":
        rr_freq = MINUTELY
        delta = timedelta(minutes=1) - timedelta(seconds=1)

    # Each 5 minutes
    elif every == "5min":
        rr_freq = MINUTELY
        rr_interval = 5
        delta = timedelta(minutes=5) - timedelta(seconds=1)

    # Each 10 minutes
    elif every == "10min":
        rr_freq = MINUTELY
        rr_interval = 10
        delta = timedelta(minutes=10) - timedelta(seconds=1)

    # Each 30 minutes
    elif every == "30min":
        rr_freq = MINUTELY
        rr_interval = 30
        delta = timedelta(minutes=30) - timedelta(seconds=1)

    # Hourly
    elif every == "hourly":
        rr_freq = HOURLY
        delta = timedelta(hours=1) - timedelta(seconds=1)

    # Daily
    elif every == "daily":
        rr_freq = DAILY
        delta = timedelta(days=1) - timedelta(seconds=1)

    # Weekly
    elif every == "weekly":
        rr_freq = WEEKLY
        delta = timedelta(weeks=1) - timedelta(seconds=1)

    # Monthly
    elif every == "monthly":
        rr_freq = MONTHLY
        delta = relativedelta(months=+1) - relativedelta(seconds=1)

    # Yearly
    elif every == "yearly":
        rr_freq = YEARLY
        delta = relativedelta(years=+1) - relativedelta(seconds=1)

    else:
        raise ValueError(f'Unknown interval "{every}"')

    if isinstance(delta, timedelta):
        delta = get_relativedelta(seconds=int(delta.total_seconds()))

    return RecurrenceInfo(
        every=every,
        frequency=rr_freq,
        interval=rr_interval,
        duration=delta,
    )


def get_relativedelta(seconds: int):
    # TODO: Add to `pytimeparse2`?
    # https://stackoverflow.com/questions/16977768/elegant-way-to-convert-python-datetime-timedelta-to-dateutil-relativedelta

    seconds_in = {
        "year": 365 * 24 * 60 * 60,
        "month": 30 * 24 * 60 * 60,
        "day": 24 * 60 * 60,
        "hour": 60 * 60,
        "minute": 60,
    }

    years, rem = divmod(seconds, seconds_in["year"])
    months, rem = divmod(rem, seconds_in["month"])
    days, rem = divmod(rem, seconds_in["day"])
    hours, rem = divmod(rem, seconds_in["hour"])
    minutes, rem = divmod(rem, seconds_in["minute"])
    seconds = rem

    return relativedelta(
        years=years,
        months=months,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    ).normalized()


def format_date_filename(date, every=None):  # noqa: ARG001
    # pattern = '%Y-%m-%d'
    pattern = "%Y-%m-%dT%H-%M-%S"
    # if every in ['secondly', 'minutely', 'hourly']:
    #    pattern = '%Y-%m-%dT%H-%M-%S'
    date_formatted = date.strftime(pattern)
    return date_formatted


def format_date_grafana(date: datetime, recurrence: RecurrenceInfo):
    pattern = "%Y-%m-%d"
    if recurrence.frequency in [SECONDLY, MINUTELY, HOURLY]:
        pattern = "%Y-%m-%dT%H:%M:%SZ"
    date_formatted = date.strftime(pattern)
    return date_formatted


def convert_absolute_timestamp(value: Union[datetime, str, int]) -> datetime:
    """
    Read and convert absolute timestamps.
    """
    if isinstance(value, datetime):
        pass
    elif isinstance(value, int):
        value = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        value = dateutil.parser.parse(value)
    else:
        raise TypeError(
            f"Unknown data type for `start` or `stop` value: {value} ({type(value)})",
        )
    return value


def convert_input_timestamp(
    value: Union[datetime, str, int],
    relative_to: Optional[datetime] = None,
) -> datetime:
    """
    Read and convert absolute or relative (humanized) timestamps.
    """
    if isinstance(value, str):
        if value == "now":
            return datetime.now(tz=timezone.utc)
        try:
            delta = parse_human_time(value)
            if not delta:
                raise ValueError(f"Unable to parse {value}")
            if not relative_to:
                raise ValueError("relative_to not given or empty")
            return relative_to + timedelta(seconds=delta)
        except ValueError as ex:
            if "Unable to parse" not in str(ex):
                raise

    return convert_absolute_timestamp(value)
