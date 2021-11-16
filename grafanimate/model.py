# -*- coding: utf-8 -*-
# (c) 2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

import dateutil.parser
from dataclass_property import dataclass


class SequencingMode(Enum):
    WINDOW = "window"
    CUMULATIVE = "cumulative"


@dataclass
class AnimationSequence:
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
    steps: List[AnimationSequence]
    grafana_url: Optional[str] = None
    dashboard_uid: Optional[str] = None
    dashboard_title: Optional[str] = None
    source: Optional[str] = None


@dataclasses.dataclass
class RenderingOptions:
    video_framerate: int = 2
    video_fps: int = 25
    gif_fps: int = 10
    gif_width: int = 480
