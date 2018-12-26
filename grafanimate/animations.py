#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
from datetime import timedelta

import shutil

import os
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, HOURLY, DAILY, WEEKLY, MONTHLY
from grafanimate.grafana import GrafanaWrapper

logger = logging.getLogger(__name__)


class SequentialAnimation:

    def __init__(self, grafana_url=None, dashboard_uid=None, time_start=None, time_end=None, time_step=None):

        self.dashboard_uid = dashboard_uid

        self.time_start = time_start
        # TODO: Default to "now()"
        self.time_end = time_end
        self.time_step = time_step

        self.grafana = GrafanaWrapper(grafana_url=grafana_url)
        self.grafana.boot_firefox(headless=False)
        self.grafana.boot_grafana()

    def start(self):

        logger.info('Opening dashboard')
        self.grafana.open_dashboard(self.dashboard_uid)
        logger.info('Dashboard ready')

    def run(self, dtstart=None, dtuntil=None, interval=None):

        #flavor = 'expand'
        flavor = 'window'

        freq, delta = self.get_freq_delta(interval)

        #until = datetime.now()
        if flavor == 'expand':
            dtuntil += delta

        # Compute complete date range.
        daterange = list(rrule(dtstart=dtstart, until=dtuntil, freq=freq))

        # Iterate date range.
        for date in daterange:

            # Compute start and end dates based on flavor.

            if flavor == 'window':
                start_date_formatted = format_date(date, interval)
                end_date_formatted = format_date(date + delta, interval)

            elif flavor == 'expand':
                start_date_formatted = format_date(dtstart, interval)
                end_date_formatted = format_date(date, interval)

            # Render image.
            image = self.render(start_date_formatted, end_date_formatted)

            # Compute image sequence file name.
            imagefile = './var/spool/{uid}/{uid}_{date}.png'.format(
                interval=interval,
                uid=self.dashboard_uid,
                date=start_date_formatted)

            # Ensure directory exists.
            directory = os.path.dirname(imagefile)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Store image.
            with open(imagefile, 'w') as f:
                f.write(image)

            logger.info('Saved frame to {}. Size: {}'.format(imagefile, len(image)))

    def get_freq_delta(self, interval):

        # Hourly
        if interval == 'hourly':
            freq = HOURLY
            delta = timedelta(hours=1)

        # Daily
        elif interval == 'daily':
            freq = DAILY
            delta = timedelta(days=1)

        # Weekly
        elif interval == 'weekly':
            freq = WEEKLY
            delta = timedelta(weeks=1)

        # Monthly
        elif interval == 'monthly':
            freq = MONTHLY
            #delta = timedelta(month=1)
            delta = relativedelta(months=+1)

        return freq, delta

    def render(self, date_begin, date_end):

        logger.debug('Adjusting time range control')
        self.grafana.timewarp(date_begin, date_end)

        logger.debug('Rendering image')
        return self.make_image()

    def make_image(self):
        image = self.grafana.render_image()
        #logger.info('Image size: %s', len(image))
        return image


def format_date(date, interval=None):
    pattern = '%Y-%m-%d'
    if interval == 'hourly':
        pattern = '%Y-%m-%dT%H:%M:%S'
    date_formatted = date.strftime(pattern)
    return date_formatted