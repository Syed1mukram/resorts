from collections import deque

from config import AUDIO_FILE, IMAGES_DIR
from src.utils import log
from src.transcript import TranscriptGenerator
from src.image_matcher import ImageMatcher
from src.pexels_api import PexelsAPI

VIDEO_RATIO = 0.30

VIDEO_KEYWORDS={"beach","ocean","sea","waves","coast","coastline","shore","drone","aerial","view","views","landscape","sunset","sunrise","pool","swimming","walk","walking","drive","street","city","mountain","river","waterfall","garden","arrival","outside","exterior","skyline","harbor","marina","nature"}
IMAGE_KEYWORDS={"room","suite","bedroom","bathroom","balcony","lobby","restaurant","bar","spa","gym","reception","breakfast","interior","bed","villa","apartment","buffet","desk"}

class TimelineBuilder:
    def __init__(self):
        self.transcript=TranscriptGenerator()
        self.matcher=ImageMatcher()
        self.pexels=PexelsAPI()
        self.used_images=deque(maxlen=8)
        self.used_videos=deque(maxlen=8)

    def wants_video(self,text):
        text=text.lower()
        return any(k in text for k in VIDEO_KEYWORDS)

    def wants_image(self,text):
        text=text.lower()
        return any(k in text for k in IMAGE_KEYWORDS)

    def build(self):
        log("Generating transcript...")
        segments=self.transcript.transcribe(AUDIO_FILE)
        log("Indexing images...")
        self.matcher.index_images(IMAGES_DIR)
        timeline=[]
        image_count=0
        video_count=0
        max_videos=max(1,int(len(segments)*VIDEO_RATIO))
        transcript_end = float(segments[-1]["end"])

        for i, seg in enumerate(segments):
            start=float(seg["start"])
            if i < len(segments)-1:
                end=float(segments[i+1]["start"])
            else:
                end=transcript_end
            duration=end-start
            text=seg["text"].strip()
            media=None; media_type="image"
            if self.wants_video(text) and video_count<max_videos:
                v=self.pexels.download(text)
                if v and v not in self.used_videos:
                    media=v; media_type="video"; self.used_videos.append(v); video_count+=1
            if media is None:
                result=self.matcher.find_best(text)
                if result:
                    img,_=result; media=img; media_type="image"; image_count+=1
                    self.used_images.append(img)
            if media is None and timeline:
                media=timeline[-1]["media"]; media_type=timeline[-1]["media_type"]
            if media is None:
                continue
            timeline.append({"start":start,"end":end,"duration":duration,"text":text,"media":media,"media_type":media_type})
        log(f"Segments : {len(segments)}")
        log(f"Timeline : {len(timeline)}")
        log(f"Images   : {image_count}")
        log(f"Videos   : {video_count}")
        return timeline
