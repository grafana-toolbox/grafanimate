#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
import time
from operator import attrgetter

from munch import munchify
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY

from grafanimate.grafana import GrafanaWrapper
from grafanimate.model import SequencingMode, AnimationSequence

logger = logging.getLogger(__name__)


class SequentialAnimation:

    def __init__(self, grafana: GrafanaWrapper, dashboard_uid=None, options=None):

        self.grafana = grafana
        self.dashboard_uid = dashboard_uid
        self.options = options or None

    def start(self):
        self.log('Opening dashboard')
        self.grafana.open_dashboard(self.dashboard_uid, options=self.options)
        self.log('Dashboard ready')

    def log(self, message):
        logger.info(message)
        self.grafana.console_info(message)

    def run(self, step: AnimationSequence):

        self.log("Starting animation: {}".format(step))

        # Destructure `step` instance.
        dtstart, dtuntil, interval, mode = attrgetter("dtstart", "dtuntil", "interval", "mode")(step)

        if dtstart > dtuntil:
            message = 'Timestamp dtstart={} is after dtuntil={}'.format(dtstart, dtuntil)
            raise ValueError(message)

        rr_freq, rr_interval, dtdelta = self.get_freq_delta(interval)

        #until = datetime.now()
        if mode == SequencingMode.CUMULATIVE:
            dtuntil += dtdelta

        # Compute complete date range.
        logger.info('Creating rrule: dtstart=%s, until=%s, freq=%s, interval=%s', dtstart, dtuntil, rr_freq, rr_interval)
        daterange = list(rrule(dtstart=dtstart, until=dtuntil, freq=rr_freq, interval=rr_interval))
        #logger.info('Date range is: %s', daterange)

        # Iterate date range.
        for date in daterange:

            logger.info("=" * 42)
            logger.info('Datetime step: %s', date)

            # Compute start and end dates based on mode.

            if mode == SequencingMode.WINDOW:
                dtstart = date
                dtuntil = date + dtdelta

            elif mode == SequencingMode.CUMULATIVE:
                dtuntil = date

            # Render image.
            image = self.render(dtstart, dtuntil, interval)

            # Build item model.
            item = munchify({
                'meta': {
                    'grafana': self.grafana,
                    'scenario': self.options["scenario"],
                    'dashboard': self.dashboard_uid,
                    'interval': interval,
                },
                'data': {
                    'dtstart': dtstart,
                    'dtuntil': dtuntil,
                    'image': image,
                },
            })

            yield item

            if self.options["exposure-time"] > 0:
                logger.info("Waiting for {} seconds (exposure time)".format(self.options["exposure-time"]))
                time.sleep(self.options["exposure-time"])

        self.log("Animation finished")

    def get_freq_delta(self, interval):

        rr_interval = 1

        # Secondly
        if interval == 'secondly':
            rr_freq = SECONDLY
            delta = timedelta(seconds=1)

        # Minutely
        elif interval == 'minutely':
            rr_freq = MINUTELY
            delta = timedelta(minutes=1) - timedelta(seconds=1)

        # Each 5 minutes
        elif interval == '5min':
            rr_freq = MINUTELY
            rr_interval = 5
            delta = timedelta(minutes=5) - timedelta(seconds=1)

        # Each 10 minutes
        elif interval == '10min':
            rr_freq = MINUTELY
            rr_interval = 10
            delta = timedelta(minutes=10) - timedelta(seconds=1)

        # Each 30 minutes
        elif interval == '30min':
            rr_freq = MINUTELY
            rr_interval = 30
            delta = timedelta(minutes=30) - timedelta(seconds=1)

        # Hourly
        elif interval == 'hourly':
            rr_freq = HOURLY
            delta = timedelta(hours=1) - timedelta(seconds=1)

        # Daily
        elif interval == 'daily':
            rr_freq = DAILY
            delta = timedelta(days=1) - timedelta(seconds=1)

        # Weekly
        elif interval == 'weekly':
            rr_freq = WEEKLY
            delta = timedelta(weeks=1) - timedelta(seconds=1)

        # Monthly
        elif interval == 'monthly':
            rr_freq = MONTHLY
            delta = relativedelta(months=+1) - relativedelta(seconds=1)

        # Yearly
        elif interval == 'yearly':
            rr_freq = YEARLY
            delta = relativedelta(years=+1) - relativedelta(seconds=1)

        else:
            raise ValueError('Unknown interval "{}"'.format(interval))

        return rr_freq, rr_interval, delta

    def render(self, dtstart, dtuntil, interval):

        logger.debug('Adjusting time range control')
        self.grafana.timewarp(dtstart, dtuntil, interval)

        logger.debug('Rendering image')
        return self.make_image()

    def make_image(self):
        image = self.grafana.render_image()
        #logger.info('Image size: %s', len(image))
        return image
