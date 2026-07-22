from collections import deque
import math

from config import (
    AUDIO_FILE,
    IMAGES_DIR,
)

from src.utils import log
from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher
from src.pexels_api import PexelsAPI


WINDOW_DURATION = 5.0
VIDEO_RATIO = 0.35
VIDEO_COOLDOWN = 4


class TimelineBuilder:

    def __init__(self):

        self.transcript = TranscriptGenerator()
        self.matcher = ImageMatcher()
        self.pexels = PexelsAPI()

        self.used_images = deque(maxlen=5)
        self.used_videos = deque(maxlen=VIDEO_COOLDOWN)

    # -----------------------------------------------------

    def _audio_length(self, segments):

        if not segments:
            return 0.0

        return float(segments[-1]["end"])

    # -----------------------------------------------------

    def _window_text(

        self,
        segments,
        start,
        end

    ):

        parts = []

        for seg in segments:

            if seg["end"] <= start:
                continue

            if seg["start"] >= end:
                break

            parts.append(seg["text"])

        return " ".join(parts).strip()
    # -----------------------------------------------------

    def build(self):

        log("Generating transcript...")

        segments = self.transcript.transcribe(
            AUDIO_FILE
        )

        log("Indexing images...")

        self.matcher.index_images(
            IMAGES_DIR
        )

        audio_length = self._audio_length(
            segments
        )

        total_windows = math.ceil(
            audio_length / WINDOW_DURATION
        )

        timeline = []

        image_count = 0
        video_count = 0

        next_video = 3

        last_media = None
        last_type = "image"

        for index in range(total_windows):

            start = index * WINDOW_DURATION

            end = min(
                audio_length,
                start + WINDOW_DURATION
            )

            duration = end - start

            text = self._window_text(

                segments,

                start,

                end,

            )

            if not text and timeline:

                text = timeline[-1]["text"]

            use_video = (

                index >= next_video

                and

                video_count <

                int(
                    total_windows * VIDEO_RATIO
                )

            )

            media = None
            media_type = "image"
            # -----------------------------------------
            # VIDEO
            # -----------------------------------------

            if use_video:

                video = self.pexels.download(
                    text
                )

                if (
                    video
                    and
                    video not in self.used_videos
                ):

                    media = video
                    media_type = "video"

                    self.used_videos.append(
                        video
                    )

                    video_count += 1

                    next_video = index + 4

            # -----------------------------------------
            # IMAGE
            # -----------------------------------------

            if media is None:

                for _ in range(5):

                    result = self.matcher.find_best(
                        text
                    )

                    if result is None:
                        break

                    image, score = result

                    if image in self.used_images:
                        continue

                    media = image
                    media_type = "image"

                    self.used_images.append(
                        image
                    )

                    image_count += 1

                    break

            # -----------------------------------------
            # FALLBACK
            # -----------------------------------------

            # -----------------------------------------
            # FALLBACK
            # -----------------------------------------

            if media is None:

                result = self.matcher.find_best(text)

                if result:

                    media, _ = result
                    media_type = "image"

                elif timeline:

                    media = timeline[-1]["media"]

                    if str(media).lower().endswith(".mp4"):

                        media_type = "video"

                    else:

                        media_type = "image"

                else:

                    continue

            last_media = media
            last_type = media_type

            timeline.append({

                "start": start,
                "end": end,
                "duration": duration,
                "text": text,
                "media": media,
                "media_type": media_type,

            })
        # -----------------------------------------------------

        log(f"Segments : {len(segments)}")
        log(f"Windows  : {total_windows}")
        log(f"Timeline : {len(timeline)}")
        log(f"Images   : {image_count}")
        log(f"Videos   : {video_count}")

        if timeline:

            total = sum(
                clip["duration"]
                for clip in timeline
            )

            log(
                f"Timeline Duration : "
                f"{total:.3f} sec"
            )

            log(
                f"Last End : "
                f"{timeline[-1]['end']:.3f} sec"
            )

        return timeline


# -----------------------------------------------------

if __name__ == "__main__":

    builder = TimelineBuilder()

    timeline = builder.build()

    print("-" * 70)

    total = 0.0

    for i, clip in enumerate(
        timeline,
        start=1
    ):

        total += clip["duration"]

        print(

            f"{i:03d} | "

            f"{clip['media_type']:5s} | "

            f"{clip['start']:7.2f} -> "

            f"{clip['end']:7.2f} | "

            f"{clip['duration']:5.2f}s"

        )

    print("-" * 70)

    print(
        f"Timeline Duration : "
        f"{total:.2f} sec"
    )

    if timeline:

        print(
            f"Last End : "
            f"{timeline[-1]['end']:.2f} sec"
        )

    print("-" * 70)