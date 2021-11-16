// Investigating the Grafana AngularJS application structure.
/*
grafana
grafana.core

grafana.services
grafana.panels
grafana.controllers
grafana.directives
grafana.filters
grafana.routes
*/
/*
log('angular:', angular);
log('angular.toJson:', angular.toJson());
log('angular.element:', angular.element);
log('grafana-app:', angular.element('grafana-app'));
log('grafana.module:', angular.module('grafana'));
log('grafana.services:', angular.module('grafana.services'));
log('grafana.core:', angular.module('grafana.core'));
*/

/*
var grafana_core = angular.module('grafana.core');
log('appEvents:', grafana_core.appEvents);
log('component-fail:', grafana_core.component('schrott'));
log('component:', grafana_core.component('appEvents'));
log('service:', grafana_core.service('appEvents'));
//log('directive:', grafana_core.directive('appEvents'));
log('controller:', grafana_core.controller('appEvents'));
log('factory:', grafana_core.factory('appEvents'));
log('value:', grafana_core.value('appEvents'));
log('info:', grafana_core.info());
*/

//console.info('Acquiring "dashboardSrv" component');
//dashboardSrv = angular.element('grafana-app').injector().get('dashboardSrv');
//log('dashboardSrv:', dashboardSrv);
//log('dash:', dashboardSrv.dash);

//var appEvent = dashboardSrv.$rootScope.appEvent;
//log('dash:', dashboardSrv.dash);

/*
dashboardSrv.$rootScope.$on('ds-request-response', function(event, name) {
    log('============= YEAH');
});
*/

/*
dashboardSrv.$rootScope.onAppEvent('*', function(event) {
    log('=========== EVENT:', event);
});

dashboardSrv.$rootScope.onAppEvent('ds-request-response', function(event) {
    log('=========== EVENT:', 'ds-request-response:', event);
});
*/

/*
console.info('Acquiring "alertingSrv" component');
//alertSrv = angular.element('grafana-app').injector().get('alertSrv');
//alertSrv.set(title, message, 'error', timeout);
alertingSrv = angular.element('grafana-app').injector().get('alertingSrv');
alertingSrv.set("Your error", "Your message", 'error', 4);
*/

/*
console.info('Acquiring "dashboardViewStateSrv" component');
dashboardViewStateSrv = angular.element('grafana-app').injector().get('dashboardViewStateSrv');
console.log('dashboardViewStateSrv:', dashboardViewStateSrv);
//dashboardViewStateSrv.dashboard.toggleViewMode();
*/

/*
appEvents.on('ds-request-response', function(data) {
    console.log(data);
});
*/

window.grafana_load_dashboard = function (uid) {
  //log('angular:', angular);
  console.info("Loading dashboard", uid);

  $rootScope.$on("dashboard-fetch-end", function (event, result) {
    log("DASHBOARD LOADED", event, result);
    if (result.dashboard.uid == uid) {
      log("=== CORRECT!");
    }
  });

  // https://stackoverflow.com/questions/16450125/angularjs-redirect-from-outside-angular/16450748#16450748
  $rootScope.$apply(function () {
    // https://docs.angularjs.org/api/ng/service/$location#url
    $location.url("/d/" + uid + "?from=0&to=0");
  });
  return;

  //$rootScope.$apply(function () {
  log("APPLY2 APPLY2 APPLY2");
  dashboardLoaderSrv.loadDashboard(null, null, uid).then(function (result) {
    //log('loadDashboard.result:', result);
    log("Loaded dashboard with url:", result.meta.url);
    dashboardSrv.setCurrent(result.dashboard);
    //dashboard_hook();

    //var $scope = angular.module('grafana.core').get('$scope');
    //$rootScope.initDashboard(result, $scope);

    var $rootScope = angular
      .element("grafana-app")
      .injector()
      .get("$rootScope");
    //$rootScope.$apply(function(){
    //$rootScope.text = new Date();
    $rootScope.initDashboard(result, $rootScope);
    //});
  });
  //});
};

function sidecar_boot() {
  log("==========================================");

  // https://stackoverflow.com/questions/16450125/angularjs-redirect-from-outside-angular/16450748#16450748
  $location = grafanaApp.injector().get("$location");
  log("$location:", $location);

  log('Acquiring "timeSrv" component');
  timeSrv = grafanaApp.injector().get("timeSrv");

  log('Acquiring "dashboardLoaderSrv" component');
  dashboardLoaderSrv = grafanaApp.injector().get("dashboardLoaderSrv");

  log('Acquiring "dashboardSrv" component');
  dashboardSrv = grafanaApp.injector().get("dashboardSrv");

  //log('dashboard:', dashboard);

  //var appEvent = dashboardSrv.$rootScope.appEvent;
  //log('rootScope:', dashboardSrv.$rootScope);
  //log('appEvent:', appEvent);

  /*
    dashboard.panels[0].events.on('refresh', function(event) {
        log('================ REFRESH PANEL');
        log('loading:', dashboard.panels[0].loading);
    });
    dashboard.panels[0].events.on('data-received', function(event) {
        log('================ DATA-RECEIVED');
        log('loading:', dashboard.panels[0].loading);
    });
    */

  /*
    var grafana_core = angular.module('grafana.core');
    log('grafana_core:', grafana_core);
    //var bl = grafana_core.get('LoadDashboardCtrl');
    var bl = grafana_core.LoadDashboardCtrl;
    log('bl:', bl);
    */

  /*
    var grafana_core = angular.module('grafana.core');
    log('grafana_core:', grafana_core);
    log('appEvents:', grafana_core.appEvents);
    log('appEvents:', grafana_core.$appEvents);
    log('appEvents:', grafana_core.$$appEvents);
    log('appEvents-4:', grafana_core.constant('appEvents'));

    var grafanaGraph = grafana_core.grafanaGraph;
    log('grafanaGraph:', grafanaGraph);


    appEvents = grafana_core.constant('appEvents');
    */

  $rootScope.$apply(function () {
    log("APPLY APPLY APPLY");

    //$rootScope.appEvent('toggle-kiosk-mode', { exit: true });

    //var appEvents = dashboardSrv.backendSrv.appEvents;
    //log('appEvents:', appEvents);

    /*
        appEvents.on('*', function(event, payload) {
            log('=========== EVENT appEvents:', event, payload);
        });
        appEvents.on('ds-request-response', function(event, payload) {
            log('=========== EVENT appEvents:', event, payload);
        });
        */

    $rootScope.$on("*", function (event, payload) {
      log("=========== EVENT:", event, payload);
    });

    $rootScope.$on("ds-request-response", function (event, payload) {
      log("=========== EVENT:", event, payload);
    });

    $rootScope.$on("zoom-out", function (event, payload) {
      log("=========== EVENT zoom-out:", event, payload);
    });

    $rootScope.$on("dashboard-fetch-start", function (event, payload) {
      log("=========== EVENT dashboard-fetch-start:", event, payload);
    });
    $rootScope.$on("dashboard-fetch-end", function (event, payload) {
      log("=========== EVENT dashboard-fetch-end:", event, payload);
    });

    $rootScope.$on("all", function (event, payload) {
      log("=========== EVENT ALL:", event, payload);
    });
  });

  /*
   */

  /*
    dashboardSrv.$rootScope.onAppEvent('*', function(event, payload) {
        log('=========== EVENT:', event, payload);
    });
    */

  /*
    dashboardSrv.$rootScope.$on('ds-request-response', function(event, name) {
        log('============= YEAH');
    });
    */

  /*
   */
}
//sidecar_boot();

window.grafana_set_time = function (from, to) {
  return true;

  //log('------------------------------------------');

  var inflight = dashboardSrv.backendSrv.inFlightRequests;
  //log('--- inflight:', inflight);

  // https://stackoverflow.com/questions/48264279/how-to-set-time-range-in-grafana-dashboard-from-text-panels/52492205#52492205
  timeSrv.setTime({ from: from, to: to });

  //$rootScope.appEvent('all', 'hello');
  //$rootScope.appEvent('toggle-kiosk-mode', { exit: true });

  return true;
};

// https://stackoverflow.com/questions/24595460/how-to-access-update-rootscope-from-outside-angular/24596251#24596251
//$rootScope = grafanaApp.injector().get('$rootScope');
//log('$rootScope:', $rootScope);
