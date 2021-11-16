# -*- coding: utf-8 -*-
# (c) 2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
from datetime import datetime
from enum import Enum
from typing import List, Optional


class SequencingMode(Enum):
    WINDOW = "window"
    CUMULATIVE = "cumulative"


@dataclasses.dataclass
class AnimationStep:
    dtstart: datetime
    dtuntil: datetime
    interval: str
    mode: Optional[SequencingMode] = SequencingMode.WINDOW


@dataclasses.dataclass
class AnimationScenario:
    steps: List[AnimationStep]
    grafana_url: Optional[str] = None
    dashboard_uid: Optional[str] = None
