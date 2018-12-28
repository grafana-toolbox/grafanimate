#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
from pkg_resources import resource_stream
from marionette_driver import Wait
from marionette_driver.errors import TimeoutException
from grafanimate.marionette import FirefoxMarionetteBase
from grafanimate.util import format_date_grafana

log = logging.getLogger(__name__)


class GrafanaWrapper(FirefoxMarionetteBase):
    """
    https://marionette-client.readthedocs.io/en/master/interactive.html
    """

    def __init__(self, baseurl=None):
        self.baseurl = baseurl
        log.info('Starting GrafanaWrapper on %s', baseurl)
        FirefoxMarionetteBase.__init__(self)

    def boot_grafana(self):
        """
        Navigate to Grafana application and inject Grafana Sidecar service.
        """
        log.info('Starting Grafana at {}'.format(self.baseurl))

        # Navigate to resource URL.
        self.marionette.navigate(self.baseurl)

        # Wait for Grafana application to load.
        self.wait_for_grafana()

        # Load Javascript Grafana Sidecar service.
        with resource_stream('grafanimate', 'grafana-sidecar.js') as f:
            javascript = f.read()
            self.run_javascript(javascript)

    def wait_for_grafana(self):
        """
        Wait for element <grafana-app> to appear.
        """
        log.info('Waiting for Grafana to load')
        element = self.wait_for_element_tag("grafana-app")
        log.info('Grafana loaded')
        return element

    def open_dashboard(self, uid, options=None):
        """
        Open a Grafana Dashboard with the designated uid
        and wait for all data to load into all panels.
        """
        options = options or {}
        javascript = mkjscall("grafanaSidecar.openDashboard", uid, options)
        log.info('Running Javascript: %s', javascript)
        self.run_javascript(javascript)
        self.wait_all_data_received()

    def get_dashboard_title(self):
        return self.calljs("grafanaSidecar.getDashboardTitle")

    def wait_all_data_received(self):
        """
        Wait for all data to arrive in the dashboard.
        """

        log.info('Waiting for "all-data-received" event')
        waiter = Wait(self.marionette, timeout=20.0, interval=1.0)

        def condition(marionette):
            return self.calljs("grafanaSidecar.hasAllData")

        try:
            waiter.until(condition)
        except TimeoutException as ex:
            log.warning('Timed out waiting for data: %s. Continuing anyway.', ex)

    def clear_all_data_received(self):
        return self.calljs("grafanaSidecar.hasAllData", False)

    def timewarp(self, dtstart, dtuntil, interval):
        """
        Navigate the Dashboard to the designated point in time
        and wait for refreshing all child components including data.
        """

        # Notify user.
        message = 'Timewarp to {} -> {}'.format(dtstart, dtuntil)
        log.info(message)
        self.console_log(message)

        # Perform timewarp.
        self.clear_all_data_received()
        self.timerange_set(format_date_grafana(dtstart, interval), format_date_grafana(dtuntil, interval))
        self.wait_all_data_received()

    def timerange_set(self, starttime, endtime):
        """
        Adjust Grafana time control. This is not synchronous.
        """
        return self.calljs("grafanaSidecar.setTime", starttime, endtime)

    def timerange_get(self):
        """
        For fetching the current timeRange values, use::

            var timeRange = angular.element('grafana-app').injector().get('timeSrv').timeRange();
            var temp_date_from = new Date(timeRange.from);
            var temp_date_to = new Date(timeRange.to);

        -- https://community.grafana.com/t/how-to-access-time-picker-from-to-within-a-text-panel-and-jquery/6071/3
        """
        return self.calljs("grafanaSidecar.getTime")
        raise NotImplemented("timerange_get not implemented yet")

    def run_javascript(self, sourcecode):
        """
        Run the designated Javascript code directly in the scope
        of the application under test. Don't use any sandboxing.

        :code: Plain Javascript source code.
        """
        # https://github.com/mozilla/geckodriver/issues/1067#issuecomment-347180427
        # https://github.com/devtools-html/har-export-trigger/issues/27#issuecomment-424777524
        log.debug('Running Javascript: %s', sourcecode)
        return self.marionette.execute_script(sourcecode, sandbox=None, new_sandbox=False)

    def calljs(self, name, *args):
        return self.run_javascript(mkjscall(name, *args))

    def console_log(self, message):
        """
        Write a message to the Browser console.
        """
        return self.calljs("console.log", message)

    def wait_for_map(self):
        """
        Wait for map element <panel-plugin-grafana-worldmap-panel ...> to appear.
        """
        log.debug('Waiting for map element to appear in DOM')
        element = self.wait_for_element_tag("panel-plugin-grafana-worldmap-panel")
        log.info('Finished waiting for map element')
        log.info(element)
        return element


def mkjscall(name, *arguments, **flags):
    flags.setdefault('add_return', True)
    tpl = '{return}{name}({arguments});'
    tplvars = {
        'return': flags['add_return'] and 'return ' or '',
        'name': name,
        'arguments': mkjsargs(*arguments),
    }
    return tpl.format(**tplvars)


def mkjsargs(*arguments):
    return json.dumps(arguments).strip('[]')

