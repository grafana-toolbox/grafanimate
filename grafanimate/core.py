# -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
from pathlib import Path

import pkg_resources
from furl import furl
from munch import Munch

from grafanimate.animations import SequentialAnimation
from grafanimate.grafana import GrafanaWrapper
from grafanimate.model import AnimationScenario, AnimationSequence
from grafanimate.spool import TemporaryStorage
from grafanimate.util import as_list, filter_dict, import_module

log = logging.getLogger(__name__)


def make_grafana(url, use_panel_events) -> GrafanaWrapper:

    do_login = False
    url = furl(url)
    if url.username:
        do_login = True
        username = url.username
        password = url.password
        url.username = None
        url.password = None

    grafana = GrafanaWrapper(baseurl=str(url), use_panel_events=use_panel_events)
    grafana.boot_firefox(headless=False)
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
        raise NotImplementedError('Animation scenario "{}" not found or implemented'.format(source))

    scenario.source = source

    return scenario


def load_module(modname):
    if Path(modname).exists():
        module = import_module("<unknown>", modname)
    else:
        module = pkg_resources.EntryPoint(None, modname).resolve()
    return module


def resolve_reference(module, symbol):
    reference = getattr(module, symbol, None)
    if callable(reference):
        reference = reference()
    if isinstance(reference, AnimationScenario):
        pass
    elif isinstance(reference, (AnimationSequence, list)):
        reference = AnimationScenario(steps=as_list(reference))
    return reference


def run_animation_scenario(scenario: AnimationScenario, grafana: GrafanaWrapper, options: Munch) -> TemporaryStorage:

    log.info("Running animation scenario {}".format(scenario))

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
    animation = SequentialAnimation(grafana=grafana, dashboard_uid=scenario.dashboard_uid, options=animation_options)
    animation.start()

    # Run animation scenario.
    for step in scenario.steps:
        results = animation.run(step)
        storage.save_items(results)

    return storage


def run_animation_adhoc():
    # TODO: Introduce ad-hoc mode. In the meanwhile, please use scenario mode.
    """
    animator = SequentialAnimation(
        options['url'],
        time_start=options.get('start'),
        time_end=options.get('end', 'now'),
        time_step=options.get('interval', '1h')
    )
    animator.run()
    """
    pass
