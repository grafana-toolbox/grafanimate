###################
grafanimate backlog
###################


******
Prio 1
******
- [x] Fix missing .js file in Python dist package
- [x] Add ATTENTION remark to README
- [x] Improve docs about demo screenshot
- [o] Add attribution also for non-worldmap dashboards
- [x] Fix postprocessing errors::

    Input #0, image2, from './var/spool/DLOlE_Rmz/DLOlE_Rmz_*.png':
      Duration: 00:00:28.75, start: 0.000000, bitrate: N/A
        Stream #0:0: Video: png, rgba(pc), 1497x483, 4 fps, 4 tbr, 4 tbn, 4 tbc
    Stream mapping:
      Stream #0:0 -> #0:0 (png (native) -> h264 (libx264))
    Press [q] to stop, [?] for help

    [libx264 @ 0x7fcf0c001200] width not divisible by 2 (1497x483)
    [libx264 @ 0x7fa917001200] height not divisible by 2 (1348x823)

- [o] German date formatting: "Karten (CDC) am 7. März 2018 um 5 Uhr" instead of "Karten (CDC) on 2018-03-07 at 05:00:00"
- [o] Automatically set height of window based on content
- [o] Purge spool directory before starting
- [o] Put total dtstart-dtend into final output filenames
- [o] Check whether applying filtering by --panel-id actually does _not_ render the other panels
- [o] Otherwise / also, introduce --panel-whitelist and --panel-blacklist parameters


******
Prio 2
******
- [o] Make output directory ``./var/spool`` configurable
- [o] Set User-Agent appropriately
- [o] Screenshot by element or fullscreen, reflect in output directory somehow
- [o] Integrate postprocessing.py into scenario, make upload optionally
- [o] Check "ir-sensor-svg-pixmap" [weef]
- [o] Handle error ``--- PANEL DATA-ERROR TypeError: "ctrl.series[0] is undefined"`` on:
      https://swarm.hiveeyes.org/grafana/d/_TbvFUyik/weef-test-ir-sensor-svg-pixmap-for-grafanimate?from=0&to=0&orgId=2&kiosk=tv
- [o] Render specific panel in fullscreen mode like ``&panelId=6&fullscreen`` [weef]
- [o] Optionally, also use ``d-solo`` mode for rendering a single panel without any header at all [weef]
- [o] Remove background header gradient when being in fullscreen mode?
- [o] Default to "now()" if no dtuntil is given
- [o] Check which timezone offset gets used when addressing by unqualified timestamp
- [o] Problem when trying to address Grafana in "d-solo" mode like
      ``https://swarm.hiveeyes.org/grafana/d-solo/_TbvFUyik?panelId=6&fullscreen``,
      only works with https://swarm.hiveeyes.org/grafana/d-solo/_TbvFUyik/<slug>.
      While it will load with an arbitrary slug, it will display two "Dashboard init failed; t.dashboard is undefined"
      notification popups, which we have to avoid.

      Possible workaround: Retrieve correct slug by means of
      http http://localhost:3000/api/dashboards/uid/1aOmc1sik | jq '.meta.slug'
- [o] Split timerange into even-sized segments with ``rrule(count=N)``
- [o] Introduce interval specifiers like '1h', '3d', etc.

******
Prio 3
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
- [o] Detect when ``window.grafanaStudio`` goes away. I.e. when reloading the browser.
- [o] Improve error handling. Currently croaks with
    - ``from=0&to=0`` or ``from=2018-08-14&to=2018-08-14``
      on "weef-test-ir-sensor-svg-pixmap-for-grafanimate"
- [o] Rename to "Grafana Studio" and publish as regular Grafana Plugin


******
Prio 4
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
