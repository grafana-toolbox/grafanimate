# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
from datetime import datetime, timedelta, timezone

from datetime_interval import Interval

"""
**********************************************
Improving time range control for "grafanimate"
**********************************************

Introduction
============
- https://community.hiveeyes.org/t/improving-time-range-control-for-grafanimate/1783/13
- https://en.wikipedia.org/wiki/Dope_sheet
- https://en.wikipedia.org/wiki/Exposure_sheet
- https://en.wikipedia.org/wiki/Animation#Stop_motion_animation

Running
=======
::

    python grafanimate/timecontrol.py

Backlog
=======
- Use datetime parser::

    from dateutil import parser

- Investigate NumPy
    - https://docs.scipy.org/doc/numpy/reference/arrays.datetime.html
    - https://jakevdp.github.io/PythonDataScienceHandbook/03.11-working-with-time-series.html

- Investigate Pandas
    - http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Period.html
    - http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.PeriodIndex.html
    - https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    - https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#time-span-representation
    - https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html
    - http://www.marcelscharth.com/python/time.html

    - That's nice:
        - https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#custom-frequency-ranges
        - http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.period_range.html#pandas.period_range
"""


class SlidingPeriodicInterval:
    def __init__(self, start, stop, every):
        self.start = start
        self.stop = stop
        self.every = every

    def __iter__(self):
        cursor = Interval(start=self.start, duration=self.every)
        yield cursor

        while cursor.end < self.stop:
            cursor += self.every
            yield cursor


class CumulativePeriodicInterval:
    def __init__(self, start, stop, every):
        self.start = start
        self.stop = stop
        self.every = every

    def __iter__(self):
        cursor = Interval(start=self.start, duration=self.every)
        yield cursor

        while cursor.end < self.stop:
            cursor.end += self.every
            yield cursor


def print_intervals(intervals):
    for interval in intervals:
        print(f"{interval.start} - {interval.end}")  # noqa: T201


def print_header(title):
    print()  # noqa: T201
    print("#", title)  # noqa: T201


def create_dope_sheet_blueprint():
    now = datetime.now(tz=timezone.utc)
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)

    print_header("Sliding forward")
    intervals = SlidingPeriodicInterval(
        start=yesterday,
        stop=tomorrow,
        every=timedelta(days=1),
    )
    print_intervals(intervals)

    # Just reversing the list of intervals yields deterministic results as it is literally
    # just the opposite of sliding forward without any different computation involved.
    print_header("Sliding reverse")
    intervals = SlidingPeriodicInterval(
        start=yesterday,
        stop=tomorrow,
        every=timedelta(days=1),
    )
    print_intervals(reversed(list(intervals)))

    print_header("Cumulative I (unaligned)")
    intervals = CumulativePeriodicInterval(
        start=yesterday,
        stop=tomorrow,
        every=timedelta(days=1),
    )
    print_intervals(intervals)

    print_header("Cumulative II (aligned)")
    now_aligned_to_hour = now - timedelta(
        minutes=now.minute,
        seconds=now.second,
        microseconds=now.microsecond,
    )
    intervals = CumulativePeriodicInterval(
        start=now_aligned_to_hour,
        stop=now_aligned_to_hour + timedelta(hours=2),
        every=timedelta(minutes=15),
    )
    print_intervals(intervals)


if __name__ == "__main__":
    create_dope_sheet_blueprint()
