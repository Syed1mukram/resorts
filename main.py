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


    print("\n========== TIMELINE ==========")
    total = 0.0
    for i, item in enumerate(timeline):
        d = float(item["duration"])
        total += d
        print(f"{i:02d} | {item['media_type']:5} | {d:.3f}")
    print(f"\nTOTAL TIMELINE = {total:.3f} sec")
    print("==============================\n")

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