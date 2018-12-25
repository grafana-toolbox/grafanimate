#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import time
import base64
import logging
from urllib import urlencode
from collections import OrderedDict
from datetime import datetime, timedelta

from dateutil.rrule import rrule, DAILY
from marionette_driver import Wait

from grafanimate.marionette import FirefoxMarionetteBase


logger = logging.getLogger(__name__)


class GrafanaWrapper(FirefoxMarionetteBase):
    """
    https://marionette-client.readthedocs.io/en/master/interactive.html
    """

    def wait_for_map(self):
        """
        Wait for map element <panel-plugin-grafana-worldmap-panel ...> to appear.
        """
        logger.debug('Waiting for map element to appear in DOM')
        self.waiter = Wait(self.marionette, timeout=15.0, interval=1.0)
        element = self.waiter.until(lambda m: self.get_map())
        logger.info('Finished waiting for map element')
        logger.info(element)
        return element

    def get_map(self):
        """
        Get map element <panel-plugin-grafana-worldmap-panel ...> from HTML DOM.
        """
        return self.find_tag("panel-plugin-grafana-worldmap-panel")

    def navigate_dashboard(self, url):

        # Navigate to resource URL.
        self.marionette.navigate(url)

        # Wait for map to be loaded.
        self.wait_for_map()

    def map_image(self):

        # Return screenshot from element.
        element = self.get_map()
        image_base64 = self.marionette.screenshot(element=element)

        # Decode from base64 format.
        image = base64.b64decode(image_base64)

        return image

    def timerange_set(self, starttime, endtime):
        """
        """

        # https://stackoverflow.com/questions/48264279/how-to-set-time-range-in-grafana-dashboard-from-text-panels/52492205#52492205
        javascript = """
            timeSrv = angular.element('grafana-app').injector().get('timeSrv');
            timeSrv.setTime({{from: "{}", to: "{}"}});
            return true;
        """.format(starttime, endtime)

        # https://github.com/mozilla/geckodriver/issues/1067#issuecomment-347180427
        # https://github.com/devtools-html/har-export-trigger/issues/27#issuecomment-424777524
        status = self.run_javascript(javascript)
        if status == True:
            logger.debug('Setting time range control succeeded')
        else:
            message = 'Setting time range control to (start={}, end={}) failed'.format(starttime, endtime)
            logger.error(message)
            raise KeyError(message)

        # FIXME: Wait for data to load after adjusting time control
        time.sleep(0.1)

    def timerange_get(self):
        """
        For fetching the current timeRange values, use::

            var timeRange = angular.element('grafana-app').injector().get('timeSrv').timeRange();
            var temp_date_from = new Date(timeRange.from);
            var temp_date_to = new Date(timeRange.to);

        -- https://community.grafana.com/t/how-to-access-time-picker-from-to-within-a-text-panel-and-jquery/6071/3
        """
        raise NotImplemented("timerange_get not implemented yet")

    def run_javascript(self, sourcecode):
        return self.marionette.execute_script(sourcecode, sandbox=None, new_sandbox=False)

    def console_log(self, message):
        javascript = "console.log('{}');".format(message)
        self.run_javascript(javascript)


class Animator:

    def __init__(self, dashboard_url, time_start=None, time_end=None, time_step=None):

        self.dashboard_url = dashboard_url
        self.time_start = time_start
        # TODO: Default to "now()"
        self.time_end = time_end
        self.time_step = time_step

        self.grafana = GrafanaWrapper()
        self.grafana.bootstrap(headless=False)

    def run(self):

        logger.info('Opening dashboard {}'.format(self.dashboard_url))

        # TODO: Parse from ``self.time_start``.
        start_date = datetime(2015, 10, 1)
        start_date_formatted = format_date(start_date)

        # TODO: Parse from ``self.time_end``.
        end_date = start_date + timedelta(days=1)
        end_date_formatted = format_date(end_date)

        # Compute first url and navigate to it.
        url = self.make_url(start_date_formatted, end_date_formatted)
        logger.info('Navigating to {}'.format(url))
        self.grafana.navigate_dashboard(url)

        # Run time range controller.
        logger.info('Starting animation')

        # TODO: Use until=``self.time_end``. Use freq=``self.time_step``.
        daterange = list(rrule(freq=DAILY, until=datetime.now(), dtstart=start_date))
        for date in daterange:
            end_date_formatted = format_date(date)

            # Notify user.
            message = 'Generating frame for {}-{}'.format(start_date_formatted, end_date_formatted)
            logger.info(message)
            self.grafana.console_log(message)

            # Render image.
            image = self.render(start_date_formatted, end_date_formatted)

    def render(self, date_begin, date_end):
        logger.debug('Adjusting time range control')
        self.grafana.timerange_set(date_begin, date_end)

        logger.debug('Rendering image')
        return self.make_image()

    def make_image(self):
        image = self.grafana.map_image()
        logger.info('Image size: %s', len(image))
        return image

    def make_url(self, date_begin, date_end):
        params = OrderedDict()

        params['orgId'] = 1
        params['from'] = date_begin
        params['to'] = date_end

        query = urlencode(params)
        url = self.dashboard_url + '?' + query

        return url


def format_date(date):
    return date.strftime('%Y%m%d')
