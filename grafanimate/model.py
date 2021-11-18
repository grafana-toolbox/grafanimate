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
    def start(self) -> datetime:
        return self._start

    @property
    def stop(self) -> datetime:
        return self._stop

    @start.setter
    def start(self, value: Union[datetime, str]):
        self._start = self.convert_timestamp(value)

    @stop.setter
    def stop(self, value: Union[datetime, str]):
        self._stop = self.convert_timestamp(value)

    def convert_timestamp(self, value: Union[datetime, str]) -> datetime:
        if isinstance(value, datetime):
            pass
        elif isinstance(value, int):
            value = datetime.fromtimestamp(value)
        elif isinstance(value, str):
            value = dateutil.parser.parse(value)
        else:
            raise TypeError("Unknown data type for `start` or `stop` value: {} ({})".format(value, type(value)))
        return value


@dataclasses.dataclass
class AnimationScenario:
    sequences: List[AnimationSequence]
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
