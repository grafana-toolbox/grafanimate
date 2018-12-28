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

    def __init__(self, grafana, storage, dashboard_uid=None, target=None, options=None):

        self.grafana = grafana
        self.storage = storage
        self.dashboard_uid = dashboard_uid

        # Dispatch output to different target formats.
        # FIXME: Not implemented yet.
        self.target = target

        # Start the engines.
        self.engine = SequentialAnimation(grafana=grafana, dashboard_uid=dashboard_uid, options=options)
        self.engine.start()

    def ldi_all(self):
        logger.info('Running scenario ldi_all')

        # LDI, ramp-up
        results = self.engine.run(dtstart=datetime(2015, 10, 1), dtuntil=datetime(2017, 1, 1), interval='monthly')
        self.storage.save_items(results)

        # LDI, growth
        results = self.engine.run(dtstart=datetime(2017, 1, 1), dtuntil=datetime.now(), interval='weekly')
        self.storage.save_items(results)

        self.storage.save_items(results)

    def ldi_with_gaps(self):
        logger.info('Running scenario ldi_with_gaps')

        # LDI, ramp-up
        results = self.engine.run(dtstart=datetime(2015, 10, 1), dtuntil=datetime(2017, 1, 1), interval='monthly')
        self.storage.save_items(results)

        # LDI, growth, with gap at 2018-04-29 - 2018-12-20
        # TODO: Detect empty data from datasource through Grafana Sidecar and skip respective images.
        results = self.engine.run(dtstart=datetime(2017, 1, 1), dtuntil=datetime(2018, 6, 5), interval='weekly')
        self.storage.save_items(results)

        results = self.engine.run(dtstart=datetime(2018, 12, 20), dtuntil=datetime.now(), interval='weekly')
        self.storage.save_items(results)

    def cdc_maps(self):
        logger.info('Running scenario cdc_maps')

        # CDC, temperatur-sonne-and-niederschlag-karten
        results = self.engine.run(dtstart=datetime(2018, 3, 6, 5, 0, 0), dtuntil=datetime(2018, 3, 10, 23, 59, 59), interval='hourly')

        # Short sequence, for debugging processes.
        #results = self.engine.run(dtstart=datetime(2018, 3, 6, 5, 0, 0), dtuntil=datetime(2018, 3, 6, 6, 59, 59), interval='hourly')

        self.storage.save_items(results)

    def ir_sensor_svg_pixmap(self):
        """
        dtstart: 2018-08-14 03:16:00
        dtuntil: 2018-08-14 03:16:36
        """
        logger.info('Running scenario ir_sensor_svg_pixmap')

        results = self.engine.run(dtstart=datetime(2018, 8, 14, 3, 16, 0), dtuntil=datetime(2018, 8, 14, 3, 16, 36), interval='secondly')
        self.storage.save_items(results)
