from pathlib import Path
from collections import OrderedDict

from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher


BASE_DIR = Path("input/images")

# Minimum CLIP similarity required.
MIN_SCORE = 0.18

# Don't keep the same image for every nearby segment
RECENT_WINDOW = 3


def find_hotels():
    hotels = []

    if not BASE_DIR.exists():
        raise RuntimeError(f"Missing folder: {BASE_DIR}")

    for folder in BASE_DIR.iterdir():
        if not folder.is_dir():
            continue

        voice = folder / "voice.mp3"
        images = folder / "images"

        if voice.exists() and images.exists():
            hotels.append(folder)

    def sort_key(path):
        try:
            return (0, int(path.name))
        except ValueError:
            return (1, path.name.lower())

    return sorted(hotels, key=sort_key)


def select_hotel(hotel_dir):

    voice_file = hotel_dir / "voice.mp3"
    images_dir = hotel_dir / "images"

    print("\n" + "=" * 60)
    print(f"HOTEL {hotel_dir.name}")
    print("=" * 60)

    # ---------------------------------------------------------
    # TRANSCRIPT
    # ---------------------------------------------------------

    print("\n[1/3] Generating transcript...")

    transcript = TranscriptGenerator()
    segments = transcript.transcribe(voice_file)

    # ---------------------------------------------------------
    # CLIP
    # ---------------------------------------------------------

    print("\n[2/3] Indexing images...")

    matcher = ImageMatcher()
    matcher.index_images(images_dir)

    # ---------------------------------------------------------
    # SELECTION
    # ---------------------------------------------------------

    print("\n[3/3] Selecting useful images...\n")

    selected = OrderedDict()
    recent_images = []

    for segment in segments:

        text = segment["text"].strip()

        if not text:
            continue

        result = matcher.find_best(text)

        if not result:
            print(f"SKIP | {text}")
            continue

        image_path, score = result
        image_path = Path(image_path)
        score = float(score)

        # Weak match = don't force an image
        if score < MIN_SCORE:
            print(
                f"SKIP WEAK | {image_path.name} "
                f"| {score:.3f} | {text}"
            )
            continue

        # Don't repeatedly use the same image in nearby segments
        if image_path in recent_images:

            # If the image was already selected, don't create
            # another entry for it.
            print(
                f"REUSE | {image_path.name} "
                f"| {score:.3f} | {text}"
            )
            continue

        # New useful image
        selected[image_path] = {
            "score": score,
            "text": text,
            "start": float(segment["start"]),
            "end": float(segment["end"]),
        }

        recent_images.append(image_path)

        if len(recent_images) > RECENT_WINDOW:
            recent_images.pop(0)

        print(
            f"{len(selected):02d}. "
            f"{image_path.name} "
            f"| {score:.3f} "
            f"| {text}"
        )

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    output_file = Path(
        f"selected_images_{hotel_dir.name}.txt"
    )

    with output_file.open("w", encoding="utf-8") as f:

        f.write(f"HOTEL {hotel_dir.name}\n")
        f.write("=" * 70 + "\n\n")

        for number, (image, data) in enumerate(
            selected.items(),
            start=1
        ):

            f.write(
                f"{number:02d} | "
                f"{image.name} | "
                f"score={data['score']:.3f} | "
                f"{data['start']:.2f}-{data['end']:.2f} | "
                f"{data['text']}\n"
            )

    print("\n----------------------------------------")
    print(
        f"Selected images : {len(selected)}"
    )
    print(
        f"Saved           : {output_file}"
    )
    print("----------------------------------------")


def main():

    hotels = find_hotels()

    if not hotels:
        raise RuntimeError(
            "No hotel folders found."
        )

    print(
        f"Found {len(hotels)} hotel(s)."
    )

    for hotel in hotels:
        select_hotel(hotel)

    print("\n========================================")
    print("IMAGE SELECTION COMPLETE")
    print("========================================")


if __name__ == "__main__":
    main()