import re
from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, MINUTELY
from dateutil.tz import tzutc
from freezegun import freeze_time

from grafanimate.model import AnimationScenario, AnimationSequence, SequencingMode
from grafanimate.timeutil import RecurrenceInfo


def test_sequence_datetime():
    seq = AnimationSequence(
        start=datetime(2021, 11, 14, 2, 0, 0),
        stop=datetime(2021, 11, 14, 2, 16, 36),
        every="5min",
    )

    assert seq.start == datetime(2021, 11, 14, 2, 0, 0)
    assert seq.stop == datetime(2021, 11, 14, 2, 16, 36)
    assert seq.mode == SequencingMode.WINDOW

    assert seq.recurrence.every == "5min"
    assert seq.recurrence.frequency == MINUTELY
    assert seq.recurrence.interval == 5
    assert seq.recurrence.duration == relativedelta(minutes=+5, seconds=-1)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-14T02:00:00/2021-11-14T02:04:59",
        "2021-11-14T02:05:00/2021-11-14T02:09:59",
        "2021-11-14T02:10:00/2021-11-14T02:14:59",
        "2021-11-14T02:15:00/2021-11-14T02:19:59",
    ]


def test_sequence_isodate():
    seq = AnimationSequence(
        start="2021-11-15T02:12:05Z",
        stop="2021-11-15T02:37:36Z",
        every="3min",
        mode=SequencingMode.CUMULATIVE,
    )

    assert seq.start == datetime(2021, 11, 15, 2, 12, 5, tzinfo=tzutc())
    assert seq.stop == datetime(2021, 11, 15, 2, 37, 36, tzinfo=tzutc())
    assert seq.mode == SequencingMode.CUMULATIVE

    assert seq.recurrence.every == "3min"
    assert seq.recurrence.frequency == MINUTELY
    assert seq.recurrence.interval == 3
    assert seq.recurrence.duration == relativedelta(minutes=+3, seconds=-1)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-15T02:12:05+00:00/2021-11-15T02:12:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:15:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:18:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:21:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:24:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:27:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:30:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:33:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:36:05+00:00",
        "2021-11-15T02:12:05+00:00/2021-11-15T02:39:05+00:00",
    ]


def test_sequence_epoch():
    seq = AnimationSequence(
        start=1637091011,
        stop=1637091911,
        every="4m5s",
        mode=SequencingMode.CUMULATIVE,
    )

    assert seq.start == datetime(2021, 11, 16, 19, 30, 11, tzinfo=timezone.utc)
    assert seq.stop == datetime(2021, 11, 16, 19, 45, 11, tzinfo=timezone.utc)
    assert seq.mode == SequencingMode.CUMULATIVE

    assert seq.recurrence.every == "4m5s"
    assert seq.recurrence.frequency == MINUTELY
    assert seq.recurrence.interval == 4
    assert seq.recurrence.duration == relativedelta(minutes=+4, seconds=+4)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-16T19:30:11+00:00/2021-11-16T19:30:11+00:00",
        "2021-11-16T19:30:11+00:00/2021-11-16T19:34:11+00:00",
        "2021-11-16T19:30:11+00:00/2021-11-16T19:38:11+00:00",
        "2021-11-16T19:30:11+00:00/2021-11-16T19:42:11+00:00",
        "2021-11-16T19:30:11+00:00/2021-11-16T19:46:11+00:00",
    ]


@freeze_time("2021-11-19T20:34:17Z")
def test_sequence_relative_to_now():
    seq = AnimationSequence(
        start="-30m",
        stop="+30m",
        every="8m",
    )

    assert seq.start == datetime(2021, 11, 19, 20, 4, 17, tzinfo=tzutc())
    assert seq.stop == datetime(2021, 11, 19, 21, 4, 17, tzinfo=tzutc())

    assert seq.recurrence.every == "8m"
    assert seq.recurrence.frequency == MINUTELY
    assert seq.recurrence.interval == 8
    assert seq.recurrence.duration == relativedelta(minutes=+8, seconds=-1)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-19T20:04:17+00:00/2021-11-19T20:12:16+00:00",
        "2021-11-19T20:12:17+00:00/2021-11-19T20:20:16+00:00",
        "2021-11-19T20:20:17+00:00/2021-11-19T20:28:16+00:00",
        "2021-11-19T20:28:17+00:00/2021-11-19T20:36:16+00:00",
        "2021-11-19T20:36:17+00:00/2021-11-19T20:44:16+00:00",
        "2021-11-19T20:44:17+00:00/2021-11-19T20:52:16+00:00",
        "2021-11-19T20:52:17+00:00/2021-11-19T21:00:16+00:00",
        "2021-11-19T21:00:17+00:00/2021-11-19T21:08:16+00:00",
    ]


@freeze_time("2021-11-19T20:34:17Z")
def test_sequence_relative_to_start():
    seq = AnimationSequence(
        start="-14d",
        stop="start+7d",
        every="1d",
    )

    assert seq.start == datetime(2021, 11, 5, 20, 34, 17, tzinfo=tzutc())
    assert seq.stop == datetime(2021, 11, 12, 20, 34, 17, tzinfo=tzutc())

    assert seq.recurrence.every == "1d"
    assert seq.recurrence.frequency == DAILY
    assert seq.recurrence.interval == 1
    assert seq.recurrence.duration == relativedelta(days=+1, seconds=-1)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-05T20:34:17+00:00/2021-11-06T20:34:16+00:00",
        "2021-11-06T20:34:17+00:00/2021-11-07T20:34:16+00:00",
        "2021-11-07T20:34:17+00:00/2021-11-08T20:34:16+00:00",
        "2021-11-08T20:34:17+00:00/2021-11-09T20:34:16+00:00",
        "2021-11-09T20:34:17+00:00/2021-11-10T20:34:16+00:00",
        "2021-11-10T20:34:17+00:00/2021-11-11T20:34:16+00:00",
        "2021-11-11T20:34:17+00:00/2021-11-12T20:34:16+00:00",
        "2021-11-12T20:34:17+00:00/2021-11-13T20:34:16+00:00",
    ]


@freeze_time("2021-11-19T20:34:17Z")
def test_sequence_relative_with_now():
    seq = AnimationSequence(
        start="-7d",
        stop="now",
        every="1d",
    )

    assert seq.start == datetime(2021, 11, 12, 20, 34, 17, tzinfo=tzutc())
    assert seq.stop == datetime(2021, 11, 19, 20, 34, 17, tzinfo=tzutc())

    assert seq.recurrence.every == "1d"
    assert seq.recurrence.frequency == DAILY
    assert seq.recurrence.interval == 1
    assert seq.recurrence.duration == relativedelta(days=+1, seconds=-1)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-12T20:34:17+00:00/2021-11-13T20:34:16+00:00",
        "2021-11-13T20:34:17+00:00/2021-11-14T20:34:16+00:00",
        "2021-11-14T20:34:17+00:00/2021-11-15T20:34:16+00:00",
        "2021-11-15T20:34:17+00:00/2021-11-16T20:34:16+00:00",
        "2021-11-16T20:34:17+00:00/2021-11-17T20:34:16+00:00",
        "2021-11-17T20:34:17+00:00/2021-11-18T20:34:16+00:00",
        "2021-11-18T20:34:17+00:00/2021-11-19T20:34:16+00:00",
        "2021-11-19T20:34:17+00:00/2021-11-20T20:34:16+00:00",
    ]


@freeze_time("2021-11-19T20:34:17Z")
def test_sequence_recurrence():
    seq = AnimationSequence(
        start="-7d",
        stop="now",
        recurrence=RecurrenceInfo(
            frequency=DAILY, interval=1, duration=relativedelta(days=+1, seconds=-1)
        ),
    )

    assert seq.start == datetime(2021, 11, 12, 20, 34, 17, tzinfo=tzutc())
    assert seq.stop == datetime(2021, 11, 19, 20, 34, 17, tzinfo=tzutc())

    assert seq.recurrence.every is None
    assert seq.recurrence.frequency == DAILY
    assert seq.recurrence.interval == 1
    assert seq.recurrence.duration == relativedelta(days=+1, seconds=-1)

    assert list(seq.get_timeranges_isoformat()) == [
        "2021-11-12T20:34:17+00:00/2021-11-13T20:34:16+00:00",
        "2021-11-13T20:34:17+00:00/2021-11-14T20:34:16+00:00",
        "2021-11-14T20:34:17+00:00/2021-11-15T20:34:16+00:00",
        "2021-11-15T20:34:17+00:00/2021-11-16T20:34:16+00:00",
        "2021-11-16T20:34:17+00:00/2021-11-17T20:34:16+00:00",
        "2021-11-17T20:34:17+00:00/2021-11-18T20:34:16+00:00",
        "2021-11-18T20:34:17+00:00/2021-11-19T20:34:16+00:00",
        "2021-11-19T20:34:17+00:00/2021-11-20T20:34:16+00:00",
    ]


def test_sequence_needs_recurrence_or_every():
    with pytest.raises(ValueError) as ex:
        AnimationSequence(
            start="-7d",
            stop="now",
        )
    assert ex.match("Parameter `every` is mandatory when `recurrence` is not given")


@freeze_time("2021-11-19T20:34:17Z")
def test_sequence_start_greater_than_stop():
    with pytest.raises(ValueError) as ex:
        AnimationSequence(
            start="+1d",
            stop="-1d",
            every="10m",
        )
    assert ex.match(
        re.escape(
            "Timestamp start=2021-11-20T20:34:17+00:00 is after stop=2021-11-18T20:34:17+00:00"
        )
    )


def test_scenario_basic():
    scenario = AnimationScenario(
        grafana_url="https://daq.example.org/grafana/",
        dashboard_uid="foobar",
        sequences=[
            AnimationSequence(
                start="2021-11-14T15:20:05Z",
                stop="2021-11-14T15:45:36Z",
                every="5min",
                mode=SequencingMode.WINDOW,
            ),
            AnimationSequence(
                start="2021-11-15T02:12:05Z",
                stop="2021-11-15T02:37:36Z",
                every="3 minutes 2 seconds",
                mode=SequencingMode.CUMULATIVE,
            ),
        ],
    )

    assert len(scenario.sequences) == 2
