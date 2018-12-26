###################
grafanimate backlog
###################


******
Prio 1
******
- [x] Fix missing .js file in Python dist package
- [x] Add ATTENTION remark to README
- [x] Improve docs about demo screenshot
- [o] Make output directory ``./var/spool`` configurable
- [o] Set User-Agent appropriately
- [o] Screenshot by element or fullscreen, reflect in output directory somehow
- [o] Integrate postprocessing.py into scenario, make upload optionally
- [o] Check "ir-sensor-svg-pixmap" [weef]
- [o] Handle error ``--- PANEL DATA-ERROR TypeError: "ctrl.series[0] is undefined"`` on:
      https://swarm.hiveeyes.org/grafana/d/_TbvFUyik/weef-test-ir-sensor-svg-pixmap-for-grafanimate?from=0&to=0&orgId=2&kiosk=tv


******
Prio 2
******
- [o] Start- und Endtime in Unix Epoch oder sogar gemischt [weef]
- [o] Add audio::

    The latter optionally accepts adding audio for creating a more immersive atmosphere.

- [o] Specify element (tag or class name) on commandline
- [o] Show notifications/annotations/events like "Sommerpause", "Event Xyz!", etc.
- [o] Render LDI quarterly for gif file on README
- [o] Introduce ad-hoc mode::

    # Run on designated dashboard, starting time range control at 2015-10-01 with an interval of 1 day
    grafanimate http://localhost:3000/d/1aOmc1sik/luftdaten-info-coverage --start=20151001 --interval=1d

- [o] Implement different datetime output and formatting flavours
- [o] Detect when grafanaSidecar goes away. I.e. when reloading the browser.
- [o] Improve error handling. Currently croaks with
    - ``from=0&to=0`` or ``from=2018-08-14&to=2018-08-14``
      on "weef-test-ir-sensor-svg-pixmap-for-grafanimate"


******
Prio 3
******
- [o] Repeat the very last frame for some more times.
- [o] Put Grafana hostname into filename when saving
- [o] Actually honor options ``--start``, ``--end`` and ``--interval``
- [o] Implement GrafanaWrapper.timerange_get
- [o] Add eye candy like clock element from "Es war einmal..."
- Add more options for
    - [o] Running Firefox headless or not
    - [o] Time range control and stepping
- Add more content
    - Stations currently appearing
    - PR events happening
- [o] How to popup the overlay for a short amount of time after
      place is added to map for the first time?
- [o] Add counter element
- [o] Use https://grafana.com/plugins/ryantxu-ajax-panel to show other content


****
Done
****
- [x] Rename title: "luftdaten.info growth"
- [x] Improve dashboard layout
- [x] Toggle fullscreen mode
- [x] Hide spinner
- [x] Timing: Wait for data to load after adjusting time control
