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

            zoom = 0.9 + (
                self.zoom_strength * progress
            )

        elif motion == "zoom_out":

            zoom = (
                0.9 + self.zoom_strength
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

        tx = max_x / 1.3
        ty = max_y / 1.5

        if motion == "left":

            tx = max_x * (1.0 - progress)

        elif motion == "right":

            tx = max_x * progress

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

        # Center of image
        cx = img_w * 0.5
        cy = img_h * 0.5

        # Translation to move virtual camera
        dx = -(tx)
        dy = -(ty)

        # Affine matrix
        M = np.array(

            [

                [zoom, 0.0, (1.0 - zoom) * cx + dx],

                [0.0, zoom, (1.0 - zoom) * cy + dy],

            ],

            dtype=np.float32,

        )

        frame = cv2.warpAffine(

            image,

            M,

            (img_w, img_h),

            flags=cv2.INTER_LINEAR,

            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255,255,255),
        )

        x = (img_w - out_width) // 2
        y = (img_h - out_height) // 2

        frame = frame[
            y:y + out_height,
            x:x + out_width
        ]

        return frame