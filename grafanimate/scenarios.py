#  -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
"""
Run different animation scenarios/sequences.

As the ad-hoc interface is not finished yet,
this is all we got. Enjoy!

The parameters `dtstart`, `dtuntil` and `interval` should explain themselves.

The parameter `mode` can has two values (defaulting to `window`):
- "window" will slide a window through the defined time range
- "cumulative" will use a fixed start time and stepwise expand the end time by `interval`
"""
import logging
from datetime import datetime

from grafanimate.model import SequencingMode, AnimationStep, AnimationScenario

logger = logging.getLogger(__name__)


def playdemo():
    """
    Run demo on `play.grafana.org`.

    Example::

        grafanimate --grafana-url=https://play.grafana.org/ --dashboard-uid=000000012 --scenario=playdemo
    """
    logger.info('Running scenario playdemo')

    return AnimationScenario(
        grafana_url="https://play.grafana.org/",
        dashboard_uid="000000012",
        steps=[
            AnimationStep(
                dtstart=datetime(2021, 11, 14, 2, 0, 0),

                # Produce video with reasonable duration.
                # dtuntil=datetime(2021, 11, 14, 4, 16, 36),

                # Produce very short video.
                dtuntil=datetime(2021, 11, 14, 2, 16, 36),

                interval='5min',
                mode=SequencingMode.CUMULATIVE,
            ),
        ]
    )


def playdemo_advanced():
    """
    Run demo on `play.grafana.org`.

    Example::

        grafanimate --grafana-url=https://play.grafana.org/ --dashboard-uid=000000012 --scenario=playdemo_advanced
    """
    logger.info('Running scenario playdemo')

    return AnimationScenario(
        grafana_url="https://play.grafana.org/",
        dashboard_uid="000000012",
        steps=[
            AnimationStep(
                dtstart=datetime(2021, 11, 14, 2, 0, 0),
                dtuntil=datetime(2021, 11, 14, 2, 16, 36),
                interval='5min',
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationStep(
                dtstart="2021-11-15T02:12:05Z",
                dtuntil="2021-11-15T02:37:36Z",
                interval='5min',
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationStep(
                dtstart=1637091011,
                dtuntil=1637091911,
                interval='5min',
                mode=SequencingMode.CUMULATIVE,
            ),
        ]
    )


def ldi_all():
    """
    Luftdaten.info, all
    """
    logger.info('Running scenario ldi_all')

    return [

        # LDI, ramp-up
        AnimationStep(
            dtstart=datetime(2015, 10, 1),
            dtuntil=datetime(2017, 1, 1),
            interval='monthly'),

        # LDI, growth
        AnimationStep(
            dtstart=datetime(2017, 1, 1),
            dtuntil=datetime.now(),
            interval='weekly'),

    ]


def ldi_with_gaps():
    """
    Luftdaten.info, growth
    """
    logger.info('Running scenario ldi_with_gaps')

    return [

        # LDI, ramp-up
        AnimationStep(
            dtstart=datetime(2015, 10, 1),
            dtuntil=datetime(2017, 1, 1),
            interval='monthly'),

        # LDI, growth, with gap at 2018-04-29 - 2018-12-20
        # TODO: Detect empty data from datasource through Grafana Sidecar and skip respective images.
        AnimationStep(
            dtstart=datetime(2017, 1, 1),
            dtuntil=datetime(2018, 6, 5),
            interval='weekly'),

        # LDI, until now
        AnimationStep(
            dtstart=datetime(2018, 12, 20),
            dtuntil=datetime.now(),
            interval='weekly'),
    ]


def ldi_nye_2017_2018():
    """
    LDI, New Year's Eve 2018
    """
    logger.info('Running scenario ldi_nye_2017_2018')
    return AnimationStep(
        dtstart=datetime(2017, 12, 31, 21, 0, 0),
        dtuntil=datetime(2018, 1, 1, 4, 0, 0),
        interval='10min')


def ldi_nye_2018_2019():
    """
    LDI, New Year's Eve 2018/2019
    """
    logger.info('Running scenario ldi_nye_2018_2019')
    return [
        AnimationStep(dtstart=datetime(2018, 12, 31, 15, 0, 0), dtuntil=datetime(2018, 12, 31, 20, 0, 0), interval='30min'),
        AnimationStep(dtstart=datetime(2018, 12, 31, 20, 0, 0), dtuntil=datetime(2018, 12, 31, 23, 0, 0), interval='10min'),
        AnimationStep(dtstart=datetime(2018, 12, 31, 23, 0, 0), dtuntil=datetime(2019, 1, 1, 1, 0, 0), interval='5min'),
        AnimationStep(dtstart=datetime(2019, 1, 1, 1, 0, 0), dtuntil=datetime(2019, 1, 1, 4, 0, 0), interval='10min'),
        AnimationStep(dtstart=datetime(2019, 1, 1, 4, 0, 0), dtuntil=datetime(2019, 1, 1, 9, 0, 0), interval='30min'),
    ]


def cdc_maps():
    """
    DWD CDC, temperatur-sonne-and-niederschlag-karten
    """
    logger.info('Running scenario cdc_maps')
    return AnimationStep(
        dtstart=datetime(2018, 3, 6, 5, 0, 0),
        dtuntil=datetime(2018, 3, 10, 23, 59, 59),
        interval='hourly')

    # Short sequence, for debugging processes.
    #return AnimationStep(dtstart=datetime(2018, 3, 6, 5, 0, 0), dtuntil=datetime(2018, 3, 6, 6, 59, 59), interval='hourly')


def uba_ldi_dwd_maps():
    """
    Labor: Studio / UBA/LDI/DWD-Studio [dev!]
    """
    logger.info('Running scenario uba_ldi_dwd_maps')
    return AnimationStep(
        dtstart=datetime(2018, 10, 6, 5, 0, 0),
        dtuntil=datetime(2018, 10, 10, 23, 59, 59),
        interval='hourly')


def ir_sensor_svg_pixmap():
    """
    dtstart: 2018-08-14 03:16:00
    dtuntil: 2018-08-14 03:16:36
    """
    logger.info('Running scenario ir_sensor_svg_pixmap')
    return AnimationStep(
        dtstart=datetime(2018, 8, 14, 3, 16, 0),
        dtuntil=datetime(2018, 8, 14, 3, 16, 36),
        interval='secondly')
