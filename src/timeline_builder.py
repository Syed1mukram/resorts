from collections import deque

from config import (
    AUDIO_FILE,
    IMAGES_DIR,
)

from src.utils import log
from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher
from src.pexels_api import PexelsAPI


VIDEO_RATIO = 0.35
VIDEO_COOLDOWN = 4
MIN_SEGMENT = 1.5


class TimelineBuilder:

    def __init__(self):

        self.transcript = TranscriptGenerator()
        self.matcher = ImageMatcher()
        self.pexels = PexelsAPI()

        self.used_images = deque(maxlen=5)
        self.used_videos = deque(maxlen=VIDEO_COOLDOWN)
    # -----------------------------------------------------

    def build(self):

        log("Generating transcript...")

        segments = self.transcript.transcribe(AUDIO_FILE)

        segments = [
            s for s in segments
            if (float(s["end"]) - float(s["start"])) >= MIN_SEGMENT
        ]

        log("Indexing images...")

        self.matcher.index_images(IMAGES_DIR)

        timeline = []

        image_count = 0
        video_count = 0

        next_video = 3

        for index, seg in enumerate(segments):

            start = float(seg["start"])
            end = float(seg["end"])
            duration = end - start

            text = seg["text"].strip()

            media = None
            media_type = "image"

            use_video = (
                index >= next_video
                and
                video_count < int(len(segments) * VIDEO_RATIO)
            )

            # ---------------- VIDEO ----------------

            if use_video:

                video = self.pexels.download(text)

                if video and video not in self.used_videos:

                    media = video
                    media_type = "video"

                    self.used_videos.append(video)

                    video_count += 1
                    next_video = index + VIDEO_COOLDOWN

            # ---------------- IMAGE ----------------

            if media is None:

                for _ in range(5):

                    result = self.matcher.find_best(text)

                    if result is None:
                        break

                    image, score = result

                    if image in self.used_images:
                        continue

                    media = image
                    media_type = "image"

                    self.used_images.append(image)

                    image_count += 1
                    break

            # ---------------- FALLBACK ----------------

            if media is None:

                if timeline:

                    media = timeline[-1]["media"]
                    media_type = timeline[-1]["media_type"]

                else:

                    result = self.matcher.find_best(text)

                    if result:

                        media, _ = result
                        media_type = "image"
                    else:
                        continue

            timeline.append({

                "start": start,
                "end": end,
                "duration": duration,
                "text": text,
                "media": media,
                "media_type": media_type,

            })

        log(f"Segments : {len(segments)}")
        log(f"Timeline : {len(timeline)}")
        log(f"Images   : {image_count}")
        log(f"Videos   : {video_count}")

        return timeline