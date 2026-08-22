from pathlib import Path

from config import (
    HOTELS_DIR,
    OUTPUT_DIR,
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
    log(" Resort Video Maker - Multi Hotel")
    log("----------------------------------------")

    # Find numbered hotel folders
    hotel_folders = [
        p for p in HOTELS_DIR.iterdir()
        if p.is_dir() and p.name.isdigit()
    ]

    # Countdown order: 9 -> 1
    hotel_folders.sort(
        key=lambda p: int(p.name),
        reverse=True
    )

    if not hotel_folders:
        raise RuntimeError("No hotel folders found.")

    renderer = Renderer()

    for hotel_dir in hotel_folders:

        hotel_number = hotel_dir.name

        audio_file = hotel_dir / "voice.mp3"
        images_dir = hotel_dir / "images"

        log("----------------------------------------")
        log(f" Processing Hotel #{hotel_number}")
        log(f" Voice  : {audio_file}")
        log(f" Images : {images_dir}")
        log("----------------------------------------")

        if not audio_file.exists():
            log(f"SKIPPED Hotel #{hotel_number}: voice.mp3 missing")
            continue

        if not images_dir.exists():
            log(f"SKIPPED Hotel #{hotel_number}: images folder missing")
            continue

        builder = TimelineBuilder(
            audio_file=audio_file,
            images_dir=images_dir
        )

        timeline = builder.build()

        if not timeline:
            log(f"SKIPPED Hotel #{hotel_number}: timeline empty")
            continue

        output_path = (
            Path(OUTPUT_DIR)
            / f"hotel_{hotel_number}.mp4"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        renderer.render(
            timeline=timeline,
            audio_file=audio_file,
            output_file=output_path,
            hotel_number=hotel_number,
            test_duration=10
        )

        log(
            f"Hotel #{hotel_number} saved : "
            f"{output_path}"
        )

    log("----------------------------------------")
    log(" ALL HOTELS COMPLETE")
    log("----------------------------------------")


if __name__ == "__main__":
    main()