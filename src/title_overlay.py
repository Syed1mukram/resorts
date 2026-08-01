from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class TitleOverlay:

    def __init__(self):

        self.width = 1920
        self.height = 1080

        # Windows / Kaggle common fonts
        self.font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]

        self.regular_font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]

    # ---------------------------------------------------------

    def _font(self, size, bold=True):

        paths = (
            self.font_paths
            if bold
            else self.regular_font_paths
        )

        for path in paths:

            if Path(path).exists():

                return ImageFont.truetype(
                    path,
                    size=size
                )

        return ImageFont.load_default()

    # ---------------------------------------------------------

    def _center_text(
        self,
        draw,
        text,
        y,
        font,
        fill,
    ):

        box = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        text_width = box[2] - box[0]

        x = (
            self.width - text_width
        ) // 2

        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill
        )

    # ---------------------------------------------------------

    def create(
        self,
        hotel_number,
        hotel_name,
        output_file,
    ):

        hotel_number = int(hotel_number)

        overlay = Image.new(
            "RGBA",
            (self.width, self.height),
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(
            overlay,
            "RGBA"
        )

        number_font = self._font(90)
        title_font = self._font(76)
        small_font = self._font(34, bold=False)

        # Split optional subtitle
        parts = hotel_name.split(" - ", 1)

        title = parts[0].strip()

        subtitle = (
            parts[1].strip()
            if len(parts) > 1
            else ""
        )

        # =====================================================
        # #9 - BLACK / GOLD CLASSIC
        # =====================================================

        if hotel_number == 9:

            draw.rounded_rectangle(
                (360, 310, 1560, 780),
                radius=40,
                fill=(0, 0, 0, 175),
                outline=(218, 165, 32, 230),
                width=5
            )

            number_color = (235, 185, 65, 255)
            title_color = (255, 255, 255, 255)
            subtitle_color = (235, 185, 65, 255)

        # =====================================================
        # #8 - WHITE / NAVY
        # =====================================================

        elif hotel_number == 8:

            draw.rounded_rectangle(
                (300, 350, 1620, 750),
                radius=30,
                fill=(255, 255, 255, 225)
            )

            number_color = (15, 48, 90, 255)
            title_color = (15, 48, 90, 255)
            subtitle_color = (40, 40, 40, 255)

        # =====================================================
        # #7 - DARK LUXURY
        # =====================================================

        elif hotel_number == 7:

            draw.polygon(
                [
                    (430, 300),
                    (1490, 300),
                    (1640, 540),
                    (1490, 780),
                    (430, 780),
                    (280, 540),
                ],
                fill=(5, 12, 25, 205),
                outline=(220, 170, 50, 255)
            )

            number_color = (225, 175, 55, 255)
            title_color = (255, 255, 255, 255)
            subtitle_color = (225, 175, 55, 255)

        # =====================================================
        # #6 - CLEAN WHITE / GOLD
        # =====================================================

        elif hotel_number == 6:

            draw.rounded_rectangle(
                (250, 365, 1670, 730),
                radius=20,
                fill=(255, 255, 255, 230),
                outline=(190, 145, 55, 255),
                width=5
            )

            number_color = (175, 125, 35, 255)
            title_color = (30, 30, 35, 255)
            subtitle_color = (150, 105, 30, 255)

        # =====================================================
        # #5 - MODERN BLACK
        # =====================================================

        elif hotel_number == 5:

            draw.rounded_rectangle(
                (320, 320, 1600, 770),
                radius=20,
                fill=(0, 0, 0, 205),
                outline=(45, 210, 175, 255),
                width=5
            )

            number_color = (55, 225, 185, 255)
            title_color = (255, 255, 255, 255)
            subtitle_color = (55, 225, 185, 255)

        # =====================================================
        # #4 - SOFT WHITE
        # =====================================================

        elif hotel_number == 4:

            draw.rounded_rectangle(
                (260, 350, 1660, 750),
                radius=70,
                fill=(255, 255, 255, 225)
            )

            number_color = (105, 55, 145, 255)
            title_color = (75, 35, 100, 255)
            subtitle_color = (90, 70, 100, 255)

        # =====================================================
        # #3 - PREMIUM CREAM
        # =====================================================

        elif hotel_number == 3:

            draw.rounded_rectangle(
                (350, 285, 1570, 795),
                radius=80,
                fill=(250, 245, 225, 235),
                outline=(190, 145, 55, 255),
                width=5
            )

            number_color = (180, 125, 35, 255)
            title_color = (25, 65, 55, 255)
            subtitle_color = (145, 100, 30, 255)

        # =====================================================
        # #2 - BLACK / GOLD PREMIUM
        # =====================================================

        elif hotel_number == 2:

            draw.rounded_rectangle(
                (280, 330, 1640, 760),
                radius=25,
                fill=(5, 5, 5, 215),
                outline=(225, 170, 55, 255),
                width=6
            )

            number_color = (235, 185, 65, 255)
            title_color = (255, 255, 255, 255)
            subtitle_color = (235, 185, 65, 255)

        # =====================================================
        # #1 - WINNER / MOST PREMIUM
        # =====================================================

        else:

            draw.rounded_rectangle(
                (300, 285, 1620, 800),
                radius=35,
                fill=(255, 255, 255, 220),
                outline=(215, 160, 45, 255),
                width=7
            )

            draw.rectangle(
                (300, 285, 1620, 300),
                fill=(215, 160, 45, 255)
            )

            number_color = (190, 130, 25, 255)
            title_color = (20, 35, 55, 255)
            subtitle_color = (155, 105, 25, 255)

        # =====================================================
        # TEXT
        # =====================================================

        self._center_text(
            draw,
            f"#{hotel_number}",
            365,
            number_font,
            number_color
        )

        self._center_text(
            draw,
            title.upper(),
            500,
            title_font,
            title_color
        )

        if subtitle:

            self._center_text(
                draw,
                subtitle.upper(),
                625,
                small_font,
                subtitle_color
            )

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        overlay.save(
            output_file,
            "PNG"
        )

        return output_file