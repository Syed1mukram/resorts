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

    # ======================================================
    # CHECK FFMPEG
    # ======================================================

    if not ffmpeg_exists():
        raise RuntimeError("FFmpeg not found.")

    if not ffprobe_exists():
        raise RuntimeError("FFprobe not found.")

    log("----------------------------------------")
    log(" Resort Video Maker - Multi Hotel")
    log("----------------------------------------")

    # ======================================================
    # FIND HOTEL FOLDERS
    # ======================================================

    hotel_folders = [
        p
        for p in HOTELS_DIR.iterdir()
        if p.is_dir() and p.name.isdigit()
    ]

    # Countdown:
    # 11 -> 10 -> 9 -> ... -> 1

    hotel_folders.sort(
        key=lambda p: int(p.name),
        reverse=True
    )

    if not hotel_folders:
        raise RuntimeError(
            f"No numbered hotel folders found in: {HOTELS_DIR}"
        )

    renderer = Renderer()

    # ======================================================
    # PROCESS EACH HOTEL
    # ======================================================

    for hotel_dir in hotel_folders:

        hotel_number = hotel_dir.name

        audio_file = hotel_dir / "voice.mp3"
        images_dir = hotel_dir / "images"
        title_file = hotel_dir / "title.txt"

        # --------------------------------------------------
        # HOTEL NAME
        # --------------------------------------------------

        if title_file.exists():

            hotel_name = title_file.read_text(
                encoding="utf-8"
            ).strip()

        else:

            hotel_name = f"Hotel {hotel_number}"

        # --------------------------------------------------
        # LOG
        # --------------------------------------------------

        log("----------------------------------------")
        log(f" Processing Hotel #{hotel_number}")
        log(f" Name   : {hotel_name}")
        log(f" Voice  : {audio_file}")
        log(f" Images : {images_dir}")
        log("----------------------------------------")

        # --------------------------------------------------
        # CHECK FILES
        # --------------------------------------------------

        if not audio_file.exists():

            log(
                f"SKIPPED Hotel #{hotel_number}: "
                "voice.mp3 missing"
            )

            continue

        if not images_dir.exists():

            log(
                f"SKIPPED Hotel #{hotel_number}: "
                "images folder missing"
            )

            continue

        # ==================================================
        # BUILD TIMELINE
        # ==================================================

        builder = TimelineBuilder(
            audio_file=audio_file,
            images_dir=images_dir
        )

        timeline = builder.build()

        if not timeline:

            log(
                f"SKIPPED Hotel #{hotel_number}: "
                "timeline empty"
            )

            continue

        # ==================================================
        # OUTPUT
        # ==================================================

        output_path = (
            Path(OUTPUT_DIR)
            / f"hotel_{hotel_number}.mp4"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # RENDER
        # ==================================================

        renderer.render(
            timeline=timeline,
            audio_file=audio_file,
            output_file=output_path,
            hotel_number=hotel_number,
            hotel_name=hotel_name,
        )

        log("----------------------------------------")
        log(
            f"Hotel #{hotel_number} saved : "
            f"{output_path}"
        )
        log("----------------------------------------")

    # ======================================================
    # COMPLETE
    # ======================================================

    log("----------------------------------------")
    log(" ALL HOTELS COMPLETE")
    log("----------------------------------------")


if __name__ == "__main__":
    main()