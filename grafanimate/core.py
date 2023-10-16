# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import importlib
import logging
from pathlib import Path

from furl import furl
from munch import Munch

from grafanimate.animations import SequentialAnimation
from grafanimate.grafana import GrafanaWrapper
from grafanimate.model import AnimationScenario, AnimationSequence
from grafanimate.spool import TemporaryStorage
from grafanimate.util import as_list, filter_dict, import_module

log = logging.getLogger(__name__)


def make_grafana(
    url: str,
    dashboard_uid: str,
    options: dict,
    headless=False,
) -> GrafanaWrapper:
    do_login = False
    url_object = furl(url)
    if url_object.username:
        do_login = True
        username = url_object.username
        password = url_object.password
        url_object.username = None
        url_object.password = None
    url = str(url_object)

    view = "d"
    slug = "foo"
    query = ""
    if options["dashboard-view"]:
        view = options["dashboard-view"]
    if options["panel-id"]:
        if options["dashboard-view"] == "d-solo":
            query = (
                "?panelId="
                + options["panel-id"]
                + "&__feature.dashboardSceneSolo&fullscreen"
            )
        else:
            query = "?viewPanel=" + options["panel-id"]

    if url[-1] != "/":
        url += "/"
    url += view + "/" + dashboard_uid + "/" + slug + query
    log.info(f"URL: {url}")

    grafana = GrafanaWrapper(
        baseurl=str(url),
        use_panel_events=options["use-panel-events"],
        window_size=options["window-size"],
        zoom_factor=options["zoom-factor"],
    )
    grafana.boot_firefox(headless=headless)
    grafana.boot_grafana()

    if do_login:
        grafana.login(username, password)

    return grafana


def get_scenario(source: str) -> AnimationScenario:
    """
    Resolve scenario from Python module or file.
    """

    # If it's not a full-qualified reference, fall back to trying the built-in scenario methods.
    modname, _, symbol = source.partition(":")
    if not symbol:
        symbol = modname
        modname = "grafanimate.scenarios"

    # Load module and resolve symbol.
    module = load_module(modname)
    scenario: AnimationScenario = resolve_reference(module, symbol)

    if scenario is None:
        raise NotImplementedError(
            f'Animation scenario "{source}" not found or implemented',
        )

    scenario.source = source

    return scenario


def load_module(modname):
    if Path(modname).exists():
        module = import_module("<unknown>", modname)
    else:
        module = importlib.import_module(modname)
    return module


def resolve_reference(module, symbol):
    reference = getattr(module, symbol, None)
    if callable(reference):
        reference = reference()
    if isinstance(reference, AnimationScenario):
        pass
    elif isinstance(reference, (AnimationSequence, list)):
        reference = AnimationScenario(sequences=as_list(reference))
    return reference


def run_animation_scenario(
    scenario: AnimationScenario,
    grafana: GrafanaWrapper,
    options: Munch,
) -> TemporaryStorage:
    log.info(
        f"Running animation scenario at {scenario.grafana_url}, with dashboard UID {scenario.dashboard_uid}",
    )

    storage = TemporaryStorage()

    # Define options to be propagated to the Javascript client domain.
    animation_options = filter_dict(
        options,
        [
            "panel-id",
            "dashboard-view",
            "header-layout",
            "datetime-format",
            "exposure-time",
            "use-panel-events",
            "scenario",
        ],
    )

    # Start the engines.
    animation = SequentialAnimation(
        grafana=grafana,
        dashboard_uid=scenario.dashboard_uid,
        options=animation_options,
    )
    animation.start()

    # Run animation scenario.
    for index, sequence in enumerate(scenario.sequences):
        sequence.index = index  # type: ignore[assignment]  # TODO: Review.
        results = list(animation.run(sequence))
        if not options.dry_run:
            storage.save_items(results)

    return storage


def run_animation_adhoc():
    # TODO: Introduce ad-hoc mode. In the meanwhile, please use scenario mode.
    """
    animator = SequentialAnimation(
        options['url'],
        time_start=options.get('start'),
        time_end=options.get('end', 'now'),
        time_step=options.get('every', '1h')
    )
    animator.run()
    """
