# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import sys
import logging
from docopt import docopt, DocoptExit
from grafanimate import __appname__, __version__
from grafanimate.animations import SequentialAnimation
from grafanimate.scenarios import AnimationScenario
from grafanimate.util import normalize_options, setup_logging

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
      --dashboard-uid=<uid>         Grafana dashboard uid

      --debug                       Enable debug logging
      -h --help                     Show this screen


    Examples for scenario mode. Script your animation in file "scenarios.py".

      # Generate sequence of .png files in ./var/spool/ldi_all/1aOmc1sik
      grafanimate --grafana-url=http://localhost:3000/ --scenario=ldi_all --dashboard-uid=1aOmc1sik



    NOT IMPLEMENTED YET

      --target=<target>             Data output target

    Examples: Ad hoc mode.

    Until implemented, please use scenario mode.
    Don't be afraid, it's just some copy/pasting in the "scenarios.py" file, go ahead.

      --start=<start>               Start time
      --end=<end>                   End time
      --interval=<end>              Interval time

    """

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=__appname__ + ' ' + __version__))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    #import json; log.info('Options: {}'.format(json.dumps(options, indent=4)))

    # Sanity checks.

    if not options['scenario']:
        raise DocoptExit('Error: Parameter --dashboard-uid is mandatory')

    if not options['dashboard-uid']:
        raise DocoptExit('Error: Parameter --dashboard-uid is mandatory')

    # Prepare animation.
    scenario = AnimationScenario(grafana_url=options['grafana-url'], dashboard_uid=options['dashboard-uid'])
    if not hasattr(scenario, options.scenario):
        raise NotImplementedError('Animation scenario "{}" not implemented'.format(options.scenario))

    # Run animation scenario.
    func = getattr(scenario, options.scenario)
    func()


    # TODO: Introduce ad-hoc mode. In the meanwhile, please use scenario mode.
    """
    animator = SequentialAnimation(
        options['url'],
        time_start=options.get('start'),
        time_end=options.get('end', 'now'),
        time_step=options.get('interval', '1h')
    )
    animator.run()
    """

    # TODO: Parse from ``self.time_start``.

    # 2018-01-01
    # start_date = datetime(2018, 1, 1)

    # 2018-08-09
    # start_date = datetime(2018, 8, 9)
