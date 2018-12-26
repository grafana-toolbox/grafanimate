#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
from datetime import datetime
from grafanimate.animations import SequentialAnimation

logger = logging.getLogger(__name__)


class AnimationScenario:
    """
    Run different anmiation scenarios/sequences.

    As the ad-hoc interface is not finished yet,
    this is all we got. Enjoy!
    """

    def __init__(self, grafana_url=None, dashboard_uid=None):
        self.engine = SequentialAnimation(grafana_url=grafana_url, dashboard_uid=dashboard_uid)
        self.engine.start()

    def ldi_all(self):

        logger.info('Running scenario ldi_all')

        # LDI, ramp-up
        self.engine.run(dtstart=datetime(2015, 10, 1), dtuntil=datetime(2017, 1, 1), interval='monthly')

        # LDI, growth
        #self.run_sequence(dtstart=datetime(2017, 1, 1), dtuntil=datetime.now(), interval='weekly')

        # LDI, growth, with gap
        # 2018-04-14 - 2018-12-20
        self.engine.run(dtstart=datetime(2017, 1, 1), dtuntil=datetime(2018, 4, 28), interval='weekly')
        self.engine.run(dtstart=datetime(2018, 12, 20), dtuntil=datetime.now(), interval='weekly')
