# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import sys
import logging
from docopt import docopt, DocoptExit
from grafanimate import __appname__, __version__
from grafanimate.core import Animator
from grafanimate.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    Usage:
      grafanimate <url> [options] [--target=<target>]...
      grafanimate --version
      grafanimate (-h | --help)

    Options:
      --target=<target>             Data output target (not available yet)
      --start=<start>               Start time
      --end=<end>                   End time
      --interval=<end>              Interval time
      --debug                       Enable debug logging
      -h --help                     Show this screen

    Examples:

      # Run on designated dashboard, starting time range control at 2015-10-01 with an interval of 1 day
      grafanimate http://localhost:3000/d/1aOmc1sik/luftdaten-info-growth --start=20151001 --interval=1d

    """

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=__appname__ + ' ' + __version__))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    #log.info('Options: {}'.format(json.dumps(options, indent=4)))

    animator = Animator(
        options['url'],
        time_start=options.get('start'),
        time_end=options.get('end', 'now'),
        time_step=options.get('interval', '1h')
    )
    animator.run()
