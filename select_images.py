from pathlib import Path
from collections import OrderedDict

from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher


BASE_DIR = Path("input/images")


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

    return sorted(hotels, key=lambda x: int(x.name) if x.name.isdigit() else x.name)


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
    # SELECT
    # ---------------------------------------------------------

    print("\n[3/3] Selecting images...")

    selected = OrderedDict()

    for segment in segments:

        text = segment["text"].strip()

        if not text:
            continue

        result = matcher.find_best(text)

        if not result:
            continue

        image_path, score = result

        image_path = Path(image_path)

        # Unique images only
        if image_path not in selected:

            selected[image_path] = {
                "score": float(score),
                "text": text,
                "start": float(segment["start"]),
                "end": float(segment["end"]),
            }

            print(
                f"{len(selected):02d}. "
                f"{image_path.name} "
                f"| {float(score):.3f} "
                f"| {text}"
            )

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    output_file = Path(
        f"selected_images_{hotel_dir.name}.txt"
    )

    with output_file.open("w", encoding="utf-8") as f:

        f.write(
            f"HOTEL {hotel_dir.name}\n"
        )

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
        f"Selected unique images : {len(selected)}"
    )
    print(
        f"Saved                  : {output_file}"
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