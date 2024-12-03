# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import time
import typing as t

from munch import Munch, munchify

from grafanimate.grafana import GrafanaWrapper
from grafanimate.model import AnimationFrame, AnimationSequence

logger = logging.getLogger(__name__)


class SequentialAnimation:
    def __init__(
        self,
        grafana: GrafanaWrapper,
        dashboard_uid: t.Optional[str] = None,
        options: t.Optional[Munch] = None,
    ):
        self.grafana = grafana
        self.dashboard_uid = dashboard_uid
        self.options = options or Munch()
        self.dry_run: bool = self.options.get("dry-run", False)

    def start(self):
        self.log("Opening dashboard")
        self.grafana.open_dashboard(self.dashboard_uid, options=self.options)
        self.log("Dashboard ready")

    def log(self, message):
        logger.info(message)
        self.grafana.console_info(message)

    def run(self, sequence: AnimationSequence):
        if not isinstance(sequence, AnimationSequence):
            return

        self.log(f"Starting animation: {sequence}")

        frame: AnimationFrame
        for frame in sequence.get_frames():
            # logger.info("=" * 42)

            # Render image.
            image = self.render(frame)

            # Build item model.
            item = munchify(
                {
                    "meta": {
                        "grafana": self.grafana,
                        "scenario": self.options["scenario"],
                        "dashboard": self.dashboard_uid,
                        "every": frame.timerange.recurrence.every,
                    },
                    "data": {
                        "start": frame.timerange.start,
                        "stop": frame.timerange.stop,
                        "image": image,
                    },
                    "frame": frame,
                },
            )

            yield item

        self.log("Animation finished")

    def render(self, frame: AnimationFrame):
        logger.debug("Adjusting time range control")
        self.grafana.timewarp(frame, self.dry_run)

        logger.debug("Rendering image")
        if self.options["exposure-time"] > 0:
            logger.info(
                "Waiting for %s seconds (exposure time)",
                self.options["exposure-time"],
            )
            time.sleep(self.options["exposure-time"])

        if self.options["panel-id"]:
            logger.debug("Updating Panel Label")
            self.grafana.update_tags()
        if not self.dry_run:
            return self.make_image()

    def make_image(self):
        image = self.grafana.render_image()
        # logger.info('Image size: %s', len(image))
        return image
