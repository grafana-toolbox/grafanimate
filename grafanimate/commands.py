# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
from docopt import docopt, DocoptExit
from grafanimate import __appname__, __version__
from grafanimate.core import make_grafana, make_animation, make_storage
from grafanimate.util import normalize_options, setup_logging, asbool

log = logging.getLogger(__name__)


def run():
    """
    Usage:
      grafanimate [options] [--target=<target>]...
      grafanimate --version
      grafanimate (-h | --help)

    Options:
      --grafana-url=<url>           Base URL to Grafana, [default: http://localhost:3000].
      --scenario=<scenario>         Which scenario to run. Scenarios are defined as methods.
      --dashboard-uid=<uid>         Grafana dashboard uid.

    Optional:
      --exposure-time=<seconds>     How long to wait for each frame to complete rendering. [default: 0.5]
      --use-panel-events            Whether to enable using Grafana's panel events. [default: false]
                                    Caveat: Used to work properly with Angular-based panels like `graph`.
                                            Stopped working with React-based panels like `timeseries`.

      --panel-id=<id>               Render single panel only by navigating to "panelId=<id>&fullscreen".
      --dashboard-view=<mode>       Use Grafana's "d-solo" view for rendering single panels without header.

      --header-layout=<layout>      The header rendering subsystem offers different modes
                                    for amending the vanilla Grafana user interface.
                                    Multiple modes can be combined.
                                    [default: large-font]

                                    - no-chrome:            Set kiosk mode, remove sidemenu and more chrome
                                    - large-font:           Use larger font sizes for title and datetime
                                    - collapse-datetime:    Collapse datetime into title
                                    - studio:               Apply studio modifications. This options aggregates
                                                            "no-chrome", "large-font" and "collapse-datetime".
                                    - no-folder:            Don't include foldername in title

                                    - no-title:             Turn off title widget
                                    - no-datetime:          Turn off datetime widget

      --datetime-format=<format>    Datetime format to use with header layouts like "studio".
                                    Examples: YYYY-MM-DD HH:mm:ss, YYYY, HH:mm.

                                    There are also some format presets available here:
                                    - human-date:           on 2018-08-14
                                    - human-time:           at 03:16:05
                                    - human-datetime:       on 2018-08-14 at 03:16:05

                                    When left empty, the default is determined by the configured interval.

      --debug                       Enable debug logging
      -h --help                     Show this screen


    Examples for scenario mode. Script your animation in file `scenarios.py`. The output files
    will be saved at `./var/spool/{scenario}/{dashboard-uid}`.

      # Use freely accessible `play.grafana.org` for demo purposes.
      grafanimate --grafana-url=https://play.grafana.org/ --dashboard-uid=000000012 --scenario=playdemo

      # Example for generating Luftdaten.info graph & map.
      grafanimate --grafana-url=http://localhost:3000/ --dashboard-uid=1aOmc1sik --scenario=ldi_all

      # Use more parameters to control the rendering process.
      grafanimate --grafana-url=http://localhost:3000/ --dashboard-uid=acUXbj_mz --scenario=ir_sensor_svg_pixmap --header-layout=studio --datetime-format=human-time --panel-id=6


    NOT IMPLEMENTED YET

      --target=<target>             Data output target

    Examples: Ad hoc mode.

    Until implemented, please use scenario mode.
    Don't be afraid, it's just some copy/pasting in the `scenarios.py` file, go ahead.

      --start=<start>               Start time
      --end=<end>                   End time
      --interval=<end>              Interval time

    """

    # Parse command line arguments.
    options = docopt(run.__doc__, version=__appname__ + ' ' + __version__)
    options = normalize_options(options, lists=['header-layout'])

    # Setup logging.
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debug command line options.
    if debug:
        log.info('Options: {}'.format(json.dumps(options, indent=4)))

    # Sanity checks.
    if not options['scenario']:
        raise DocoptExit('Error: Parameter --scenario is mandatory')

    if not options['dashboard-uid']:
        raise DocoptExit('Error: Parameter --dashboard-uid is mandatory')

    if options['dashboard-view'] == 'd-solo' and not options['panel-id']:
        raise DocoptExit('Error: Parameter --panel-id is mandatory for --dashboard-view=d-solo')

    options['exposure-time'] = float(options['exposure-time'])
    options['use-panel-events'] = asbool(options['use-panel-events'])
    if options['use-panel-events']:
        options['exposure-time'] = 0

    # Define and run Pipeline.

    # Define pipeline elements.
    grafana = make_grafana(options['grafana-url'], options['use-panel-events'])
    storage = make_storage(
        imagefile='./var/spool/{scenario}/{uid}/{uid}_{dtstart}_{dtuntil}.png',
        outputfile='./var/results/{uid}-{name}.mp4')

    # Assemble pipeline.
    animation = make_animation(grafana, storage, options)

    # Run stop motion animation to produce single artifacts.
    animation.run()

    # Run rendering steps, produce composite artifacts.
    title = grafana.get_dashboard_title()
    path = "./var/spool/{scenario}/{uid}/{uid}_*.png".format(scenario=options.scenario, uid=options["dashboard-uid"])
    results = storage.produce_artifacts(path=path, uid=options['dashboard-uid'], name=title)

    log.info('Produced %s results\n%s', len(results), json.dumps(results, indent=2))
