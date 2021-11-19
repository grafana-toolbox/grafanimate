#####################
grafanimate changelog
#####################


in progress
===========
- Improve scope of values for ``every`` parameter. It will now accept relative
  humanized timestamps like ``2m30s``, ``1d12h`` or ``1.5 days``.
- Allow relative timestamps / time ranges also for ``start`` and ``stop``
  parameters. Accepted are humanized values like outlined above (``2m30s``),
  combined with, e.g., ``stop=start+2m30s`` or ``start=-1h, stop=now``.


2021-11-17 0.6.0
================
- Fix attribution signature on worldmap panels
- Add scenario for UBA.LDI.DWD maps
- Add dope sheet blueprint generator spike
- Modernize to Python 3
- Add compatibility with Grafana 6, 7 and 8
- Add possibility to login to protected Grafana instances
- Add possibility to control the sequencing mode (window vs. cumulative)
- Introduce data model for animation scenarios
- Allow loading scenarios from arbitrary Python modules and files
- Optionally define ``grafana_url`` and ``dashboard_uid`` within scenario file.
  Corresponding command line parameters ``--grafana-url`` and ``--dashboard-uid``
  still take preference.
- When parsing timestamps, allow ISO8801/RFC3339 and Epoch time (``start`` and ``stop``)
- Improve documentation


2019-02-04 0.5.5
================
- Revert all image size changes leading to effectively nothing


2019-02-04 0.5.4
================
- Attempt to fix image sizes in README once more


2019-02-04 0.5.3
================
- Attempt to fix image sizes in README again


2019-02-04 0.5.2
================
- Attempt to fix image sizes in README again, see
    - https://github.com/github/markup/issues/295
    - https://github.com/github/markup/issues/1162


2019-02-04 0.5.1
================
- Fix image sizes in README


2019-02-04 0.5.0
================
- Add "5 minute" and "30 minute" intervals
- Decrease frame rate to 2 fps when rendering using FFmpeg
- Add luftdaten.info to attribution area on leaflet map widget
- Add LDI NYE shot scenario
- Fix missing dependency to the "Munch" package
- Fix "ptrace" Makefile target for uploading renderings
- Add "grafana-start" Makefile target
- Prevent stalling of Grafana Studio Javascript when waiting for data arrival
  of all panels when actually rendering a single panel only.
- Deactivate default attribution of luftdaten.info for map panels
- Improve documentation


2018-12-28 0.4.1
================
- Update documentation


2018-12-28 0.4.0
================
- Add parameters ``--panel-id``, ``--header-layout`` and ``--datetime-format``
- Refactor some parts of the machinery
- Increase time to wait for Browser starting up
- Improve interval handling
- Pick reasonable timeframe for "cdc_maps" example scenario
- Improve timing for heavy dashboards
- Add Makefile target for uploading to web space
- Refactor the machinery
- Get dashboard title from Grafana runtime scope for deriving the output filename from
- Properly produce .mp4 and .gif artifacts
- Fix window size wrt. FFmpeg animated gif rendering
- Add quick hack to remove specific panel from specific dashboard
- Add option --header-layout=no-folder to omit folder name from dashboard title
- Reduce gap for scenario "ldi_with_gaps"


2018-12-27 0.3.0
================
- Fix missing ``grafana-sidecar.js`` file in Python sdist package
- Add intervals "secondly", "minutely" and "yearly". Thanks, weef!
- Improve date formatting and separation of concerns
- Add sanity checks, improve logging
- Fix croaking when initially opening dashboard with "from=0&to=0" parameters
- Optimize user interface for wide dashboad names
- Fix stalling on row-type panel objects
- Don't initially run "onPanelRefresh"?
- Update documentation


2018-12-26 0.2.0
================
- Pretend to be a real program. Happy testing!


2018-12-25 0.1.0
================
- Add proof of concept for wrapping Grafana and adjusting its
  time range control, i.e. navigating the time dimension
