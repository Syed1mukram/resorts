from pathlib import Path
import shutil
import subprocess

from src.image_builder import ImageBuilder
from src.video_builder import VideoBuilder
from src.scene_overlay import get_overlay


class Renderer:

    def __init__(self):
        self.images = ImageBuilder()
        self.videos = VideoBuilder()
        self.temp_dir = Path("output/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _clean(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _build(self, timeline):
        clips = []

        for i, item in enumerate(timeline):
            clip = self.temp_dir / f"{i:04d}.mp4"
            duration = float(item["duration"])

            media_type = item.get("media_type", item.get("type", "image"))
            media = item.get("media", item.get("source"))

            if not media:
                raise RuntimeError(f"Timeline item {i} has no media.")

            if media_type == "image":
                self.images.build(media, clip, duration)
            elif media_type == "video":
                self.videos.build(media, clip, duration)
            else:
                raise RuntimeError(f"Unknown media type: {media_type}")

            clips.append(clip)

        return clips

    def _concat_file(self, clips):
        concat = self.temp_dir / "concat.txt"

        with open(concat, "w", encoding="utf-8") as f:
            for clip in clips:
                f.write(f"file '{clip.resolve().as_posix()}'\n")

        return concat

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

        if not clips:
            raise RuntimeError("No clips were generated.")

        concat = self._concat_file(clips)

        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Final locked title style from scene_overlay.py.
        # It is designed to appear for the first 5 seconds.
        overlay = get_overlay(7, hotel_number, hotel_name)

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat),
            "-i", str(audio_file),

            "-vf", overlay,

            "-map", "0:v:0",
            "-map", "1:a:0",

            # Use CPU x264 for the final encode.
            # Kaggle GPU is used by the AI/CLIP stages;
            # NVENC is not assumed to be available.
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",

            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-shortest",
            "-movflags", "+faststart",

            str(output_file),
        ]

        print("\n----------------------------------------")
        print("Final rendering...")
        print(f"Hotel : NO. {hotel_number} — {hotel_name}")
        print("----------------------------------------\n")

        subprocess.run(cmd, check=True)

        print("\n----------------------------------------")
        print("Render Complete")
        print("----------------------------------------")
        print(f"Output : {output_file}")
        print("----------------------------------------\n")

        return output_file