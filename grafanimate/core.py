# -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging

from furl import furl
from munch import Munch

from grafanimate.animations import SequentialAnimation
from grafanimate.grafana import GrafanaWrapper
from grafanimate.model import AnimationScenario
from grafanimate.scenarios import BuiltinScenarios
from grafanimate.mediastorage import MediaStorage
from grafanimate.util import filter_dict, as_list

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


def make_storage(imagefile=None, outputfile=None) -> MediaStorage:
    return MediaStorage(imagefile=imagefile, outputfile=outputfile)


def get_scenario(label: str) -> AnimationScenario:

    scenario = None

    # 1. Try built-in scenario methods.
    builtins = BuiltinScenarios()
    func = getattr(builtins, label, None)
    if callable(func):
        scenario = AnimationScenario(steps=as_list(func()))

    if scenario is None:
        raise NotImplementedError('Animation scenario "{}" not found or implemented'.format(label))

    return scenario


def run_animation(grafana: GrafanaWrapper, storage: MediaStorage, scenario: AnimationScenario, options: Munch):

    # Define options to be propagated to the Javascript client domain.
    animation_options = filter_dict(options, ['panel-id', 'dashboard-view', 'header-layout', 'datetime-format', 'exposure-time', 'use-panel-events', 'scenario'])

    # Start the engines.
    animation = SequentialAnimation(grafana=grafana, dashboard_uid=options['dashboard-uid'], options=animation_options)
    animation.start()

    # Run animation scenario.
    for step in scenario.steps:
        results = animation.run(step)
        storage.save_items(results)

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
