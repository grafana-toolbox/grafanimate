# (c) 2018-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
import os

from grafanimate.model import RenderingOptions

logger = logging.getLogger(__name__)


class MediaProducer:
    def __init__(self, options: RenderingOptions):
        self.options = options

    def to_video(self, source, target):
        """
        http://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/
        https://stackoverflow.com/questions/24961127/how-to-create-a-video-from-images-with-ffmpeg

        https://stackoverflow.com/questions/38726370/ffmpeg-text-watermark-bottom-left/38728172#38728172
        https://superuser.com/questions/939357/ffmpeg-watermark-on-bottom-right-corner/939386#939386
        """
        # command = "ffmpeg -framerate 4 -pattern_type glob -i '{}' -c:v libx264 -r 30 -pix_fmt yuv420p '{}' -y".format(source, target)
        # -vf "fps=25,format=yuv420p,drawtext=fontfile=OpenSans-Regular.ttf:text='Title of this Video':fontcolor=white:fontsize=24:x=(w-tw)/2:y=(h/PHI)+th
        # command = "ffmpeg -framerate 4 -pattern_type glob -i '{}' -c:v libx264 -vf 'fps=25,format=yuv420p,drawtext=text=Produced with Grafana and grafanimate:fontsize=11:x=w-tw-30:y=h-th-10:fontcolor=lightgrey:fontfile=/Library/Fonts/Arial.ttf' '{}' -y".format(source, target)

        # TODO: Expose `-framerate` and `fps` values.
        # use the `pad` option to avoid ffmpeg errors like 'height not divisible by 2'
        command = f"ffmpeg -framerate {self.options.video_framerate} -pattern_type glob -i '{source}' -c:v libx264 -vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2,fps={self.options.video_fps},format=yuv420p' '{target}' -y"
        logger.info(f"Rendering video: {target}")
        logger.debug(command)
        os.system(command)  # noqa: S605

    def to_gif(self, source, target):
        """
        # High Quality Gifs with FFmpeg
        # https://medium.com/@colten_jackson/doing-the-gif-thing-on-debian-82b9760a8483
        ::

            ffmpeg -ss 2.6 -t 1.3 -i MVI_7035.MOV \
                -vf fps=15,scale=320:-1:flags=lanczos,palettegen palette.png

            ffmpeg -ss 2.6 -t 1.3 -i MVI_7035.MOV -i palette.png \
                -filter_complex "fps=15,scale=400:-1:flags=lanczos[x];[x][1:v]paletteuse" sixthtry.gif

        > I think the -1 in the video filters refers to the height and basically means ‘preserve aspect ratio’.
        > So, in this case, 320:-1 means scale to: w=320, h=320/CurrentWidth*CurrentHeight

        # How to make GIFs with FFmpeg
        https://engineering.giphy.com/how-to-make-gifs-with-ffmpeg/

        # How do I convert a video to GIF using FFmpeg, with reasonable quality?
        https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality

        # High quality GIF with FFmpeg
        http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html

        # FFmpeg gif script for bash
        https://github.com/thevangelist/FFMPEG-gif-script-for-bash

        > Here is a better version with fifo filter to avoid Buffer queue overflow when using paletteuse filter.
        > By using split filter to avoid the creation of intermediate palette PNG file.
        > -- https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality/1256459#1256459

        ffmpeg -i input.mp4 -filter_complex 'fps=10,scale=320:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse' out.gif
        """

        """
        # PoC
        ffmpeg -i dwd-cdc-2018-08.mov -vf fps=15,scale=320:-1:flags=lanczos,palettegen palette.png
        ffmpeg -i dwd-cdc-2018-08.mov -i palette.png -filter_complex "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" dwd-cdc-2018-08.gif -y
        """

        """
        # One-step conversion.
        ffmpeg -ss $START -i $IN_URL -t $LENGTH -filter_complex "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,split=2 [a][b]; [a] palettegen [pal]; [b] [pal] paletteuse" out.gif
        ffmpeg -i dwd-cdc-2018-08.mov -filter_complex 'fps=10,scale=480:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse' dwd-cdc-2018-08-v2.gif -y
        """

        # TODO: Expose `fps` and `scale` values.
        command = f"ffmpeg -i '{source}' -filter_complex 'fps={self.options.gif_fps},scale={self.options.gif_width}:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] [p] paletteuse' '{target}' -y"
        logger.info("Rendering GIF: %s", target)
        logger.debug(command)
        os.system(command)  # noqa: S605

    def upload_server(self, source):
        command = f"make --makefile=/Users/amo/dev/hiveeyes/sources/documentation/Makefile ptrace source={source}"
        os.system(command)  # noqa: S605

    def render(self, source, target):
        mp4 = target
        suffix = "." + target.split(".")[-1]
        gif = mp4.replace(suffix, ".gif")
        self.to_video(source, mp4)
        self.to_gif(mp4, gif)
        results = [mp4, gif]
        return results


def run(source, target):
    renderer = MediaProducer(options=RenderingOptions())
    renderer.render(source, target)
    # upload_server(gif)
    # upload_server(mp4)


if __name__ == "__main__":
    run("./var/spool/*_1aOmc1sik_*.png", "./var/results/ldi-coverage.mp4")

    # to_video('./var/spool/*_1aOmc1sik_*.png', 'ldi-coverage.mp4')
    # to_gif('ldi-coverage.mp4', 'ldi-coverage.gif')
    # upload_server('ldi-coverage.gif')
    # upload_server('ldi-coverage.mp4')
