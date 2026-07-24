import random

import cv2
import numpy as np


class Camera:

    def __init__(self):

        self.zoom_strength = 0.04
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

            zoom = 1.0 + (
                self.zoom_strength * progress
            )

        elif motion == "zoom_out":

            zoom = (
                1.0 + self.zoom_strength
            ) - (
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

        tx = max_x / 2.0
        ty = max_y / 2.0

        if motion == "left":

            tx = max_x * (1.0 - progress) * 0.85

        elif motion == "right":

            tx = max_x * progress * 0.85

        elif motion == "up":

            ty = max_y * (1.0 - progress)

        elif motion == "down":

            ty = max_y * progress

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

        img_h, img_w = image.shape[:2]

        tx, ty, zoom = self.get_transform(
            progress,
            motion,
            img_w,
            img_h,
            out_width,
            out_height,
        )

        # Camera window size
        cam_w = int(out_width / zoom)
        cam_h = int(out_height / zoom)

        cam_w = min(cam_w, img_w)
        cam_h = min(cam_h, img_h)

        max_x = max(0, img_w - cam_w)
        max_y = max(0, img_h - cam_h)

        if motion == "left":
            x = int(max_x * (1.0 - progress))
            y = max_y // 2

        elif motion == "right":
            x = int(max_x * progress)
            y = max_y // 2

        elif motion == "up":
            x = max_x // 2
            y = int(max_y * (1.0 - progress))

        elif motion == "down":
            x = max_x // 2
            y = int(max_y * progress)

        else:
            x = max_x // 2
            y = max_y // 2

        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

       crop = image[y:y + cam_h, x:x + cam_w]

        frame = cv2.resize(
            crop,
            (out_width, out_height),
            interpolation=cv2.INTER_LINEAR,
        )

        return frame