from pathlib import Path

from config import (
    AUDIO_FILE,
    OUTPUT_VIDEO,
)

from src.utils import (
    ffmpeg_exists,
    ffprobe_exists,
    log,
)

from src.timeline_builder import TimelineBuilder
from src.renderer import Renderer


def main():

    if not ffmpeg_exists():
        raise RuntimeError("FFmpeg not found.")

    if not ffprobe_exists():
        raise RuntimeError("FFprobe not found.")

    log("----------------------------------------")
    log(" Resort Video Maker")
    log("----------------------------------------")

    builder = TimelineBuilder()

    timeline = builder.build()

    if not timeline:
        raise RuntimeError("Timeline is empty.")

    output_path = Path(OUTPUT_VIDEO)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    renderer = Renderer()

    renderer.render(
        timeline=timeline,
        audio_file=AUDIO_FILE,
        output_file=output_path
    )

    log("----------------------------------------")
    log(f"Video saved : {output_path}")
    log("----------------------------------------")


if __name__ == "__main__":
    main()