# (c) 2018-2021 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import os.path
import shutil
from tempfile import mkdtemp

from grafanimate.timeutil import format_date_filename

logger = logging.getLogger(__name__)


class TemporaryStorage:
    def __init__(self):
        self.workdir = mkdtemp()
        self.imagefile_template = "{uid}_{seq}_{start}_{stop}.png"

    def save_items(self, results) -> list[str]:
        files = []
        for item in results:
            # logger.info('item: %s', item)
            printable = item.copy()
            printable.data.image = printable.data.image[:23] + b"..."
            logger.debug("Item: %s", printable)
            files.append(self.save_item(item))
        return files

    def save_item(self, item) -> str:
        # Compute image sequence file name.
        imagename = self.imagefile_template.format(
            uid=item.meta.dashboard,
            seq=str(item.frame.sequence.index).zfill(4),
            start=format_date_filename(item.data.start),
            stop=format_date_filename(item.data.stop),
        )

        imagefile = os.path.join(self.workdir, imagename)

        # Store image.
        with open(imagefile, "wb") as f:
            f.write(item.data.image)

        logger.info(f"Saved frame to {imagefile} (size={len(item.data.image)})")

        return imagefile

    def __del__(self):
        shutil.rmtree(self.workdir)
