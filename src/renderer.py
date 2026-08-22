from pathlib import Path
import shutil
import subprocess

from src.image_builder import ImageBuilder
from src.video_builder import VideoBuilder


class Renderer:

    def __init__(self):

        self.images = ImageBuilder()
        self.videos = VideoBuilder()

        self.temp_dir = Path("output/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------

    def _clean(self):

        if self.temp_dir.exists():

            shutil.rmtree(self.temp_dir)

        self.temp_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------------------------------

    def _build(self, timeline):

        clips = []

        for i, item in enumerate(timeline):

            clip = self.temp_dir / f"{i:04d}.mp4"

            duration = float(item["duration"])

            if item["media_type"] == "image":

                self.images.build(
                    item["media"],
                    clip,
                    duration
                )

            else:

                self.videos.build(
                    item["media"],
                    clip,
                    duration
                )

            clips.append(clip)

        return clips
    # ---------------------------------------------------------

    def _concat_file(self, clips):

        concat = self.temp_dir / "concat.txt"

        with open(concat, "w", encoding="utf-8") as f:

            for clip in clips:

                f.write(
                    f"file '{clip.resolve().as_posix()}'\n"
                )

        return concat

    # ---------------------------------------------------------

    def render(

        self,

        timeline,

        audio_file,

        output_file,

    ):

        self._clean()

        clips = self._build(timeline)

        concat = self._concat_file(clips)

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ---------------------------------------------------------
        # Optional 5-second hotel title
        # ---------------------------------------------------------
        title_file = Path(audio_file).parent / "title.txt"
        hotel_name = (
            title_file.read_text(encoding="utf-8").strip()
            if title_file.exists()
            else f"Hotel {hotel_number or ''}".strip()
        )

        if test_duration is not None:
            # Keep only the requested test duration.
            test_duration = min(float(test_duration), 10.0)

        font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

        def esc(value):
            return (
                str(value)
                .replace("\\", "\\\\")
                .replace(":", "\\:")
                .replace("'", "\\'")
                .replace(",", "\\,")
            )

        title_filter = (
            "drawbox=x=70:y=410:w=8:h=190:"
            "color=00AEEF:t=fill:"
            "enable='between(t,0,5)',"
            f"drawtext=fontfile='{font}':"
            f"text='NO. {esc(hotel_number or '')}':"
            "x=110:y=410:fontsize=48:"
            "fontcolor=white:"
            "enable='between(t,0,5)':"
            "alpha='if(lt(t,0.35),t/0.35,if(gt(t,4.5),(5-t)/0.5,1))',"
            f"drawtext=fontfile='{font}':"
            f"text='{esc(hotel_name.upper())}':"
            "x=110:y=485:fontsize=52:"
            "fontcolor=FFD21F:"
            "enable='between(t,0,5)':"
            "alpha='if(lt(t,0.35),t/0.35,if(gt(t,4.5),(5-t)/0.5,1))'"
        )

        cmd = [

            "ffmpeg",

            "-y",

            "-f",
            "concat",

            "-safe",
            "0",

            "-i",
            str(concat),

            "-i",
            str(audio_file),

            "-vf",
            title_filter,
            "-map",
            "0:v:0",

            "-map",
            "1:a:0",

            "-c:v",
            "h264_nvenc",

            "-preset",
            "medium",

            "-cq",
            "22",

            "-pix_fmt",
            "yuv420p",

            "-r",
            "30",

            "-vsync",
            "cfr",

            "-c:a",
            "aac",

            "-b:a",
            "192k",

            "-ar",
            "48000",

            "-movflags",
            "+faststart",

            str(output_file)

        ]

        if test_duration is not None:
            cmd.insert(cmd.index("-c:v"), "-t")
            cmd.insert(cmd.index("-c:v"), f"{test_duration:.3f}")

        subprocess.run(
            cmd,
            check=True
        )
        print("\n----------------------------------------")
        print("Cleaning temporary files...")
        print("----------------------------------------")

        # try:
        #     shutil.rmtree(self.temp_dir)
        # except Exception:
        #     pass

        print("\n----------------------------------------")
        print("Render Complete")
        print("----------------------------------------")
        print(f"Output : {output_file}")

        return output_file