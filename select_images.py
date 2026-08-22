from pathlib import Path
from collections import OrderedDict

from config import AUDIO_FILE, IMAGES_DIR
from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher


OUTPUT_FILE = Path("selected_images.txt")


def main():
    print("----------------------------------------")
    print(" IMAGE SELECTION ONLY")
    print("----------------------------------------")

    # 1. Transcribe narration
    print("\n[1/3] Generating transcript...")
    transcript = TranscriptGenerator()
    segments = transcript.transcribe(AUDIO_FILE)

    # 2. Load the SAME CLIP image matcher
    print("\n[2/3] Indexing images...")
    matcher = ImageMatcher()
    matcher.index_images(IMAGES_DIR)

    # Keep unique images while preserving first-use order
    selected = OrderedDict()

    print("\n[3/3] Selecting images...\n")

    for i, segment in enumerate(segments):
        text = segment["text"].strip()

        if not text:
            continue

        result = matcher.find_best(text)

        if not result:
            continue

        image, score = result

        if image is None:
            continue

        image = Path(image)

        if image not in selected:
            selected[image] = {
                "score": float(score),
                "text": text,
            }

            print(
                f"{len(selected):02d}. "
                f"{image.name} "
                f"(score={float(score):.3f})"
            )

    # Save selected filenames
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write("SELECTED IMAGES\n")
        f.write("=" * 60 + "\n\n")

        for number, (image, data) in enumerate(
            selected.items(), start=1
        ):
            f.write(
                f"{number:02d} | "
                f"{image.name} | "
                f"score={data['score']:.3f}\n"
            )

    print("\n----------------------------------------")
    print(f"Total unique images selected : {len(selected)}")
    print(f"Saved list                    : {OUTPUT_FILE}")
    print("----------------------------------------")


if __name__ == "__main__":
    main()