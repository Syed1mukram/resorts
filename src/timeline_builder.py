from collections import deque

from config import AUDIO_FILE, IMAGES_DIR
from src.utils import log
from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher
from src.pexels_api import PexelsAPI

VIDEO_RATIO = 0.30

VIDEO_KEYWORDS = {
    "beach","ocean","sea","waves","coast","coastline","shore","drone","aerial",
    "view","views","landscape","sunset","sunrise","pool","swimming","walk",
    "walking","drive","street","city","mountain","river","waterfall","garden",
    "arrival","outside","exterior","skyline","harbor","marina","nature"
}

IMAGE_KEYWORDS = {
    "room","suite","bedroom","bathroom","balcony","lobby","restaurant","bar",
    "spa","gym","reception","breakfast","interior","bed","villa","apartment",
    "buffet","desk"
}


class TimelineBuilder:

    def __init__(self):
        from src.scene_analyzer import SceneAnalyzer

        self.scene = SceneAnalyzer()
        self.transcript = TranscriptGenerator()
        self.matcher = ImageMatcher()
        self.pexels = PexelsAPI()

        self.used_images = deque(maxlen=8)
        self.used_videos = deque(maxlen=8)

    def wants_video(self, text):
        text = text.lower()
        return any(k in text for k in VIDEO_KEYWORDS)

    def build(self):

        log("Generating transcript...")
        segments = self.transcript.transcribe(AUDIO_FILE)

        log("Indexing images...")
        self.matcher.index_images(IMAGES_DIR)

        timeline = []

        image_count = 0
        video_count = 0

        max_videos = max(1, int(len(segments) * VIDEO_RATIO))

        transcript_end = float(segments[-1]["end"])

        for i, seg in enumerate(segments):

            if i == 0:
                start = 0.0
            else:
                start = float(seg["start"])

            # Continuous timeline
            if i == len(segments) - 1:
                end = transcript_end
            else:
                end = float(segments[i + 1]["start"])

            duration = max(0.05, end - start)

            text = seg["text"].strip()

            media = None
            media_type = "image"

            if self.wants_video(text) and video_count < max_videos:

                video = self.pexels.download(text)

                if video:
                    media = video
                    media_type = "video"
                    video_count += 1

            if media is None:

                scene = self.scene.analyze(text)

                result = self.matcher.find_best(
                     prompt=scene["prompt"],
                     scene=scene["scene"]
                )

                if result:
                    media = result[0]
                    media_type = "image"
                    image_count += 1

            if media is None and timeline:

                media = timeline[-1]["media"]
                media_type = timeline[-1]["media_type"]

            if media is None:
                continue

            timeline.append({
                "start": start,
                "end": end,
                "duration": duration,
                "text": text,
                "media": media,
                "media_type": media_type
            })

        log(f"Segments : {len(segments)}")
        log(f"Timeline : {len(timeline)}")
        log(f"Images   : {image_count}")
        log(f"Videos   : {video_count}")

        print("\n========== TIMELINE DEBUG ==========")

        total = 0.0

        for i, item in enumerate(timeline):
            total += item["duration"]
            print(
                f"{i:02d} | "
                f"{item['start']:.3f} -> {item['end']:.3f} | "
                f"{item['duration']:.3f}"
            )

        print("------------------------------------")
        print(f"Timeline Total : {total:.3f}")
        print(f"Transcript End : {transcript_end:.3f}")
        print(f"Last End       : {timeline[-1]['end']:.3f}")
        print("====================================")

        return timeline