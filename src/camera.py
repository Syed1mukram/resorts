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

        print(img_w, img_h)
        print(out_width, out_height)

        if motion == "zoom_in":
            zoom = 1.00 + 0.08 * progress

        elif motion == "zoom_out":
            zoom = 1.08 - 0.08 * progress

        else:
            zoom = 1.015

        crop_w = out_width / zoom
        crop_h = out_height / zoom

        max_x = max(0.0, img_w - crop_w)
        max_y = max(0.0, img_h - crop_h)

        x = max_x * 0.5
        y = max_y * 0.5

        pan = 0.30

        if motion == "left":
            x = max_x * (0.5 - pan * progress)

        elif motion == "right":
            x = max_x * (0.5 + pan * progress)

        elif motion == "up":
            y = max_y * (0.5 - pan * progress)

        elif motion == "down":
            y = max_y * (0.5 + pan * progress)

        x = np.clip(x, 0, max_x)
        y = np.clip(y, 0, max_y)

        x1 = int(round(x))
        y1 = int(round(y))
        x2 = int(round(x + crop_w))
        y2 = int(round(y + crop_h))

        crop = image[y1:y2, x1:x2]

        frame = cv2.resize(
            crop,
            (out_width, out_height),
            interpolation=cv2.INTER_CUBIC
        )

        return frame