# -*- coding: utf-8 -*-
# (c) 2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses

import dateutil.parser
from dataclass_property import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union


class SequencingMode(Enum):
    WINDOW = "window"
    CUMULATIVE = "cumulative"


@dataclass
class AnimationStep:
    interval: str
    mode: Optional[SequencingMode] = SequencingMode.WINDOW
    milliseconds: int = 0

    @property
    def dtstart(self) -> datetime:
        return self._dtstart

    @property
    def dtuntil(self) -> datetime:
        return self._dtuntil

    @dtstart.setter
    def dtstart(self, value: Union[datetime, str]):
        self._dtstart = self.convert_timestamp(value)

    @dtuntil.setter
    def dtuntil(self, value: Union[datetime, str]):
        self._dtuntil = self.convert_timestamp(value)

    def convert_timestamp(self, value: Union[datetime, str]) -> datetime:
        if isinstance(value, datetime):
            pass
        elif isinstance(value, int):
            value = datetime.fromtimestamp(value)
        elif isinstance(value, str):
            value = dateutil.parser.parse(value)
        else:
            raise TypeError("Unknown data type for `dtstart` or `dtuntil` value: {} ({})".format(value, type(value)))
        return value


@dataclasses.dataclass
class AnimationScenario:
    steps: List[AnimationStep]
    grafana_url: Optional[str] = None
    dashboard_uid: Optional[str] = None
