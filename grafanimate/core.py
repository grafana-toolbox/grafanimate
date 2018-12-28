# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging

from grafanimate.grafana import GrafanaWrapper
from grafanimate.scenarios import AnimationScenario
from grafanimate.util import filter_dict

log = logging.getLogger(__name__)


def make_grafana(url):
    grafana = GrafanaWrapper(baseurl=url)
    grafana.boot_firefox(headless=False)
    grafana.boot_grafana()
    return grafana


def make_animation(grafana, options):

    # Prepare animation.
    scenario = AnimationScenario(
        grafana=grafana,
        dashboard_uid=options['dashboard-uid'],
        options=filter_dict(options, ['panel-id', 'dashboard-view', 'header-layout', 'datetime-format'])
    )
    if not hasattr(scenario, options.scenario):
        raise NotImplementedError('Animation scenario "{}" not implemented'.format(options.scenario))

    # Run animation scenario.
    func = getattr(scenario, options.scenario)
    return func


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
