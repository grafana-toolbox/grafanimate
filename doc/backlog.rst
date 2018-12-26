###################
grafanimate backlog
###################


******
Prio 1
******
- [o] Fix missing .js file in Python dist package
- [o] Wait for data to load after adjusting time control
- [o] Screenshot by element or fullscreen
- [o] Specify element (tag or class name) on commandline
- [o] Show notification like "Sommerpause", "Event Xyz!", etc.
- [o] Quarterly for LDI gif on README
- [o] Introduce ad-hoc mode::

    # Run on designated dashboard, starting time range control at 2015-10-01 with an interval of 1 day
    grafanimate http://localhost:3000/d/1aOmc1sik/luftdaten-info-coverage --start=20151001 --interval=1d



******
Prio 2
******
- [x] Rename title: "luftdaten.info growth"
- [x] Improve dashboard layout
- [/] Add counter element
- [o] Toggle fullscreen mode
- [o] Hide spinner

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
- [o] Use https://grafana.com/plugins/ryantxu-ajax-panel to show other content
