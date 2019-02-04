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


class GrafanaStudioSrv {

    /** @ngInject */
    constructor($rootScope, $location) {

        console.info('Booting Grafana Sidecar service');

        this.$rootScope = $rootScope;
        this.$location = $location;

        this.appElement = angular.element('grafana-app');
        this.dashboardSrv = this.appElement.injector().get('dashboardSrv');
        this.timeSrv = this.appElement.injector().get('timeSrv');

        this.onDashboardLoad = this.onDashboardLoad.bind(this);

        // FIXME: Maybe stuff this into this.dashboardSrv.dash?
        //        GrafanaStudioSrv is actually a singleton, right?

        // TODO: Create a DashboardController instance per call of "openDashboard" and hold state variables
        //       like "all_data_loaded" or "options" there as they are actually per-dashboard!

        this.options = {};
        this.all_data_loaded = false;
        this.timerange = null;
    }

    hasAllData(value) {
        if (value !== undefined) {
            this.all_data_loaded = value;
        }
        return this.all_data_loaded;
    }

    setTime(from, to) {
        // Internal bookeeping for "collapse-datetime" layout.
        this.timerange = {from: from, to: to};

        // Propagate to Grafana service.
        this.timeSrv.setTime(this.timerange);
    }

    getTime() {
        /*
        For fetching the current timeRange values, use::

            var timeRange = angular.element('grafana-app').injector().get('timeSrv').timeRange();
            var temp_date_from = new Date(timeRange.from);
            var temp_date_to = new Date(timeRange.to);

        -- https://community.grafana.com/t/how-to-access-time-picker-from-to-within-a-text-panel-and-jquery/6071/3
        */
        var timeRange = this.timeSrv.timeRange();
        return timeRange;
    }

    openDashboard(uid, options) {
        options = options || {};
        console.info('Opening dashboard', uid, options);
        //_.(this.options).extend(options);
        _.extend(this.options, options);
        this.loadDashboard(uid).then(this.onDashboardLoad);
    }

    hasHeaderLayout() {
        var header_layout = this.options['header-layout'];
        var layouts = Array.prototype.slice.call(arguments);
        for (var layout of layouts) {
            if (header_layout.includes(layout)) {
                return true;
            }
        }
        return false;
    }

    loadDashboard(uid) {

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

                        // Quick hack to remove specific panel from specific dashboard.
                        if (uid == 'DLOlE_Rmz') {
                            result.dashboard.panels.shift();
                        }

                        // Resolve promise, thus progressing the pipeline.
                        resolve(result);
                    }
                });

                $rootScope.$on('all-data-received', function(event, result) {
                    //log('DASHBOARD ALL-DATA-RECEIVED', event, result);
                    _this.hasAllData(true);
                });

                // Compute dashboard url.
                var view = 'd';
                var slug = 'foo';
                var query = '';
                if (_this.options['dashboard-view']) {
                    view = _this.options['dashboard-view'];
                }
                if (_this.options['panel-id']) {
                    query = '?panelId=' + _this.options['panel-id'] + '&fullscreen';
                }
                var url = '/' + view + '/' + uid + '/' + slug + query;

                // Trigger the dashboard loading.
                // https://docs.angularjs.org/api/ng/service/$location#url
                // https://stackoverflow.com/questions/16450125/angularjs-redirect-from-outside-angular/16450748#16450748
                $location.url(url);

            });

            // Time out this promise after a while.
            setTimeout(reject, 10000, 'Timeout while fetching dashboard ' + uid);

        });

        return promise;
    }

    onDashboardLoad() {
        console.info('Dashboard loaded');

        // Acquire real dashboard model object.
        var dashboard = this.dashboardSrv.dash;
        //log('dashboard:', dashboard);

        dashboard.events.on('render', function(event) {
            log('================ DASHBOARD RENDER');
        });

        var _this = this;
        dashboard.events.on('refresh', function(event) {
            //log('================ DASHBOARD REFRESH');

            // Clear signal.
            _this.hasAllData(false);

            // Adjust user interface on dashboard refresh.
            _this.improveDashboardChrome();
            _this.improvePanelChrome();

            // Watch dashboard for panel data to arrive.
            _this.onDashboardRefresh();

        });

        // Adjust user interface on dashboard load.
        // FIXME: This happens too fast. Complex dashboards might not have finished loading here.
        if (this.hasHeaderLayout('no-chrome', 'studio')) {
            this.setKioskMode();
        }
        //_this.improveDashboardChrome();

        // FIXME: Q: Really?
        //        A: Yes, seems to be required at least for the "cdc_maps" scenario
        //           as there won't be any refresh event to catch at first hand.
        _this.onDashboardRefresh();

    }

    onDashboardRefresh() {
        var dashboard = this.dashboardSrv.dash;

        var panel_id = this.options['panel-id'];

        // Wait for all panels to receive their data.
        var promises = [];
        dashboard.panels.forEach(function(panel) {

            //log('panel:', panel);

            // Skip all other panels when specific panel is selected.
            if (panel_id != undefined) {
                if (panel.id != panel_id) {
                    return;
                }
            }

            // Skip panels with type==row or type==text.
            //var whitelist = ['grafana-worldmap-panel', 'marcuscalidus-svg-panel'];
            var blacklist = ['row', 'text'];
            if (blacklist.includes(panel.type)) {
                return;
            }

            var promise = new Promise(function(resolve, reject) {
                panel.events.on('data-received', function() {
                    log('--- data-received for panel.id:', panel.id);
                    resolve();
                });
                panel.events.on('data-error', function(event) {
                    //console.error('--- PANEL DATA-ERROR', event);
                    console.warn('--- data-error for panel.id:', panel.id);
                    reject(event);
                });
            });
            promises.push(promise);
        });

        // Consolidate all promises into single one.
        // TODO: What about the error case? Should call `.hasAllData(false)`?
        // TODO: Q: What if promises is an empty array?
        //       A: It will resolve successfully, which might not be what we want.
        var _this = this;
        Promise.all(promises).then(function(event) {
            _this.$rootScope.$emit('all-data-received', dashboard);
        }).catch(function(error) {
            console.error('Unable to receive data:', error);
        });
    }

    improveDashboardChrome() {

        if (this.hasHeaderLayout('no-chrome', 'studio')) {

            //this.setKioskMode();

            // Add some padding to content top.
            $('.main-view').css('padding-top', '1rem');

            // Remove left side menu.
            $('.sidemenu').remove();

            // Adjust navigation bar.
            //$('.navbar').css('padding-left', '15px');
            $('.navbar').css({'background': 'unset', 'box-shadow': 'unset', 'border-bottom': 'unset'});

            // Clean up dashboard title widget.
            $('.navbar-page-btn').find('.fa-caret-down').remove();
            $('.navbar-page-btn').find('.gicon-dashboard').remove();

            // Clean up navigation buttons.
            $('.navbar-buttons--tv').remove();

        }

        // Adjust header font size. v1.
        if (this.hasHeaderLayout('large-font', 'studio')) {

            // Adjust font size of title widget.
            $('.navbar-page-btn').css('font-size', 'xx-large');
            $('.navbar-page-btn').parent().css('width', '100%');
            $('.navbar-page-btn').css('max-width', '100%');
            //$('.navbar-page-btn').css('width', '600px');
            //$('.navbar-page-btn').css('max-width', '800px');

            // Adjust font size of datetime widget.
            $('.gf-timepicker-nav-btn >').css('font-size', 'x-large');
            $('.gf-timepicker-nav-btn').css('height', 'unset');
            $('.gf-timepicker-nav-btn .fa-clock-o').css('margin-right', '0.5rem');


        }

        // Disable title widget.
        if (this.hasHeaderLayout('no-title')) {
            $('.navbar-page-btn').remove();
        }

        // Disable datetime widget.
        if (this.hasHeaderLayout('collapse-datetime', 'no-datetime', 'studio')) {
            $('.gf-timepicker-nav').remove();
            $('.navbar-buttons').remove();

            // No clipping, no ellipsis.
            $('.navbar-page-btn').css('overflow', 'unset').css('text-overflow', 'unset');
        }

    }

    improvePanelChrome() {

        //log('improvePanelChrome');

        // Remove some elements from user interface on the panel level.
        if (this.hasHeaderLayout('no-chrome', 'studio')) {

            // Disable animated spinner.
            // TODO: Make controllable by commandline parameter.
            $('.panel-loading').remove();

            // Remove zoom element from Worldmap Panel.
            $('.leaflet-control-zoom').remove();

        }

        // Collapse datetime into title.
        if (this.hasHeaderLayout('collapse-datetime', 'studio')) {

            // Build title from original one plus start time.
            var title = this.getDashboardTitle();

            // Custom datetime format.
            var infix = ' at ';
            var datetime_format = this.options['datetime-format'];
            if (datetime_format) {
                var timerange = this.getTime();
                //log('timerange:', timerange);
                var dtstart;
                if (datetime_format == 'human-date') {
                    infix = '';
                    dtstart = ' on ' + timerange.from.format('YYYY-MM-DD');
                } else if (datetime_format == 'human-time') {
                    infix = '';
                    dtstart = ' at ' + timerange.from.format('HH:mm:ss');
                } else if (datetime_format == 'human-datetime') {
                    // Datetime format naming is "on DATE at TIME".
                    // https://english.stackexchange.com/questions/182660/on-vs-at-with-date-and-time/182663#182663
                    infix = '';
                    dtstart = ' on ' + timerange.from.format('YYYY-MM-DD') + ' at ' + timerange.from.format('HH:mm:ss');
                } else {
                    dtstart = timerange.from.format(datetime_format);
                }
                title += infix + dtstart;

            } else if (this.timerange) {
                var dtstart = this.timerange.from;
                title += infix + dtstart;
            }

            $('.navbar-page-btn').text(title);

        }

        // Add attribution content.
        this.addAttribution();

    }

    getDashboardTitle() {
        // Build title from original one plus start time.
        var dashboard = this.dashboardSrv.dash;
        var title = dashboard.title;
        if (!this.hasHeaderLayout('no-folder')) {
            title = dashboard.meta.folderTitle + ' / ' + title;
        }
        return title;
    }

    setKioskMode() {

        // Enter kiosk/fullscreen mode.
        this.$rootScope.appEvent('toggle-kiosk-mode');

        // Exit kiosk mode.
        //this.$rootScope.appEvent('toggle-kiosk-mode', { exit: true });
    }

    addAttribution() {
        // Hijack Leaflet attribution area for Grafana and grafanimate.
        // TODO: Use alternative place if there 's not Worldmap in sight.
        var signature = $('.leaflet-control-attribution');
        if (!signature.data('manipulated')) {
            signature.data('manipulated', true);
            var luftdaten_info = $('<a href="https://luftdaten.info/" title="luftdaten.info – Feinstaub selber messen &#8211; Open Data und Citizen Science aus Stuttgart">luftdaten.info</a>');
            var grafanimate = $('<a href="https://github.com/daq-tools/grafanimate" title="grafanimate: Animate timeseries data with Grafana">grafanimate</a>');
            var grafana = $('<a href="https://grafana.com/" title="Grafana: The leading open source software for time series analytics">Grafana</a>');
            var separator = ' | ';
            //signature.prepend(luftdaten_info, separator, grafanimate, separator, grafana, separator);
            signature.prepend(separator, grafanimate, separator, grafana, separator);
        }
    }

}

// Register sidecar service with `grafana.core`.
var grafana_core = angular.module('grafana.core');
grafana_core.service('GrafanaStudioSrv', GrafanaStudioSrv);

// Acquire application element.
// FIXME: Can we get rid of this as a dependency?
var grafanaApp = angular.element('grafana-app');

// Put service into global scope.
window.grafanaStudio = grafanaApp.injector().get('GrafanaStudioSrv');
