.. image:: https://img.shields.io/pypi/v/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/status/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/l/grafanimate.svg
    :alt: License
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/pyversions/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/dm/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

|

###########
grafanimate
###########

Animate timeseries data with Grafana.


*****
About
*****
`grafanimate` captures screenshots while animating a
Grafana dashboard by manipulating its `time range control`_,
i.e. navigating through time. The result can be rendered as a
sequence of png images, an animated gif file and as a video file.


.. attention::

    This program can put significant load on your Grafana instance
    and the underlying database machinery. Handle with care!


*****
Setup
*****

Prerequisites
=============
This program uses the fine ffmpeg_ for doing the heavy lifting.

.. _ffmpeg: https://ffmpeg.org/


grafanimate
===========

You most probably want to install ``grafanimate`` from source, because you
currently will need to edit the ``grafanimate/scenarios.py`` file to define
your own animations.

Here we go::

    # Acquire sources.
    git clone https://github.com/panodata/grafanimate
    cd grafanimate

    # Create and activate virtualenv.
    python3 -m venv .venv
    source .venv/bin/activate

    # Install package in "editable" mode.
    pip install --editable=.

.. note:: We absolutely recommend installing the program into a Python virtualenv.


*****
Usage
*****
::

    $ grafanimate --help

    Usage:
      grafanimate [options] [--target=<target>]...
      grafanimate --version
      grafanimate (-h | --help)

    Options:
      --grafana-url=<url>           Base URL to Grafana, [default: http://localhost:3000].
      --scenario=<scenario>         Which scenario to run. Scenarios are defined as methods.
      --dashboard-uid=<uid>         Grafana dashboard uid.

    Optional:
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


    Examples for scenario mode. Script your animation in file "scenarios.py".

      # Generate sequence of .png files in ./var/spool/ldi_all/1aOmc1sik
      grafanimate --grafana-url=http://localhost:3000/ --scenario=ldi_all --dashboard-uid=1aOmc1sik

      # Use more parameters to control the rendering process.
      grafanimate --grafana-url=http://localhost:3000/ --scenario=ir_sensor_svg_pixmap --dashboard-uid=_TbvFUyik --header-layout=studio --datetime-format=human-time --panel-id=6


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
At this programs' core is the code to `set time range in Grafana`_::

    timeSrv = angular.element('grafana-app').injector().get('timeSrv');
    timeSrv.setTime({from: "2015-10-01", to: "2018-12-31"});

Rendering engine
================
Turtles all the way up, the main rendering work horse is a Firefox Browser
automated through `Marionette Python Client`_ fame:

    The Marionette Python client library allows you to remotely control
    a Gecko-based browser or device which is running a Marionette server.

Outlook
=======
Neither Playlists_ nor `Scripted Dashboards`_ offer these things
to the user, but this program can be combined with both in order
to implement more complex animations on top of Grafana.


----

*******************
Project information
*******************
``grafanimate`` is released under the GNU AGPL v3 license.

The code lives on `GitHub <https://github.com/daq-tools/grafanimate>`_ and
the Python package is published to `PyPI <https://pypi.org/project/grafanimate/>`_.

The software has been tested on Python 2.7.


Contributing
============
We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.


License
=======
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program; if not, see:
<http://www.gnu.org/licenses/agpl-3.0.txt>,
or write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA



.. _Grafana: https://grafana.com/
.. _GeoLoop Panel Plugin: https://grafana.com/plugins/citilogics-geoloop-panel
.. _time range control: http://docs.grafana.org/reference/timerange/
.. _Playlists: http://docs.grafana.org/reference/playlist/
.. _Scripted Dashboards: http://docs.grafana.org/reference/scripting/
.. _set time range in Grafana: https://stackoverflow.com/questions/48264279/how-to-set-time-range-in-grafana-dashboard-from-text-panels/52492205#52492205
.. _Marionette Python Client: https://marionette-client.readthedocs.io/
