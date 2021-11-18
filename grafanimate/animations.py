#  -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import time
from datetime import timedelta
from operator import attrgetter
from typing import Tuple

from dateutil.relativedelta import relativedelta
from dateutil.rrule import (
    DAILY,
    HOURLY,
    MINUTELY,
    MONTHLY,
    SECONDLY,
    WEEKLY,
    YEARLY,
    rrule,
)
from munch import munchify
from pytimeparse2 import parse as parse_human_time

from grafanimate.grafana import GrafanaWrapper
from grafanimate.model import AnimationSequence, SequencingMode
from grafanimate.util import get_relativedelta

logger = logging.getLogger(__name__)


class SequentialAnimation:
    def __init__(self, grafana: GrafanaWrapper, dashboard_uid=None, options=None):

        self.grafana = grafana
        self.dashboard_uid = dashboard_uid
        self.options = options or None

    def start(self):
        self.log("Opening dashboard")
        self.grafana.open_dashboard(self.dashboard_uid, options=self.options)
        self.log("Dashboard ready")

    def log(self, message):
        logger.info(message)
        self.grafana.console_info(message)

    def run(self, step: AnimationSequence):

        self.log("Starting animation: {}".format(step))

        # Destructure `step` instance.
        start, stop, every, mode = attrgetter("start", "stop", "every", "mode")(step)

        if start > stop:
            message = "Timestamp start={} is after stop={}".format(start, stop)
            raise ValueError(message)

        rr_freq, rr_interval, dtdelta = self.get_freq_delta(every)

        # until = datetime.now()
        if mode == SequencingMode.CUMULATIVE:
            stop += dtdelta

        # Compute complete date range.
        logger.info("Creating rrule: dtstart=%s, until=%s, freq=%s, interval=%s", start, stop, rr_freq, rr_interval)
        daterange = list(rrule(dtstart=start, until=stop, freq=rr_freq, interval=rr_interval))
        # logger.info('Date range is: %s', daterange)

        # Iterate date range.
        for date in daterange:

            logger.info("=" * 42)
            logger.info("Datetime step: %s", date)

            # Compute start and end dates based on mode.

            if mode == SequencingMode.WINDOW:
                start = date
                stop = date + dtdelta

            elif mode == SequencingMode.CUMULATIVE:
                stop = date

            # Render image.
            image = self.render(start, stop, every)

            # Build item model.
            item = munchify(
                {
                    "meta": {
                        "grafana": self.grafana,
                        "scenario": self.options["scenario"],
                        "dashboard": self.dashboard_uid,
                        "every": every,
                    },
                    "data": {
                        "start": start,
                        "stop": stop,
                        "image": image,
                    },
                }
            )

            yield item

            if self.options["exposure-time"] > 0:
                logger.info("Waiting for {} seconds (exposure time)".format(self.options["exposure-time"]))
                time.sleep(self.options["exposure-time"])

        self.log("Animation finished")

    @staticmethod
    def get_freq_delta(interval: str) -> Tuple[int, int, timedelta]:

        rr_freq = MINUTELY
        rr_interval = 1

        # 1. Attempt to parse time using `pytimeparse` module.
        # https://pypi.org/project/pytimeparse/
        duration = parse_human_time(interval)
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

            return rr_freq, rr_interval, delta

        # 2. Compute parameters from specific labels, expression periods.

        # Secondly
        if interval == "secondly":
            rr_freq = SECONDLY
            delta = timedelta(seconds=1)

        # Minutely
        elif interval == "minutely":
            rr_freq = MINUTELY
            delta = timedelta(minutes=1) - timedelta(seconds=1)

        # Each 5 minutes
        elif interval == "5min":
            rr_freq = MINUTELY
            rr_interval = 5
            delta = timedelta(minutes=5) - timedelta(seconds=1)

        # Each 10 minutes
        elif interval == "10min":
            rr_freq = MINUTELY
            rr_interval = 10
            delta = timedelta(minutes=10) - timedelta(seconds=1)

        # Each 30 minutes
        elif interval == "30min":
            rr_freq = MINUTELY
            rr_interval = 30
            delta = timedelta(minutes=30) - timedelta(seconds=1)

        # Hourly
        elif interval == "hourly":
            rr_freq = HOURLY
            delta = timedelta(hours=1) - timedelta(seconds=1)

        # Daily
        elif interval == "daily":
            rr_freq = DAILY
            delta = timedelta(days=1) - timedelta(seconds=1)

        # Weekly
        elif interval == "weekly":
            rr_freq = WEEKLY
            delta = timedelta(weeks=1) - timedelta(seconds=1)

        # Monthly
        elif interval == "monthly":
            rr_freq = MONTHLY
            delta = relativedelta(months=+1) - relativedelta(seconds=1)

        # Yearly
        elif interval == "yearly":
            rr_freq = YEARLY
            delta = relativedelta(years=+1) - relativedelta(seconds=1)

        else:
            raise ValueError('Unknown interval "{}"'.format(interval))

        if isinstance(delta, timedelta):
            delta = get_relativedelta(seconds=delta.total_seconds())

        return rr_freq, rr_interval, delta

    def render(self, start, stop, every):

        logger.debug("Adjusting time range control")
        self.grafana.timewarp(start, stop, every)

        logger.debug("Rendering image")
        return self.make_image()

    def make_image(self):
        image = self.grafana.render_image()
        # logger.info('Image size: %s', len(image))
        return image
