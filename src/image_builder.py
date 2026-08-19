from PIL import Image
from src.camera import Camera
from pathlib import Path
import random
import subprocess

import cv2
import numpy as np

from config import (
    VIDEO_WIDTH,
    VIDEO_HEIGHT,
    FPS,
    CRF,
    PRESET,
)


class ImageBuilder:

    def __init__(self):

        self.camera = Camera()

        # Motion strength
        self.zoom_amount = 0.08      # 8%
        self.pan_amount = 0.06       # 6%

    # ---------------------------------------------------------

    def _cover_resize(self, image):

        h, w = image.shape[:2]

        scale = max(
            VIDEO_WIDTH / w,
            VIDEO_HEIGHT / h
        )

        nw = int(np.ceil(w * scale * 1.12))
        nh = int(np.ceil(h * scale * 1.12))

        image = cv2.resize(
            image,
            (nw, nh),
            interpolation=cv2.INTER_LANCZOS4
        )

        return image

    # ---------------------------------------------------------

    def _ease(self, t):

        # Smoothstep easing
        return t * t * (3.0 - 2.0 * t)

    # ---------------------------------------------------------

    def _motion(self):

        return random.choice([
            "zoom_in",
            "zoom_out",
            "left",
            "right",
        ])

    # ---------------------------------------------------------

    def _camera(
        self,
        img_w,
        img_h,
        t,
        motion
    ):

        x_max = img_w - VIDEO_WIDTH
        y_max = img_h - VIDEO_HEIGHT

        x = x_max / 2.0
        y = y_max / 2.0

        if motion == "left":

            x = x_max * (1.0 - t)

        elif motion == "right":

            x = x_max * t

        elif motion == "up":

            y = y_max * (1.0 - t)

        elif motion == "down":

            y = y_max * t

        return (
            float(x),
            float(y)
        )
    # ---------------------------------------------------------

    def build(
        self,
        image_path,
        output_path,
        duration
    ):


        try:

            pil = Image.open(image_path).convert("RGB")

            image = cv2.cvtColor(
                np.array(pil),
                cv2.COLOR_RGB2BGR
            )

        except Exception as e:

           raise RuntimeError(
               f"Cannot read image : {image_path}\n{e}"
           )

        image = self._cover_resize(image)

        # GPU rendering: avoid CPU OpenCV frame-by-frame encoding.
        # FFmpeg generates the motion and encodes directly with NVENC.
        motion = self._motion()
        duration = max(float(duration), 0.05)

        source_image = Path(output_path).with_suffix(".source.jpg")
        Image.fromarray(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ).save(source_image, quality=95)

        frames = max(int(duration * FPS), 1)

        if motion == "zoom_in":
            zoom = "min(zoom+0.0007,1.08)"
            x = "iw/2-(iw/zoom/2)"
            y = "ih/2-(ih/zoom/2)"
        elif motion == "zoom_out":
            zoom = "if(eq(on,1),1.08,max(1.0,zoom-0.0007))"
            x = "iw/2-(iw/zoom/2)"
            y = "ih/2-(ih/zoom/2)"
        elif motion == "left":
            zoom = "1.04"
            x = f"(iw-iw/zoom)*(1-on/{max(frames-1,1)})"
            y = "(ih-ih/zoom)/2"
        elif motion == "right":
            zoom = "1.04"
            x = f"(iw-iw/zoom)*(on/{max(frames-1,1)})"
            y = "(ih-ih/zoom)/2"
        else:
            zoom = "1.04"
            x = "(iw-iw/zoom)/2"
            y = "(ih-ih/zoom)/2"

        vf = (
            f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:"
            f"force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"zoompan=z='{zoom}':x='{x}':y='{y}':"
            f"d=1:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={FPS}"
        )

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(source_image),
            "-t", f"{duration:.3f}",
            "-vf", vf,
            "-an",
            "-c:v", "h264_nvenc",
            "-preset", "p4",
            "-cq", "18",
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            "-movflags", "+faststart",
            str(output_path),
        ]

        try:
            subprocess.run(cmd, check=True)
        finally:
            source_image.unlink(missing_ok=True)