from pathlib import Path
import shutil
import subprocess

from src.image_builder import ImageBuilder
from src.video_builder import VideoBuilder
from src.title_overlay import TitleOverlay


class Renderer:

    def __init__(self):

        self.images = ImageBuilder()
        self.videos = VideoBuilder()
        self.title_overlay = TitleOverlay()

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
        hotel_number,
        hotel_name,
    ):

        self._clean()

        clips = self._build(timeline)

        concat = self._concat_file(clips)

        overlay_file = self.temp_dir / "title_overlay.png"

        self.title_overlay.create(
            hotel_number=hotel_number,
            hotel_name=hotel_name,
            output_file=overlay_file
        )

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cmd = [

            "ffmpeg",
            "-y",

            # Main video
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),

            # Audio
            "-i",
            str(audio_file),

            # Transparent title overlay PNG
            "-loop",
            "1",
            "-i",
            str(overlay_file),

            # Overlay ONLY during first 3 seconds
            "-filter_complex",
            "[0:v][2:v]overlay=0:0:enable='between(t,0,3)'[v]",

            "-map",
            "[v]",

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

            "-shortest",

            "-movflags",
            "+faststart",

            str(output_file)
        ]

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