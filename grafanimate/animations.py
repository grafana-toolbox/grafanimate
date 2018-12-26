#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
from munch import munchify
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY

from grafanimate.grafana import GrafanaWrapper

logger = logging.getLogger(__name__)


class SequentialAnimation:

    def __init__(self, grafana_url=None, dashboard_uid=None, time_start=None, time_end=None, time_step=None):

        self.grafana_url = grafana_url
        self.dashboard_uid = dashboard_uid

        self.time_start = time_start
        # TODO: Default to "now()"
        self.time_end = time_end
        self.time_step = time_step

        self.grafana = GrafanaWrapper(grafana_url=self.grafana_url)
        self.grafana.boot_firefox(headless=False)
        self.grafana.boot_grafana()

    def start(self):

        logger.info('Opening dashboard')
        self.grafana.open_dashboard(self.dashboard_uid)
        logger.info('Dashboard ready')

    def run(self, dtstart=None, dtuntil=None, interval=None):

        if dtstart > dtuntil:
            message = 'Timestamp dtstart={} is after dtuntil={}'.format(dtstart, dtuntil)
            raise ValueError(message)

        #flavor = 'expand'
        flavor = 'window'

        freq, delta = self.get_freq_delta(interval)

        #until = datetime.now()
        if flavor == 'expand':
            dtuntil += delta

        # Compute complete date range.
        logger.info('Creating rrule: dtstart=%s, until=%s, freq=%s', dtstart, dtuntil, freq)
        daterange = list(rrule(dtstart=dtstart, until=dtuntil, freq=freq))
        #logger.info('Date range is: %s', daterange)

        # Iterate date range.
        for date in daterange:

            logger.info('Datetime step: %s', date)

            # Compute start and end dates based on flavor.

            if flavor == 'window':
                dtstart = date
                dtuntil = date + delta

            elif flavor == 'expand':
                dtuntil = date

            # Render image.
            image = self.render(dtstart, dtuntil, interval)

            # Build item model.
            item = munchify({
                'meta': {
                    'grafana': self.grafana_url,
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

    def get_freq_delta(self, interval):

        # Second
        if interval == 'secondly':
            freq = SECONDLY
            delta = timedelta(seconds=1)

        # Minute
        elif interval == 'minutely':
            freq = MINUTELY
            delta = timedelta(minutes=1) - timedelta(seconds=1)

        # Hourly
        elif interval == 'hourly':
            freq = HOURLY
            delta = timedelta(hours=1) - timedelta(seconds=1)

        # Daily
        elif interval == 'daily':
            freq = DAILY
            delta = timedelta(days=1) - timedelta(seconds=1)

        # Weekly
        elif interval == 'weekly':
            freq = WEEKLY
            delta = timedelta(weeks=1) - timedelta(seconds=1)

        # Monthly
        elif interval == 'monthly':
            freq = MONTHLY
            delta = relativedelta(months=+1) - relativedelta(seconds=1)

        # Yearly
        elif interval == 'yearly':
            freq = YEARLY
            delta = relativedelta(years=+1) - relativedelta(seconds=1)

        else:
            raise ValueError('Unknown interval "{}"'.format(interval))

        return freq, delta

    def render(self, dtstart, dtuntil, interval):

        logger.debug('Adjusting time range control')
        self.grafana.timewarp(dtstart, dtuntil, interval)

        logger.debug('Rendering image')
        return self.make_image()

    def make_image(self):
        image = self.grafana.render_image()
        #logger.info('Image size: %s', len(image))
        return image
