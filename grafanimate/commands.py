# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
import os
import typing as t
from ast import literal_eval
from pathlib import Path

from docopt import DocoptExit, docopt

from grafanimate import __appname__, __version__
from grafanimate.core import get_scenario, make_grafana, run_animation_scenario
from grafanimate.media import produce_artifacts
from grafanimate.model import RenderingOptions
from grafanimate.util import asbool, normalize_options, setup_logging

if t.TYPE_CHECKING:
    from grafanimate.spool import TemporaryStorage


log = logging.getLogger(__name__)


def run():
    """
    Usage:
      grafanimate [options] [--target=<target>]...
      grafanimate --version
      grafanimate (-h | --help)

    Options:

      --scenario=<scenario>         Which scenario to run. Built-in scenarios are defined within the
                                    `scenarios.py` file, however you can easily define scenarios in
                                    custom Python files.

                                    Scenarios can be referenced by arbitrary entrypoints, like:

                                    - `--scenario=grafanimate.scenarios:playdemo`    (module, symbol)
                                    - `--scenario=grafanimate/scenarios.py:playdemo` (file, symbol)
                                    - `--scenario=playdemo` (built-in)

      --output=<path>               Output path. Required.
                                    Optionally, use environment variable `GRAFANIMATE_OUTPUT` instead.

      --grafana-url=<url>           Base URL to Grafana.
                                    If your Grafana instance is protected, please specify credentials
                                    within the URL, e.g. https://user:pass@www.example.org/grafana.

      --dashboard-uid=<uid>         Grafana dashboard UID.

    Layout and scene options:
      --window-size=<window-size>   Customize window size, e.g. `(1920, 1180)`
      --zoom-factor=<zoom-factor>   Adjust zoom factor of page. [default: 1.0]
      --use-panel-events            Whether to enable using Grafana's panel events. [default: false]
                                    Caveat: Does not work for "d-solo" panels

      --panel-id=<id>               Render single panel only by navigating to "panelId=<id>&fullscreen".
      --dashboard-view=<mode>       Use Grafana's "d-solo" view for rendering single panels without header.
                                    "d-solo" is incompatible with the "use-panel-events" option

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
      --headless                    Use headless firefox if set, else render with frontend. [default: false]
                                    Setting this to true allows to render whole dashboards.
                                    Otherwise the screensize determines the maximum height.

    Capturing options:
      --exposure-time=<seconds>     How long to wait for each frame to complete rendering. [default: 0.5]
                                    Caveat: Is ignored when use-panel-events is set

    Rendering options:
      --video-framerate=<rate>      Framerate to apply when recording the video. This value will get propagated
                                    to FFmpeg's `-framerate` parameter. [default: 2]
      --video-fps=<fps>             Frames per second to apply when recording the video. This value will get
                                    propagated into FFmpeg's output encoding options. [default: 25]
      --gif-fps=<fps>               Frames per second to apply when recording the animated gif, propagated into
                                    FFmpeg's `-filter_complex` options. [default: 10]
      --gif-width=<pixel>           Width of the gif in pixels. [default: 480]

      --dry-run                     Enable dry-run mode
      --debug                       Enable debug logging
      -h --help                     Show this screen


    Examples for scenario mode. Script your animation in file `scenarios.py`. The output files
    will be saved at `./var/spool/{scenario}/{dashboard-uid}`.

      # Use freely accessible `play.grafana.org` for demo purposes.
      grafanimate --scenario=playdemo --output=./animations

      # Example for generating Luftdaten.info graph & map.
      export GRAFANIMATE_OUTPUT=./animations
      grafanimate --grafana-url=http://localhost:3000/ --dashboard-uid=1aOmc1sik --scenario=ldi_all

      # Use more parameters to control the rendering process.
      grafanimate --grafana-url=http://localhost:3000/ --dashboard-uid=acUXbj_mz --scenario=ir_sensor_svg_pixmap --header-layout=studio --datetime-format=human-time --panel-id=6 --use-panel-events

    """

    # Parse command line arguments.
    options = docopt(run.__doc__, version=__appname__ + " " + __version__)
    options = normalize_options(options, lists=["header-layout"])

    # Setup logging.
    debug = options.get("debug")
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debug command line options.
    if debug:
        log.info(f"Options: {json.dumps(options, indent=4)}")

    # Sanity checks.
    if not options["scenario"]:
        raise DocoptExit("Error: Parameter --scenario is mandatory")

    output_path = options.output
    if not output_path:
        output_path = os.environ.get("GRAFANIMATE_OUTPUT")
    if not output_path:
        raise DocoptExit(
            "Error: Parameter --output or environment variable GRAFANIMATE_OUTPUT is mandatory",
        )

    if options["dashboard-view"] == "d-solo" and not options["panel-id"]:
        raise DocoptExit(
            "Error: Parameter --panel-id is mandatory for --dashboard-view=d-solo",
        )

    options["exposure-time"] = float(options["exposure-time"])
    options["use-panel-events"] = asbool(options["use-panel-events"])
    options["headless"] = asbool(options["headless"])
    if options["use-panel-events"]:
        options["exposure-time"] = 0
    if options["window-size"]:
        options["window-size"] = literal_eval(options["window-size"])
    if options["zoom-factor"]:
        options["zoom-factor"] = float(options["zoom-factor"])

    # Prepare rendering options.
    render_options = RenderingOptions(
        video_framerate=int(options.video_framerate),
        video_fps=int(options.video_fps),
        gif_fps=int(options.gif_fps),
        gif_width=int(options.gif_width),
    )

    # Load scene.
    scenario = get_scenario(options["scenario"])

    # Resolve URL to Grafana, either from command line (precedence), or from scenario file.
    if options["grafana-url"]:
        scenario.grafana_url = options["grafana-url"]
    if not scenario.grafana_url:
        scenario.grafana_url = "http://localhost:3000"

    # The dashboard UID can be defined either in the scenario or via command line.
    # Command line takes precedence.
    if options["dashboard-uid"]:
        scenario.dashboard_uid = options["dashboard-uid"]
    if not scenario.dashboard_uid:
        raise KeyError(
            "Dashboard UID is mandatory, either supply it on the command line or via scenario file",
        )

    # Open a Grafana site in Firefox, using Marionette.
    grafana = make_grafana(
        scenario.grafana_url,
        scenario.dashboard_uid,
        options,
        options["headless"],
    )

    # Invoke pipeline: Run stop motion animation, producing single frames.
    storage: TemporaryStorage = run_animation_scenario(
        scenario=scenario,
        grafana=grafana,
        options=options,
    )

    # Define output filename pattern.
    output = Path(output_path) / "{scenario}--{title}--{uid}.mp4"

    # Run rendering sequences, produce composite media artifacts.
    scenario.dashboard_title = grafana.get_dashboard_title()
    if not options.dry_run:
        results = produce_artifacts(
            input=storage.workdir,
            output=output,
            scenario=scenario,
            options=render_options,
        )
        log.info("Produced %s results\n%s", len(results), json.dumps(results, indent=2))
