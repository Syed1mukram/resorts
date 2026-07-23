import random

import cv2
import numpy as np


class Camera:

    def __init__(self):

        self.zoom_strength = 0.03
        self.pan_strength = 0.02

    # -----------------------------------------------------

    def ease(self, t):

        return t * t * (2.0 - 1.0 * t)

    # -----------------------------------------------------

    def random_motion(self):

        return random.choice([

            "zoom_in",

            "zoom_out",

            "left",

            "right",

            "up",

            "down",

        ])

    # -----------------------------------------------------

    def get_transform(

        self,

        progress,

        motion,

        img_width,

        img_height,

        out_width,

        out_height,

    ):

        progress = self.ease(progress)

        zoom = 1.0

        if motion == "zoom_in":
            zoom = 1.0 + self.zoom_strength * progress

        elif motion == "zoom_out":
            zoom = (1.0 + self.zoom_strength) - (
                self.zoom_strength * progress
            )

        max_x = max(
            0.0,
            img_width - out_width
        )

        max_y = max(
            0.0,
            img_height - out_height
        )

        tx = max_x / 1.3
        ty = max_y / 1.5

        if motion == "left":

            tx = max_x * (1.0 - progress)

        elif motion == "right":

            tx = max_x * progress * 0.35

        elif motion == "up":

            tx = max_x * (1.0 - progress * 0.35)

        elif motion == "down":

            ty = max_y * (1.0 - progress * 0.35)

        return (

            float(tx),

            float(ty),

            float(zoom)

        )
    # -----------------------------------------------------

    def render(
        self,
        image,
        progress,
        motion,
        out_width,
        out_height,
    ):

        progress = self.ease(progress)

        img_h, img_w = image.shape[:2]

        if motion == "zoom_in":
            zoom = 1.00 + 0.04 * progress
        elif motion == "zoom_out":
            zoom = 1.04 - 0.04 * progress
        else:
            zoom = 1.02

        crop_w = int(out_width / zoom)
        crop_h = int(out_height / zoom)

        crop_w = min(crop_w, img_w)
        crop_h = min(crop_h, img_h)

        max_x = img_w - crop_w
        max_y = img_h - crop_h

        if motion == "left":
            x = int(max_x * (1.0 - progress * 0.30))
            y = max_y // 2

        elif motion == "right":
            x = int(max_x * progress * 0.30)
            y = max_y // 2

        elif motion == "up":
            x = max_x // 2
            y = int(max_y * (1.0 - progress * 0.30))

        elif motion == "down":
            x = max_x // 2
            y = int(max_y * progress * 0.30)

        else:
            x = max_x // 2
            y = max_y // 2

        crop = image[
            y:y + crop_h,
            x:x + crop_w
        ]

        frame = cv2.resize(
            crop,
            (out_width, out_height),
            interpolation=cv2.INTER_LANCZOS4
        )

        return frame