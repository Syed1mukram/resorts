from pathlib import Path

from config import HOTELS_DIR, OUTPUT_DIR

from src.utils import ffmpeg_exists, ffprobe_exists, log
from src.timeline_builder import TimelineBuilder
from src.renderer import Renderer


TITLE_FILE = Path("input/title.txt")


def load_hotel_names():
    hotels = {}

    if not TITLE_FILE.exists():
        raise RuntimeError(f"Title file not found: {TITLE_FILE}")

    for raw in TITLE_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()

        if not line or "|" not in line:
            continue

        number, name = line.split("|", 1)
        number = number.strip()
        name = name.strip()

        if number.isdigit() and name:
            hotels[int(number)] = name

    if not hotels:
        raise RuntimeError(f"No hotel names found in {TITLE_FILE}")

    return hotels


def main():
    if not ffmpeg_exists():
        raise RuntimeError("FFmpeg not found.")

    if not ffprobe_exists():
        raise RuntimeError("FFprobe not found.")

    hotels = load_hotel_names()

    log("----------------------------------------")
    log(" Resort Video Maker - Multi Hotel")
    log("----------------------------------------")

    hotel_folders = [
        p for p in HOTELS_DIR.iterdir()
        if p.is_dir() and p.name.isdigit()
    ]

    hotel_folders.sort(key=lambda p: int(p.name))

    if not hotel_folders:
        raise RuntimeError(
            f"No numbered hotel folders found in {HOTELS_DIR}"
        )

    for hotel_dir in hotel_folders:
        hotel_number = int(hotel_dir.name)

        audio_file = hotel_dir / "voice.mp3"
        images_dir = hotel_dir / "images"

        hotel_name = hotels.get(
            hotel_number,
            f"Hotel {hotel_number}"
        )

        log("----------------------------------------")
        log(f"Hotel : NO. {hotel_number} — {hotel_name}")
        log(f"Voice : {audio_file}")
        log(f"Images: {images_dir}")
        log("----------------------------------------")

        if not audio_file.exists():
            log(
                f"SKIPPED Hotel #{hotel_number}: "
                f"voice.mp3 missing"
            )
            continue

        if not images_dir.exists():
            log(
                f"SKIPPED Hotel #{hotel_number}: "
                f"images folder missing"
            )
            continue

        builder = TimelineBuilder(
            audio_file=audio_file,
            images_dir=images_dir
        )

        timeline = builder.build()

        if not timeline:
            log(
                f"SKIPPED Hotel #{hotel_number}: "
                f"timeline empty"
            )
            continue

        safe_name = "".join(
            c if c.isalnum() or c in " _-" else "_"
            for c in hotel_name
        ).strip().replace(" ", "_")

        output_path = (
            Path(OUTPUT_DIR)
            / f"hotel_{hotel_number}_{safe_name}.mp4"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        Renderer().render(
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

    log("----------------------------------------")
    log(" ALL HOTELS COMPLETE")
    log("----------------------------------------")


if __name__ == "__main__":
    main()