#  -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import os
import logging
from datetime import datetime

from grafanimate.animations import SequentialAnimation
from grafanimate.util import format_date_human

logger = logging.getLogger(__name__)


class AnimationScenarioBase:

    def save_items(self, results):

        for item in results:
            #logger.info('item: %s', item)
            printable = item.copy()
            printable.data.image = printable.data.image[:23] + '...'
            logger.debug('Item: %s', printable)
            self.save_item(item)

    def save_item(self, item):

        # Compute image sequence file name.
        imagefile = './var/spool/{uid}/{uid}_{date}.png'.format(
            interval=item.meta.interval,
            uid=item.meta.dashboard,
            date=format_date_human(item.data.dtstart))

        # Ensure directory exists.
        directory = os.path.dirname(imagefile)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Store image.
        with open(imagefile, 'w') as f:
            f.write(item.data.image)

        logger.info('Saved frame to {}. Size: {}'.format(imagefile, len(item.data.image)))


class AnimationScenario(AnimationScenarioBase):
    """
    Run different anmiation scenarios/sequences.

    As the ad-hoc interface is not finished yet,
    this is all we got. Enjoy!
    """

    def __init__(self, grafana, dashboard_uid=None, target=None, options=None):

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
        self.save_items(results)

        # LDI, growth
        results = self.engine.run(dtstart=datetime(2017, 1, 1), dtuntil=datetime.now(), interval='weekly')
        self.save_items(results)

        self.save_items(results)

    def ldi_with_gaps(self):
        logger.info('Running scenario ldi_with_gaps')

        # LDI, ramp-up
        results = self.engine.run(dtstart=datetime(2015, 10, 1), dtuntil=datetime(2017, 1, 1), interval='monthly')
        self.save_items(results)

        # LDI, growth, with gap at 2018-04-29 - 2018-12-20
        # TODO: Detect empty data from datasource through Grafana Sidecar and skip respective images.
        results = self.engine.run(dtstart=datetime(2017, 1, 1), dtuntil=datetime(2018, 4, 28), interval='weekly')
        self.save_items(results)

        results = self.engine.run(dtstart=datetime(2018, 12, 20), dtuntil=datetime.now(), interval='weekly')
        self.save_items(results)

    def cdc_maps(self):
        logger.info('Running scenario cdc_maps')

        # CDC, temperatur-sonne-and-niederschlag-karten
        results = self.engine.run(dtstart=datetime(2018, 3, 6, 5, 0, 0), dtuntil=datetime(2018, 3, 10, 23, 59, 59), interval='hourly')
        self.save_items(results)

    def ir_sensor_svg_pixmap(self):
        """
        dtstart: 2018-08-14 03:16:00
        dtuntil: 2018-08-14 03:16:36
        """
        logger.info('Running scenario ir_sensor_svg_pixmap')

        results = self.engine.run(dtstart=datetime(2018, 8, 14, 3, 16, 0), dtuntil=datetime(2018, 8, 14, 3, 16, 36), interval='secondly')
        self.save_items(results)
