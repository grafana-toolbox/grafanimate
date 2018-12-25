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

Animate all the data.


*****
About
*****
In essence, this program captures screenshots while animating
a Grafana dashboard by manipulating its `time range control`_.

The result can be saved as a series of images, an animated
gif file or as a video file. The latter optionally accepts
adding audio to support creating a lovely atmosphere when
watching the data move.


*******
Details
*******
Animating things in Grafana_ across the time-axis in the spirit
of the `GeoLoop Panel Plugin`_ has not been unlocked in a general
way. Neither Playlists_ nor `Scripted Dashboards`_ offer these
things to the user, but this program can be combined with both
to

At this programs' core is the code to `set time range in Grafana`_::

    timeSrv = angular.element('grafana-app').injector().get('timeSrv');
    timeSrv.setTime({from: "$date_range_start", to: "$date_range_end"});

Turtles all the way up, the main rendering work horse is a Firefox Browser
automated through `Marionette Python Client`_ fame:

    The Marionette Python client library allows you to remotely control
    a Gecko-based browser or device which is running a Marionette server.


****
Demo
****
Todo.


*****
Setup
*****

.. note::

    As Marionette for Firefox is not available for Python 3,
    this program works with Python 2 only.

::

    virtualenv --python=python2 .venv2
    source .venv2/bin/activate
    pip install grafanimate


*****
Usage
*****
::

    $ grafanimate --help

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


*******
License
*******
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
