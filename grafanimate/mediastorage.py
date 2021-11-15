# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging

from grafanimate import postprocessing
from grafanimate.util import format_date_human, slug, ensure_directory

logger = logging.getLogger(__name__)


class MediaStorage:

    def __init__(self, imagefile, outputfile):
        self.imagefile_template = imagefile
        self.outputfile_template = outputfile

    def save_items(self, results):

        for item in results:
            #logger.info('item: %s', item)
            printable = item.copy()
            printable.data.image = printable.data.image[:23] + b'...'
            logger.debug('Item: %s', printable)
            self.save_item(item)

    def save_item(self, item):

        # Compute image sequence file name.
        imagefile = self.imagefile_template.format(
            scenario=item.meta.scenario,
            interval=item.meta.interval,
            uid=item.meta.dashboard,
            dtstart=format_date_human(item.data.dtstart),
            dtuntil=format_date_human(item.data.dtuntil),
        )

        # Ensure directory exists.
        ensure_directory(imagefile)

        # Store image.
        with open(imagefile, 'wb') as f:
            f.write(item.data.image)

        logger.info('Saved frame to {}. Size: {}'.format(imagefile, len(item.data.image)))

    def produce_artifacts(self, path, uid=None, name=None):
        # TODO: Can use dashboard title as output filename here?
        # TODO: Can put dtstart into filename?

        #uid = self.dashboard_uid
        name = name or uid

        # Compute path to sequence images.
        #imagefile_pattern = self.imagefile_template.format(uid=uid, dtstart='*', dtuntil='*')
        imagefile_pattern = path

        # Compute output file name.
        if name:
            name = slug(name)
        outputfile = self.outputfile_template.format(name=name, uid=uid)

        # Produce output artifacts.
        ensure_directory(outputfile)
        return postprocessing.render(imagefile_pattern, outputfile)
