// -*- coding: utf-8 -*-
// (c) 2018 Andreas Motl <andreas@hiveeyes.org>
// License: GNU Affero General Public License, Version 3

/*
> Grafana is not a js library ;[
>
> -- https://github.com/grafana/grafana/issues/2122
*/

// http://stackoverflow.com/questions/5538972/console-log-apply-not-working-in-ie9/5539378#5539378
if (Function.prototype.bind) {
    var log = Function.prototype.bind.call(console.log, console);
} else {
    var log = function() {};
}


class GrafanaSidecarSrv {

    /** @ngInject */
    constructor($rootScope, $location) {

        console.info('Booting Grafana Sidecar service');

        this.$rootScope = $rootScope;
        this.$location = $location;

        this.appElement = angular.element('grafana-app');
        this.dashboardSrv = this.appElement.injector().get('dashboardSrv');
        this.timeSrv = this.appElement.injector().get('timeSrv');

        this.onDashboardOpen = this.onDashboardOpen.bind(this);

        this.all_data_loaded = false;
    }

    hasAllData(value) {
        if (value !== undefined) {
            this.all_data_loaded = value;
        }
        return this.all_data_loaded;
    }

    setTime(from, to) {
        this.timeSrv.setTime({from: from, to: to});
    }

    setupDashboard(uid) {
        this.openDashboard(uid).then(this.onDashboardOpen);
    }

    openDashboard(uid) {

        console.info('Opening dashboard', uid);

        var $rootScope = this.$rootScope;
        var $location = this.$location;
        var _this = this;
        var promise = new Promise(function(resolve, reject) {

            // Wait for dashboard being loaded.
            $rootScope.$apply(function($rootScope) {

                log('openDashboard: Installing event handlers');

                $rootScope.$on('dashboard-fetch-end', function(event, result) {
                    log('DASHBOARD LOADED', event, result);

                    // Sanity check. Has the right dashboard been loaded actually?
                    if (result.dashboard.uid == uid) {
                        resolve(result);
                    }
                });

                $rootScope.$on('all-data-received', function(event, result) {
                    //log('DASHBOARD ALL-DATA-RECEIVED', event, result);
                    _this.hasAllData(true);
                });

                // Trigger the dashboard loading.
                // https://docs.angularjs.org/api/ng/service/$location#url
                // https://stackoverflow.com/questions/16450125/angularjs-redirect-from-outside-angular/16450748#16450748
                $location.url('/d/' + uid);

            });

            // Time out this promise after a while.
            setTimeout(reject, 10000, 'Timeout while fetching dashboard ' + uid);

        });

        return promise;
    }

    setKioskMode() {

        // Enter kiosk/fullscreen mode.
        this.$rootScope.appEvent('toggle-kiosk-mode');

        // Exit kiosk mode.
        //this.$rootScope.appEvent('toggle-kiosk-mode', { exit: true });
    }

    improveDashboardChrome() {

        this.setKioskMode();

        // Top content padding.
        $('.main-view').css('padding-top', '1rem');

        // Sidemenu and navigation bar, left side.
        $('.sidemenu').hide();
        $('.navbar').css('padding-left', '15px');

        // Dashboard title, left side.
        $('.navbar-page-btn').css('font-size', 'xx-large').css('max-width', '800px');

        // Buttons and clock, right side.
        $('.navbar-buttons--tv').hide();
        $('.gf-timepicker-nav-btn').css('height', 'unset');
        $('.gf-timepicker-nav-btn >').css('font-size', 'xx-large');
        $('.gf-timepicker-nav-btn .fa-clock-o').css('margin-right', '0.5rem');

    }

    improvePanelChrome() {

        // Disable animated spinner.
        // TODO: Make controllable by commandline parameter.
        $('.panel-loading').hide();

        // Remove zoom element from Worldmap Panel.
        $('.leaflet-control-zoom').hide();

        // Hijack Leaflet attribution area for Grafana and grafanimate.
        var signature = $('.leaflet-control-attribution');
        if (!signature.data('manipulated')) {
            signature.data('manipulated', true);
            var seperator = ' | ';
            var grafanimate = $('<a href="https://github.com/daq-tools/grafanimate" title="grafanimate: Animate timeseries data with Grafana">grafanimate</a>');
            var grafana = $('<a href="https://grafana.com/" title="Grafana: The leading open source software for time series analytics">Grafana</a>');
            signature.prepend(grafanimate, seperator, grafana, seperator);
        }

    }

    onDashboardOpen() {
        console.info('Dashboard opened');

        // Adjust user interface on dashboard load.
        this.improveDashboardChrome();

        // Acquire real dashboard model object.
        var dashboard = this.dashboardSrv.dash;

        dashboard.events.on('render', function(event) {
            log('================ DASHBOARD RENDER');
        });

        var _this = this;
        dashboard.events.on('refresh', function(event) {
            //log('================ DASHBOARD REFRESH');

            // Clear signal.
            _this.hasAllData(false);

            // Adjust user interface on dashboard refresh.
            _this.improvePanelChrome();

            // Watch for panel data to arrive.
            _this.onPanelRefresh();

        });

        _this.onPanelRefresh();

    }

    onPanelRefresh() {
        var dashboard = this.dashboardSrv.dash;

        // Wait for all panels to receive their data.
        var promises = [];
        dashboard.panels.forEach(function(panel) {

            // Skip panels with type==row
            if (panel.type == 'row') {
                return;
            }

            var promise = new Promise(function(resolve, reject) {
                panel.events.on('data-received', function() {
                    //log('--- PANEL DATA-RECEIVED');
                    resolve();
                });
                panel.events.on('data-error', function(event) {
                    //console.error('--- PANEL DATA-ERROR', event);
                    reject(event);
                });
            });
            promises.push(promise);
        });

        // Consolidate all promises into single one.
        // TODO: What about the error case? Should call `.hasAllData(false)`?
        var _this = this;
        Promise.all(promises).then(function(event) {
            _this.$rootScope.$emit('all-data-received', dashboard);
        }).catch(function(error) {
            console.error('Unable to receive data:', error);
        });
    }

}

// Register sidecar service with `grafana.core`.
var grafana_core = angular.module('grafana.core');
grafana_core.service('grafanaSidecarSrv', GrafanaSidecarSrv);

// Acquire application element.
// FIXME: Can we get rid of this as a dependency?
var grafanaApp = angular.element('grafana-app');

// Put service into global scope.
window.grafanaSidecar = grafanaApp.injector().get('grafanaSidecarSrv');
