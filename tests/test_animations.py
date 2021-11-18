from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, HOURLY, MINUTELY, MONTHLY, SECONDLY, WEEKLY, YEARLY

from grafanimate.animations import SequentialAnimation


def test_freq_delta_legacy():

    get_freq_delta = SequentialAnimation.get_freq_delta

    freq, interval, delta = get_freq_delta("secondly")
    assert freq == SECONDLY
    assert interval == 1
    assert delta == relativedelta(seconds=+1)

    freq, interval, delta = get_freq_delta("minutely")
    assert freq == MINUTELY
    assert interval == 1
    assert delta == relativedelta(seconds=+59)

    freq, interval, delta = get_freq_delta("5min")
    assert freq == MINUTELY
    assert interval == 5
    assert delta == relativedelta(minutes=+5, seconds=-1)

    freq, interval, delta = get_freq_delta("10min")
    assert freq == MINUTELY
    assert interval == 10
    assert delta == relativedelta(minutes=+10, seconds=-1)

    freq, interval, delta = get_freq_delta("30min")
    assert freq == MINUTELY
    assert interval == 30
    assert delta == relativedelta(minutes=+30, seconds=-1)

    freq, interval, delta = get_freq_delta("hourly")
    assert freq == HOURLY
    assert interval == 1
    assert delta == relativedelta(minutes=+59, seconds=+59)

    freq, interval, delta = get_freq_delta("daily")
    assert freq == DAILY
    assert interval == 1
    assert delta == relativedelta(hours=+23, minutes=+59, seconds=+59)

    freq, interval, delta = get_freq_delta("weekly")
    assert freq == WEEKLY
    assert interval == 1
    assert delta == relativedelta(days=+6, hours=+23, minutes=+59, seconds=+59)

    freq, interval, delta = get_freq_delta("monthly")
    assert freq == MONTHLY
    assert interval == 1
    assert delta == relativedelta(months=+1, seconds=-1)

    freq, interval, delta = get_freq_delta("yearly")
    assert freq == YEARLY
    assert interval == 1
    assert delta == relativedelta(years=+1, seconds=-1)


def test_freq_delta_pytimeparse():

    get_freq_delta = SequentialAnimation.get_freq_delta

    freq, interval, delta = get_freq_delta("1s")
    assert freq == SECONDLY
    assert interval == 1
    assert delta == relativedelta(seconds=+1)

    freq, interval, delta = get_freq_delta("30s")
    assert freq == SECONDLY
    assert interval == 30
    assert delta == relativedelta(seconds=+30)

    freq, interval, delta = get_freq_delta("1m")
    assert freq == MINUTELY
    assert interval == 1
    assert delta == relativedelta(minutes=+1, seconds=-1)

    freq, interval, delta = get_freq_delta("2m30s")
    assert freq == MINUTELY
    assert interval == 2
    assert delta == relativedelta(minutes=+2, seconds=29)

    freq, interval, delta = get_freq_delta("30m")
    assert freq == MINUTELY
    assert interval == 30
    assert delta == relativedelta(minutes=+30, seconds=-1)

    freq, interval, delta = get_freq_delta("1h")
    assert freq == HOURLY
    assert interval == 1
    assert delta == relativedelta(hours=+1, seconds=-1)

    freq, interval, delta = get_freq_delta("12h")
    assert freq == HOURLY
    assert interval == 12
    assert delta == relativedelta(hours=+12, seconds=-1)

    freq, interval, delta = get_freq_delta("1d")
    assert freq == DAILY
    assert interval == 1
    assert delta == relativedelta(days=+1, seconds=-1)

    freq, interval, delta = get_freq_delta("1d12h")
    assert freq == DAILY
    assert interval == 1
    assert delta == relativedelta(days=+1, hours=+12, seconds=-1)

    freq, interval, delta = get_freq_delta("1.5 days")
    assert freq == DAILY
    assert interval == 1
    assert delta == relativedelta(days=+1, hours=+12, seconds=-1)

    freq, interval, delta = get_freq_delta("1w")
    assert freq == DAILY
    assert interval == 7
    assert delta == relativedelta(days=+7, seconds=-1)

    """
    freq, interval, delta = get_freq_delta("1mo")
    assert freq == MONTHLY
    assert interval == 1
    assert delta == relativedelta(months=+1, seconds=-1)

    freq, interval, delta = get_freq_delta("1y")
    assert freq == YEARLY
    assert interval == 1
    assert delta == relativedelta(years=+1, seconds=-1)
    """
