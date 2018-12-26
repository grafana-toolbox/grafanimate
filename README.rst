.. image:: https://img.shields.io/badge/Python-2.7-green.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/pypi/v/grafanimate.svg
    :target: https://pypi.org/project/grafanimate/

.. image:: https://img.shields.io/github/tag/daq-tools/grafanimate.svg
    :target: https://github.com/daq-tools/grafanimate

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
i.e. navigating through time.

The result can be saved as a sequence of images, an animated
gif file or as a video file.


.. attention::

    This program can put significant load on your Grafana instance
    and the underlying database machinery. Handle with care!


****
Demo
****

Screenshot
==========
Coverage of luftdaten.info sensors starting October 2015.

.. image:: https://ptrace.hiveeyes.org/2018-12-26_ldi-coverage.gif
    :width: 600px

Details
=======
- **Data source**: `luftdaten.info`_ (LDI)
- **Production**: `Luftdatenpumpe`_, daily

- **Development**: `Erneuerung der Luftdatenpumpe`_. All contributions welcome.
- **Composition**: `The Hiveeyes Project`_. Developing a flexible beehive monitoring infrastructure.

.. _luftdaten.info: http://luftdaten.info/
.. _Luftdatenpumpe: https://github.com/hiveeyes/luftdatenpumpe
.. _Erneuerung der Luftdatenpumpe: https://community.hiveeyes.org/t/erneuerung-der-luftdatenpumpe/1199
.. _The Hiveeyes Project: https://hiveeyes.org/



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
      --scenario=<scenario>         Which scenario to run. Scenarios are defined as methods in file "scenarios.py".
      --dashboard-uid=<uid>         Grafana dashboard uid

      --debug                       Enable debug logging
      -h --help                     Show this screen

      --target=<target>             Data output target (not available yet)

    Examples:

      # Generate sequence of .png files in ./var/spool/ldi_all/1aOmc1sik
      grafanimate --grafana-url=http://localhost:3000/ --scenario=ldi_all --dashboard-uid=1aOmc1sik


    Todo: Implement ad-hoc mode.
    Until then, please use scenario mode.
    Don't be afraid, it's just some copy/pasting in the scenarios.py file, go ahead.

      --start=<start>               Start time
      --end=<end>                   End time
      --interval=<end>              Interval time


*****
Setup
*****


ffmpeg
======
This programs depends on the ``drawtext`` ffmpeg filter.
To make this work, ffmpeg must be compiled with ``--with-freetype``.

-- https://stackoverflow.com/questions/48006872/no-such-filter-drawtext/53702852#53702852

e.g.::

    brew upgrade ffmpeg --with-freetype

grafanimate
===========
.. note::

    As Marionette for Firefox is not available for Python 3,
    this program works with Python 2 only.

::

    virtualenv --python=python2 .venv2
    source .venv2/bin/activate
    pip install grafanimate


********
Thoughts
********
Animating things in Grafana_ across the time-axis in the spirit
of the `GeoLoop Panel Plugin`_ but in a more general way has not
been unlocked for Grafana yet.

At this programs' core is the code to `set time range in Grafana`_::

    timeSrv = angular.element('grafana-app').injector().get('timeSrv');
    timeSrv.setTime({from: "2015-10-01", to: "2018-12-31"});

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
