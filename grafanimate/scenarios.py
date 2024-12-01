# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
"""
Introduction
============

This file hosts all built-in exposure sheets, i.e. multiple projects.
Its purpose is to define how to run different animation scenarios/sequences.

    An exposure sheet (also known variously as "dope sheet", "camera
    instruction sheet", or "X-sheet") is a sheet of paper used primarily in
    traditional animation to mark out the timing of various actions and
    dialogue.


Details
=======

The parameters `start`, `stop` and `every` should be self-explaining.

The parameter `mode` can have two values (defaulting to `window`):
- "window" will slide a window through the defined time range, with `every` as window width
- "cumulative" will use a fixed start time and stepwise expand the end time by `every`
"""

import logging
from datetime import datetime

from grafanimate.model import AnimationScenario, AnimationSequence, SequencingMode

logger = logging.getLogger(__name__)


def playdemo():
    """
    Run demo on `play.grafana.org`.

    Synopsis::

        grafanimate --scenario=playdemo --output=./animations
    """
    logger.info("Running scenario playdemo")

    return AnimationScenario(
        grafana_url="https://play.grafana.org/",
        dashboard_uid="000000012",
        sequences=[
            AnimationSequence(
                start=datetime(2021, 11, 14, 2, 0, 0),
                # Produce video with reasonable duration to explore different rendering options.
                stop=datetime(2021, 11, 14, 4, 16, 36),
                # Produce very short video.
                # stop=datetime(2021, 11, 14, 2, 16, 36),
                every="5min",
                mode=SequencingMode.CUMULATIVE,
            ),
        ],
    )


def playdemo_advanced():
    """
    Run demo on `play.grafana.org`, demonstrating different flavors of timestamps.

    Synopsis::

        grafanimate --scenario=playdemo_advanced --output=./animations
    """
    logger.info("Running scenario playdemo")

    return AnimationScenario(
        grafana_url="https://play.grafana.org/",
        dashboard_uid="000000012",
        sequences=[
            AnimationSequence(
                start=datetime(2021, 11, 14, 2, 0, 0),
                stop=datetime(2021, 11, 14, 2, 16, 36),
                every="5min",
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationSequence(
                start="2021-11-15T02:12:05Z",
                stop="2021-11-15T02:37:36Z",
                every="3min",
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationSequence(
                start=1637091011,
                stop=1637091911,
                every="4m5s",
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationSequence(
                start="-30m",
                stop="+30m",
                every="5m",
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationSequence(
                start="-14d",
                stop="start+7d",
                every="1d",
                mode=SequencingMode.CUMULATIVE,
            ),
            AnimationSequence(
                start="-14d",
                stop="now",
                every="1d",
                mode=SequencingMode.CUMULATIVE,
            ),
        ],
    )


def ldi_all():
    """
    Luftdaten.info, all

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=1aOmc1sik --scenario=ldi_all --output=./animations
    """
    logger.info("Running scenario ldi_all")

    return [
        # LDI, ramp-up
        AnimationSequence(
            start=datetime(2015, 10, 1),
            stop=datetime(2017, 1, 1),
            every="monthly",
        ),
        # LDI, growth
        AnimationSequence(
            start=datetime(2017, 1, 1),
            stop=datetime.now(),
            every="weekly",
        ),
    ]


def ldi_with_gaps():
    """
    Luftdaten.info, growth

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=1aOmc1sik --scenario=ldi_with_gaps --output=./animations
    """
    logger.info("Running scenario ldi_with_gaps")

    return [
        # LDI, ramp-up
        AnimationSequence(
            start=datetime(2015, 10, 1),
            stop=datetime(2017, 1, 1),
            every="monthly",
        ),
        # LDI, growth, with gap at 2018-04-29 - 2018-12-20
        # TODO: Detect empty data from datasource through Grafana Sidecar and skip respective images.
        AnimationSequence(
            start=datetime(2017, 1, 1),
            stop=datetime(2018, 6, 5),
            every="weekly",
        ),
        # LDI, until now
        AnimationSequence(
            start=datetime(2018, 12, 20),
            stop=datetime.now(),
            every="weekly",
        ),
    ]


def ldi_nye_2017_2018():
    """
    LDI, New Year's Eve 2018

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=1aOmc1sik --scenario=ldi_nye_2017_2018 --output=./animations
    """
    logger.info("Running scenario ldi_nye_2017_2018")
    return AnimationSequence(
        start=datetime(2017, 12, 31, 21, 0, 0),
        stop=datetime(2018, 1, 1, 4, 0, 0),
        every="10min",
    )


def ldi_nye_2018_2019():
    """
    LDI, New Year's Eve 2018/2019

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=1aOmc1sik --scenario=ldi_nye_2018_2019 --output=./animations
    """
    logger.info("Running scenario ldi_nye_2018_2019")
    return [
        AnimationSequence(
            start=datetime(2018, 12, 31, 15, 0, 0),
            stop=datetime(2018, 12, 31, 20, 0, 0),
            every="30min",
        ),
        AnimationSequence(
            start=datetime(2018, 12, 31, 20, 0, 0),
            stop=datetime(2018, 12, 31, 23, 0, 0),
            every="10min",
        ),
        AnimationSequence(
            start=datetime(2018, 12, 31, 23, 0, 0),
            stop=datetime(2019, 1, 1, 1, 0, 0),
            every="5min",
        ),
        AnimationSequence(
            start=datetime(2019, 1, 1, 1, 0, 0),
            stop=datetime(2019, 1, 1, 4, 0, 0),
            every="10min",
        ),
        AnimationSequence(
            start=datetime(2019, 1, 1, 4, 0, 0),
            stop=datetime(2019, 1, 1, 9, 0, 0),
            every="30min",
        ),
    ]


def cdc_maps():
    """
    DWD CDC, temperatur-sonne-and-niederschlag-karten

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=DLOlE_Rmz --scenario=cdc_maps --output=./animations
    """
    logger.info("Running scenario cdc_maps")
    return AnimationSequence(
        start=datetime(2018, 3, 6, 5, 0, 0),
        stop=datetime(2018, 3, 10, 23, 59, 59),
        every="hourly",
    )

    # Short sequence, for debugging processes.
    # return AnimationSequence(start=datetime(2018, 3, 6, 5, 0, 0), stop=datetime(2018, 3, 6, 6, 59, 59), every='hourly')


def uba_ldi_dwd_maps():
    """
    Labor: Studio / UBA/LDI/DWD-Studio [dev!]

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=of6c9qlmk --scenario=uba_ldi_dwd_maps --output=./animations
    """
    logger.info("Running scenario uba_ldi_dwd_maps")
    return AnimationSequence(
        start=datetime(2018, 10, 6, 5, 0, 0),
        stop=datetime(2018, 10, 10, 23, 59, 59),
        every="hourly",
    )


def ir_sensor_svg_pixmap():
    """
    start: 2018-08-14 03:16:00
    stop: 2018-08-14 03:16:36

    Synopsis::

        grafanimate --grafana-url=https://daq.example.org/grafana --dashboard-uid=acUXbj_mz --scenario=ir_sensor_svg_pixmap --output=./animations
    """
    logger.info("Running scenario ir_sensor_svg_pixmap")
    return AnimationSequence(
        start=datetime(2018, 8, 14, 3, 16, 0),
        stop=datetime(2018, 8, 14, 3, 16, 36),
        every="secondly",
    )
