.. image:: https://img.shields.io/pypi/v/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/status/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://codecov.io/gh/grafana-toolbox/grafanimate/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/grafana-toolbox/grafanimate
    :alt: Code coverage

.. image:: https://img.shields.io/pypi/l/grafanimate.svg
    :alt: License
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/dm/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/pyversions/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/badge/Grafana-10.x%20--%2011.x-blue.svg
    :target: https://github.com/grafana/grafana
    :alt: Supported Grafana versions

|

###########
grafanimate
###########

Animate timeseries data with Grafana.


*****
About
*****

``grafanimate`` captures screenshots while animating a Grafana dashboard by
manipulating its `time range control`_, i.e. navigating through time. The
result can be rendered as a sequence of png images, an animated gif file,
and as a video file.

.. attention::

    This program can put significant load on your Grafana instance
    and the underlying database machinery. Handle with care!


*****
Setup
*****

Prerequisites
=============

This program uses the fine FFmpeg_ program for doing the heavy lifting within
in its postprocessing subsystem.


grafanimate
===========

.. code:: sh

    pip install grafanimate


.. note::

    We absolutely recommend installing this program into a Python virtualenv::

        python3 -m venv .venv
        source .venv/bin/activate
        pip install grafanimate


*****
Usage
*****

Introduction
============

``grafanimate`` works by operating on animations defined within description
files, written in Python. In cinematography jargon, this is called "exposure
sheet", or "dope sheet".

    An exposure sheet (also known variously as "dope sheet", "camera
    instruction sheet", or "X-sheet") is a sheet of paper used primarily in
    traditional animation to mark out the timing of various actions and
    dialogue.

``grafanimate`` offers convenient data types, ``AnimationScenario`` and
``AnimationSequence``, for outlining an animation scenario made of multiple
sequences.

Please have a look at the `scenarios.py`_ file for a full example containing
multiple scenarios.

Synopsis
========

A scenario definition:

.. code:: python

    AnimationScenario(
        grafana_url="https://play.grafana.org/",
        dashboard_uid="000000012",
        sequences=[
            AnimationSequence(
                start="2021-11-15T02:12:05Z",
                stop="2021-11-15T02:37:36Z",
                every="5min",
                mode=SequencingMode.CUMULATIVE,
            ),
        ],
    )


In order to run a built-in scenario, invoke:

.. code:: sh

    grafanimate --scenario=playdemo --output=./animations

To use the headless mode which renders all panels on a dashboard and use panel events instead of waiting a fixed duration run

.. code:: sh

    grafanimate --scenario=playdemo --output=./animations--headless --use-panel-events

Details
=======

``grafanimate`` also supports relative timestamps, based on the fine
`pytimeparse2`_ library.

- Within ``every``, you will express a duration.

Help
====

For getting a detailed and descriptive overview about all available command
line options, please invoke:

.. code:: sh

    grafanimate --help

Configuration
=============

Firefox Location
----------------
grafanimate will discover a Firefox installation on your system path.
If you need to configure a specific installation location, use the
environment variable ``FIREFOX_BIN`` to point to the Firefox executable
on your system.

Examples
========

Examples for scenario mode. Script your animations in file ``scenarios.py`` or
any other Python module or file.

.. code:: sh

    # Use freely accessible `play.grafana.org` for demo purposes.
    grafanimate --scenario=playdemo --output=./animations

    # Example for generating Luftdaten.info graph & map.
    export GRAFANIMATE_OUTPUT=./animations
    grafanimate --grafana-url=http://localhost:3000/ --dashboard-uid=1aOmc1sik --scenario=ldi_all

    # Use more parameters to control the rendering process.
    grafanimate --grafana-url=http://localhost:3000/ --dashboard-uid=acUXbj_mz --scenario=ir_sensor_svg_pixmap \
        --header-layout=studio --datetime-format=human-time --panel-id=6


*******************
Usage in Containers
*******************

You can use ``grafanimate`` with Docker and Podman. An OCI image is published
to ``ghcr.io/grafana-toolbox/grafanimate``.

.. code:: sh

    docker run --rm -it --volume=$(PWD)/animations:/animations ghcr.io/grafana-toolbox/grafanimate \
        --header-layout=no-chrome \
        --video-fps=30 --video-framerate=30 \
        --scenario=playdemo --output=./animations


*******
Gallery
*******

**Composition**: `The Hiveeyes Project`_. Developing a flexible beehive monitoring infrastructure.
Clicking on an image will take you to the animated version.

.. _The Hiveeyes Project: https://hiveeyes.org/


luftdaten.info coverage
=======================
.. figure:: https://ptrace.hiveeyes.org/2018-12-28_luftdaten-info-coverage.gif
    :target: https://ptrace.hiveeyes.org/2018-12-28_luftdaten-info-coverage.mp4
    :width: 480px
    :height: 306px
    :scale: 125%

    Coverage of luftdaten.info sensors starting October 2015 across Europe.

- **Data source**: `luftdaten.info`_ (LDI)
- **Production**:  `Luftdatenpumpe`_, `LDI data plane v2`_, daily.
- **Development**: `Erneuerung der Luftdatenpumpe`_. All contributions welcome.


Fine dust pollution on New Year's Eve
=====================================
.. figure:: https://ptrace.hiveeyes.org/2019-02-04_M0h7br_ik_2019-01-01T00-15-00.png
    :target: https://ptrace.hiveeyes.org/2019-02-03_particulates-on-new-year-s-eve.mp4
    :width: 1290px
    :height: 824px
    :scale: 50%

    `Animation of fine dust pollution on New Year's Eve 2018 across Europe <https://community.hiveeyes.org/t/animation-der-feinstaubbelastung-an-silvester-2018-mit-grafanimate/1472>`_.

- **Data source**: `luftdaten.info`_ (LDI)
- **Production**:  `Luftdatenpumpe`_, `LDI data plane v2`_, historical.
- **Development**: `Erneuerung der Luftdatenpumpe`_. All contributions welcome.

.. _luftdaten.info: http://luftdaten.info/
.. _Luftdatenpumpe: https://github.com/hiveeyes/luftdatenpumpe
.. _Erneuerung der Luftdatenpumpe: https://community.hiveeyes.org/t/erneuerung-der-luftdatenpumpe/1199
.. _LDI data plane v2: https://community.hiveeyes.org/t/ldi-data-plane-v2/1412


DWD CDC
=======
.. figure:: https://ptrace.hiveeyes.org/2019-02-04_DLOlE_Rmz_2018-03-10T13-00-00.png
    :target: https://ptrace.hiveeyes.org/2018-12-28_wetter-dwd-temperatur-sonne-niederschlag-karten-cdc.mp4
    :width: 1428px
    :height: 829px
    :scale: 50%

    `Short weather film about temperature, sun and precipitation based on DWD/CDC data in March 2018 <https://community.hiveeyes.org/t/kurzer-wetterfilm-uber-temperatur-sonne-und-niederschlag-auf-basis-der-dwd-cdc-daten-im-marz-2018/1475>`_.

- **Data source**: `DWD Open Data`_ (DWD)
- **Production**:  `DWD Climate Data Center (CDC), 10m-Werte: Aktuelle Lufttemperaturen, Sonnenscheindauer & Niederschlag <https://weather.hiveeyes.org/grafana/d/DLOlE_Rmz/temperatur-sonne-and-niederschlag-karten-cdc>`_
- **Development**: <work in progress>

.. _DWD Open Data: https://opendata.dwd.de/


IR-Sensor SVG-Pixmap
====================
.. figure:: https://ptrace.hiveeyes.org/2019-02-04_acUXbj_mz_2018-08-14T03-16-12.png
    :target: https://ptrace.hiveeyes.org/2019-02-04_ir-sensor-svg-pixmap.mp4
    :width: 666px
    :height: 700px
    :scale: 50%

    IR-Sensor SVG-Pixmap displaying temperature changes inside a beehive.

- **Data source**: `Clemens Gruber`_ (CG)
- **Development**: `How to Visualize 2-Dimensional Temperature Data in Grafana <https://community.hiveeyes.org/t/how-to-visualize-2-dimensional-temperature-data-in-grafana/974/15>`_

.. _Clemens Gruber: https://community.hiveeyes.org/u/clemens



**********************
Background and details
**********************

Introduction
============
Animating things in Grafana_ across the time-axis in the spirit
of the `GeoLoop Panel Plugin`_ hasn't been unlocked for Grafana
in a more general way yet. Challenge accepted!

Time warp
=========
At this programs' core is the code to `set time range in Grafana`_:

.. code:: javascript

    __grafanaSceneContext.state.$timeRange.setState({ from: from, to: to});
    __grafanaSceneContext.state.$timeRange.onRefresh();

Rendering engine
================
Turtles all the way up, the main rendering work horse is a Firefox Browser
automated through `Marionette Python Client`_ fame:

    The Marionette Python client library allows you to remotely control
    a Gecko-based browser or device which is running a Marionette server.

Outlook
=======
Neither Playlists_ nor `Scripted Dashboards`_ (now deprecated) offer these
things to the user, but this program can be combined with both in order
to implement more complex animations on top of Grafana.


----

***********
Development
***********

.. code:: sh

    # Acquire sources.
    git clone https://github.com/grafana-toolbox/grafanimate
    cd grafanimate

    # Create and activate virtualenv.
    uv venv
    source .venv/bin/activate

    # Install package in "editable" mode.
    uv pip install --editable='.[develop,test]'

    # Run linters and software tests.
    poe check


*******************
Project information
*******************

The code lives on `GitHub <https://github.com/grafana-toolbox/grafanimate>`_ and
the Python package is published to `PyPI <https://pypi.org/project/grafanimate/>`_.


Contributing
============
We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.
You can also `discuss grafanimate`_ on our forum, you are welcome to join.


Acknowledgements
================
Thanks to all the contributors who helped to co-create and conceive this
program in one way or another. You know who you are.

Also thanks to all the people working on Python, Grafana, Firefox, FFmpeg,
and the countless other software components this program is based upon.


License
=======
``grafanimate`` is licensed under the terms of the GNU AGPL v3 license.



.. _discuss grafanimate: https://community.panodata.org/t/grafanimate/205
.. _FFmpeg: https://ffmpeg.org/
.. _GeoLoop Panel Plugin: https://grafana.com/plugins/citilogics-geoloop-panel
.. _Grafana: https://grafana.com/
.. _Marionette Python Client: https://marionette-client.readthedocs.io/
.. _Playlists: http://docs.grafana.org/reference/playlist/
.. _pytimeparse2: https://github.com/onegreyonewhite/pytimeparse2
.. _scenarios.py: https://github.com/grafana-toolbox/grafanimate/blob/main/grafanimate/scenarios.py
.. _Scripted Dashboards: http://docs.grafana.org/reference/scripting/
.. _set time range in Grafana: https://stackoverflow.com/questions/48264279/how-to-set-time-range-in-grafana-dashboard-from-text-panels/52492205#52492205
.. _time range control: http://docs.grafana.org/reference/timerange/
