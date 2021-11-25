from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, HOURLY, MINUTELY, MONTHLY, SECONDLY, WEEKLY, YEARLY

from grafanimate.timeutil import get_freq_delta


def test_freq_delta_legacy():

    recurrence = get_freq_delta("secondly")
    assert recurrence.frequency == SECONDLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(seconds=+1)

    recurrence = get_freq_delta("minutely")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(seconds=+59)

    recurrence = get_freq_delta("5min")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 5
    assert recurrence.duration == relativedelta(minutes=+5, seconds=-1)

    recurrence = get_freq_delta("10min")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 10
    assert recurrence.duration == relativedelta(minutes=+10, seconds=-1)

    recurrence = get_freq_delta("30min")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 30
    assert recurrence.duration == relativedelta(minutes=+30, seconds=-1)

    recurrence = get_freq_delta("hourly")
    assert recurrence.frequency == HOURLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(minutes=+59, seconds=+59)

    recurrence = get_freq_delta("daily")
    assert recurrence.frequency == DAILY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(hours=+23, minutes=+59, seconds=+59)

    recurrence = get_freq_delta("weekly")
    assert recurrence.frequency == WEEKLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(days=+6, hours=+23, minutes=+59, seconds=+59)

    recurrence = get_freq_delta("monthly")
    assert recurrence.frequency == MONTHLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(months=+1, seconds=-1)

    recurrence = get_freq_delta("yearly")
    assert recurrence.frequency == YEARLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(years=+1, seconds=-1)


def test_freq_delta_pytimeparse():

    recurrence = get_freq_delta("1s")
    assert recurrence.frequency == SECONDLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(seconds=+1)

    recurrence = get_freq_delta("30s")
    assert recurrence.frequency == SECONDLY
    assert recurrence.interval == 30
    assert recurrence.duration == relativedelta(seconds=+30)

    recurrence = get_freq_delta("1m")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(minutes=+1, seconds=-1)

    recurrence = get_freq_delta("2m30s")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 2
    assert recurrence.duration == relativedelta(minutes=+2, seconds=29)

    recurrence = get_freq_delta("30m")
    assert recurrence.frequency == MINUTELY
    assert recurrence.interval == 30
    assert recurrence.duration == relativedelta(minutes=+30, seconds=-1)

    recurrence = get_freq_delta("1h")
    assert recurrence.frequency == HOURLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(hours=+1, seconds=-1)

    recurrence = get_freq_delta("12h")
    assert recurrence.frequency == HOURLY
    assert recurrence.interval == 12
    assert recurrence.duration == relativedelta(hours=+12, seconds=-1)

    recurrence = get_freq_delta("1d")
    assert recurrence.frequency == DAILY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(days=+1, seconds=-1)

    recurrence = get_freq_delta("1d12h")
    assert recurrence.frequency == DAILY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(days=+1, hours=+12, seconds=-1)

    recurrence = get_freq_delta("1.5 days")
    assert recurrence.frequency == DAILY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(days=+1, hours=+12, seconds=-1)

    recurrence = get_freq_delta("1w")
    assert recurrence.frequency == DAILY
    assert recurrence.interval == 7
    assert recurrence.duration == relativedelta(days=+7, seconds=-1)

    recurrence = get_freq_delta("1mo")
    assert recurrence.frequency == MONTHLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(months=+1, seconds=-1)

    recurrence = get_freq_delta("1y")
    assert recurrence.frequency == YEARLY
    assert recurrence.interval == 1
    assert recurrence.duration == relativedelta(years=+1, seconds=-1)

    recurrence = get_freq_delta("3 years 5 months")
    assert recurrence.frequency == YEARLY
    assert recurrence.interval == 3
    assert recurrence.duration == relativedelta(years=+3, months=+5, seconds=-1)
