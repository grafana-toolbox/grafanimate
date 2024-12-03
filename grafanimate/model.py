# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
import logging
from collections.abc import Generator
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Union

from dateutil.rrule import rrule

from grafanimate.timeutil import (
    RecurrenceInfo,
    Timerange,
    convert_input_timestamp,
    get_freq_delta,
)

logger = logging.getLogger(__name__)


class SequencingMode(Enum):
    WINDOW = "window"
    CUMULATIVE = "cumulative"


@dataclasses.dataclass
class AnimationFrame:
    sequence: "AnimationSequence"
    timerange: Timerange


class AnimationSequence:
    def __init__(
        self,
        start: Union[datetime, int, str],
        stop: Union[datetime, int, str],
        every: Optional[str] = None,
        recurrence: Optional[RecurrenceInfo] = None,
        mode: Optional[SequencingMode] = SequencingMode.WINDOW,
    ):
        # Convert start/stop timestamps, resolving relative timestamps.
        now = datetime.now(tz=timezone.utc)
        self.start = convert_input_timestamp(start, relative_to=now)
        if isinstance(stop, str) and stop.startswith("start"):
            _stop = stop.replace("start", "")
            self.stop = convert_input_timestamp(_stop, relative_to=self.start)
        else:
            self.stop = convert_input_timestamp(stop, relative_to=now)

        # Analyze `every` parameter and converge into `RecurrenceInfo`.
        # From `every` (interval designator), compute frequency, interval and delta.
        if recurrence is not None:
            self.recurrence = recurrence
        else:
            if every is None:
                raise ValueError(
                    "Parameter `every` is mandatory when `recurrence` is not given"
                )
            self.recurrence = get_freq_delta(every)

        self.mode = mode
        self.index = None

        # Sanity checks.
        if self.start > self.stop:
            message = f"Timestamp start={self.start.isoformat()} is after stop={self.stop.isoformat()}"
            raise ValueError(message)

    def get_frames(self) -> Generator[AnimationFrame, None, None]:
        timerange = Timerange(
            start=self.start,
            stop=self.stop,
            recurrence=self.recurrence,
        )

        # until = datetime.now()
        if self.mode == SequencingMode.CUMULATIVE:
            timerange.stop += self.recurrence.duration

        # Compute complete date range.
        logger.info(
            "Creating rrule: dtstart=%s, until=%s, freq=%s, interval=%s",
            timerange.start,
            timerange.stop,
            self.recurrence.frequency,
            self.recurrence.interval,
        )
        daterange = list(
            rrule(
                dtstart=timerange.start,
                until=timerange.stop,
                freq=self.recurrence.frequency,
                interval=self.recurrence.interval,
            ),
        )
        # logger.info('Date range is: %s', daterange)

        # Iterate date range.
        for date in daterange:
            # Compute start and end dates based on mode.

            if self.mode == SequencingMode.WINDOW:
                start = date
                stop = date + self.recurrence.duration

            elif self.mode == SequencingMode.CUMULATIVE:
                start = timerange.start
                stop = date

            frame = AnimationFrame(
                sequence=self,
                timerange=Timerange(start=start, stop=stop, recurrence=self.recurrence),
            )
            yield frame

    def get_timeranges_isoformat(self) -> Generator[str, None, None]:
        for frame in self.get_frames():
            item = f"{frame.timerange.start.isoformat()}/{frame.timerange.stop.isoformat()}"
            # print(f'"{item}",')
            yield item


@dataclasses.dataclass
class AnimationScenario:
    sequences: list[AnimationSequence]
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
