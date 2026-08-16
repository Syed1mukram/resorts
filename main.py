from pathlib import Path
import argparse

from config import AUDIO_FILE, IMAGES_DIR, OUTPUT_VIDEO
from src.utils import ffmpeg_exists, ffprobe_exists, log
from src.timeline_builder import TimelineBuilder
from src.renderer import Renderer

HOTELS_FILE = Path("hotels.txt")


def load_hotels():
    if not HOTELS_FILE.exists():
        raise RuntimeError("hotels.txt not found.")

    hotels = {}

    for raw in HOTELS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue

        number, name = line.split("|", 1)
        number = number.strip()
        name = name.strip()

        if number.isdigit() and name:
            hotels[int(number)] = name

    if not hotels:
        raise RuntimeError("No hotels found in hotels.txt.")

    return hotels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hotel", type=int, default=1)
    args = parser.parse_args()

    if not ffmpeg_exists():
        raise RuntimeError("FFmpeg not found.")

    if not ffprobe_exists():
        raise RuntimeError("FFprobe not found.")

    hotels = load_hotels()

    if args.hotel not in hotels:
        raise RuntimeError(f"Hotel {args.hotel} not found in hotels.txt.")

    hotel_name = hotels[args.hotel]

    log("----------------------------------------")
    log(" Resort Video Maker — Kaggle/GPU")
    log("----------------------------------------")
    log(f"Hotel : NO. {args.hotel} — {hotel_name}")

    if not Path(AUDIO_FILE).exists():
        raise RuntimeError(f"Audio file not found: {AUDIO_FILE}")

    if not Path(IMAGES_DIR).exists():
        raise RuntimeError(f"Images directory not found: {IMAGES_DIR}")

    timeline = TimelineBuilder().build()

    if not timeline:
        raise RuntimeError("Timeline is empty.")

    print("\n========== TIMELINE ==========")
    total = 0.0

    for i, item in enumerate(timeline, 1):
        start = float(item.get("start", 0))
        duration = float(item["duration"])
        end = float(item.get("end", start + duration))
        media_type = item.get("media_type", item.get("type", "image"))
        total += duration
        print(f"{i:02d} | {media_type:5} | {start:.3f} -> {end:.3f} | {duration:.3f}")

    print("--------------------------------")
    print(f"Timeline Total : {total:.3f}")
    print("================================\n")

    output_path = Path(OUTPUT_VIDEO)
    if output_path.suffix:
        safe_name = "".join(
            c if c.isalnum() or c in " _-" else "_"
            for c in hotel_name
        ).strip().replace(" ", "_")
        output_path = output_path.parent / f"hotel_{args.hotel}_{safe_name}{output_path.suffix}"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    Renderer().render(
        timeline=timeline,
        audio_file=AUDIO_FILE,
        output_file=output_path,
        hotel_number=args.hotel,
        hotel_name=hotel_name,
    )

    log("----------------------------------------")
    log(f"Video saved : {output_path}")
    log("----------------------------------------")


if __name__ == "__main__":
    main()