// -*- coding: utf-8 -*-
// (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
// License: GNU Affero General Public License, Version 3

/*
> Grafana is not a js library ;[
>
> -- https://github.com/grafana/grafana/issues/2122
*/

class GrafanaStudioSrv {
  constructor() {
    console.info("Starting GrafanaStudio sidecar service");

    this.grafanaVersion = window.grafanaBootData.settings.buildInfo.version;
    console.log("Grafana version:", this.grafanaVersion);

    this.appElement = document.querySelector("grafana-app");

    this.onDashboardLoad = this.onDashboardLoad.bind(this);
    this.waitForDashboard = this.waitForDashboard.bind(this);

    this.options = {};
    this.timerange = null;
  }

  login(username, password) {
    console.log("Invoking login");

    // https://github.com/grafana/grafana/blob/v8.2.4/public/app/core/components/Login/LoginCtrl.tsx#L85-L106
    $.post({
      url: "/login", // The URL where the POST request is sent
      contentType: "application/json",
      data: JSON.stringify({ user: username, password: password }),
      success: function (response) {
        console.log("Success:", response); // Handle success
      },
      error: function (xhr, status, error) {
        console.log("Login Failed:", error); // Handle error
      },
    });
  }

  hasAllData(value) {
    return (
      document.querySelector('[aria-label="Refresh"]') &&
      !document.querySelector('[aria-label="Cancel"]')
    );
  }

  setTime(from, to) {
    __grafanaSceneContext.state.$timeRange.setState({ from: from, to: to });
    __grafanaSceneContext.state.$timeRange.onRefresh();
  }

  getTime() {
    return __grafanaSceneContext.state.$timeRange.getUrlState();
  }

  openDashboard(uid, options) {
    options = options || {};
    console.info("Opening dashboard", uid, options);
    //_.(this.options).extend(options);
    _.extend(this.options, options);
    // TODO while loadDashboard does not properly work, we need to apply customization ourselves
    this.onDashboardLoad();
    this.loadDashboard(uid).then(this.onDashboardLoad);
  }

  hasHeaderLayout() {
    var header_layout = this.options["header-layout"] || [];
    var layouts = Array.prototype.slice.call(arguments);
    for (var layout of layouts) {
      if (header_layout.includes(layout)) {
        return true;
      }
    }
    return false;
  }

  waitForDashboard(uid, resolve, reject) {
    console.log("waitForDashboard");
    var dashboard = __grafanaSceneContext._state;
    if (dashboard) {
      // Sanity check. Has the right dashboard been loaded actually?
      if (dashboard.uid == uid) {
        // Resolve promise, thus progressing the pipeline.
        resolve(dashboard);
        return;
      }
    }
    setTimeout(this.waitForDashboard, 100, uid, resolve, reject);
  }

  loadDashboard(uid) {
    var _this = this;
    var promise = new Promise(function (resolve, reject) {
      // Compute dashboard url.
      var view = "d";
      var slug = "foo";
      var query = "";
      if (_this.options["dashboard-view"]) {
        view = _this.options["dashboard-view"];
      }
      if (_this.options["panel-id"]) {
        query = "?panelId=" + _this.options["panel-id"] + "&fullscreen";
      }
      var url = "/" + view + "/" + uid + "/" + slug + query;

      // TODO We need a replacement for Grafana 11 for this
      // which opens a dashboard without a reload

      // Trigger the dashboard loading.
      // https://docs.angularjs.org/api/ng/service/$location#url
      // https://stackoverflow.com/questions/16450125/angularjs-redirect-from-outside-angular/16450748#16450748
      // TODO: If you need to automatically navigate the user to a new place in the application this should
      //       be done via the LocationSrv and it will make sure to update the application state accordingly.
      //       https://grafana.com/docs/grafana/latest/packages_api/runtime/locationsrv/
      //       https://community.grafana.com/t/how-can-i-change-template-varibale-in-a-react-plugin-in-grafana-7-0/31345/2
      //window.location.assign(url);

      // Time out this promise after a while.
      setTimeout(reject, 10000, "Timeout while loading dashboard " + uid);
    });

    return promise;
  }

  onDashboardLoad() {
    console.log("onDashboardLoad");

    __grafanaSceneContext._events.on("render", function (event) {
      console.log("================ DASHBOARD RENDER");
    });

    var _this = this;
    __grafanaSceneContext._events.on("refresh", function (event) {
      console.log("================ DASHBOARD REFRESH");
      // Clear signal.

      // Adjust user interface on dashboard refresh.
      _this.improveDashboardChrome();
      _this.improvePanelChrome();
    });

    // Adjust user interface on dashboard load.
    // FIXME: This happens too fast. Complex dashboards might not have finished loading here.
    if (this.hasHeaderLayout("no-chrome", "studio")) {
      this.setKioskMode();
    }
  }

  improveDashboardChrome() {
    // undock menu if visible
    if (document.querySelector('[aria-label="Undock menu"]')) {
      document.querySelector('[aria-label="Undock menu"]').click();
    }

    // below CSS properteis are not working with Grafana 11 anymore
    if (this.hasHeaderLayout("no-chrome", "studio")) {
      //this.setKioskMode();

      // Add some padding to content top.
      $(".main-view").css("padding-top", "1rem");
    }

    // Adjust header font size. v1.
    if (this.hasHeaderLayout("large-font", "studio")) {
      // Adjust font size of title widget.
      $(".navbar-page-btn").css("font-size", "xx-large");
      $(".navbar-page-btn").parent().css("width", "100%");
      $(".navbar-page-btn").css("max-width", "100%");
      //$('.navbar-page-btn').css('width', '600px');
      //$('.navbar-page-btn').css('max-width', '800px');

      // Adjust font size of datetime widget.
      $(".gf-timepicker-nav-btn >").css("font-size", "x-large");
      $(".gf-timepicker-nav-btn").css("height", "unset");
      $(".gf-timepicker-nav-btn .fa-clock-o").css("margin-right", "0.5rem");
    }

    // Disable title widget.
    if (this.hasHeaderLayout("no-title")) {
      $(".navbar-page-btn").remove();
    }

    // Disable datetime widget.
    if (this.hasHeaderLayout("collapse-datetime", "no-datetime", "studio")) {
      $(".gf-timepicker-nav").remove();
      $(".navbar-buttons").remove();

      // No clipping, no ellipsis.
      $(".navbar-page-btn")
        .css("overflow", "unset")
        .css("text-overflow", "unset");
    }
  }

  improvePanelChrome() {
    //log('improvePanelChrome');

    // Remove some elements from user interface on the panel level.
    if (this.hasHeaderLayout("no-chrome", "studio")) {
      // Disable animated spinner.
      // TODO: Make controllable by commandline parameter.
      $(".panel-loading").remove();

      // Remove zoom element from Worldmap Panel.
      $(".leaflet-control-zoom").remove();
    }

    // Build title from original one plus start time.
    var title = this.getDashboardTitle();

    // Custom datetime format.
    var infix = " at ";
    var datetime_format = this.options["datetime-format"];
    if (datetime_format) {
      var timerange = this.getTime();
      //log('timerange:', timerange);
      var dtstart;
      if (datetime_format == "human-date") {
        infix = "";
        dtstart = " on " + timerange.from.format("YYYY-MM-DD");
      } else if (datetime_format == "human-time") {
        infix = "";
        dtstart = " at " + timerange.from.format("HH:mm:ss");
      } else if (datetime_format == "human-datetime") {
        // Datetime format naming is "on DATE at TIME".
        // https://english.stackexchange.com/questions/182660/on-vs-at-with-date-and-time/182663#182663
        infix = "";
        dtstart =
          " on " +
          timerange.from.format("YYYY-MM-DD") +
          " at " +
          timerange.from.format("HH:mm:ss");
      } else {
        dtstart = timerange.from.format(datetime_format);
      }
      title += infix + dtstart;
    } else {
      var dtstart = this.getTime().from;
      title += infix + dtstart;
    }

    if (this.options["panel-id"] != undefined) {
      $("h2").text(title);
    }

    // Add attribution content.
    this.addAttribution();
  }

  getDashboardTitle() {
    // Build title from original one plus start time.

    var dashboard = __grafanaSceneContext._state;
    var title = dashboard.title;
    if (!this.hasHeaderLayout("no-folder")) {
      title = dashboard.meta.folderTitle + " / " + title;
    }
    return title;
  }

  setKioskMode() {
    if (!document.querySelector('[title="Enable kiosk mode"]')) {
      document.querySelector('[title="Toggle top search bar"]').click();
    }
    document.querySelector('[title="Enable kiosk mode"]').click();
  }

  addAttribution() {
    // Hijack Leaflet attribution area for Grafana and grafanimate.
    // TODO: Use alternative place if there 's not Worldmap in sight.
    var signature = $(".ol-attribution, .leaflet-control-attribution");
    if (!signature.data("manipulated")) {
      signature.data("manipulated", true);
      var grafanimate = $(
        '<a href="https://github.com/grafana-toolbox/grafanimate" title="grafanimate: Animate timeseries data with Grafana">grafanimate</a>',
      );
      var grafana = $(
        '<a href="https://grafana.com/" title="Grafana: The leading open source software for time series analytics">Grafana</a>',
      );
      var separator = " | ";
      //signature.prepend(luftdaten_info, separator, grafanimate, separator, grafana, separator);
      signature.prepend(grafanimate, separator, grafana, separator);
    }
  }
}

// Put service into global scope.
window.grafanaStudio = new GrafanaStudioSrv();
