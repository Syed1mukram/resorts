from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path


class TitleOverlay:

    def __init__(self):

        self.width = 1920
        self.height = 1080

        self.bold_fonts = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]

        self.regular_fonts = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]

    # =========================================================

    def _font(self, size, bold=True):

        paths = self.bold_fonts if bold else self.regular_fonts

        for path in paths:
            if Path(path).exists():
                return ImageFont.truetype(path, size)

        return ImageFont.load_default()

    # =========================================================

    def _text_width(self, draw, text, font):

        box = draw.textbbox((0, 0), text, font=font)
        return box[2] - box[0]

    # =========================================================

    def _fit_font(
        self,
        draw,
        text,
        max_width,
        start_size=105,
        min_size=48,
        bold=True,
    ):

        size = start_size

        while size >= min_size:

            font = self._font(size, bold)

            if self._text_width(draw, text, font) <= max_width:
                return font

            size -= 3

        return self._font(min_size, bold)

    # =========================================================

    def _center(self, draw, text, y, font, fill):

        box = draw.textbbox((0, 0), text, font=font)

        width = box[2] - box[0]

        x = (self.width - width) // 2

        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill
        )

    # =========================================================

    def _shadow_panel(
        self,
        overlay,
        box,
        radius=45,
    ):

        shadow = Image.new(
            "RGBA",
            overlay.size,
            (0, 0, 0, 0)
        )

        d = ImageDraw.Draw(shadow)

        x1, y1, x2, y2 = box

        d.rounded_rectangle(
            (x1 + 18, y1 + 22, x2 + 18, y2 + 22),
            radius=radius,
            fill=(0, 0, 0, 175)
        )

        shadow = shadow.filter(
            ImageFilter.GaussianBlur(22)
        )

        overlay.alpha_composite(shadow)

    # =========================================================

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

        # -----------------------------------------------------
        # HOTEL NAME
        # -----------------------------------------------------

        parts = hotel_name.split(" - ", 1)

        title = parts[0].strip().upper()

        subtitle = (
            parts[1].strip().upper()
            if len(parts) > 1
            else ""
        )

        # -----------------------------------------------------
        # DESIGN SETTINGS
        # -----------------------------------------------------

        designs = {

            9: {
                "box": (330, 280, 1590, 800),
                "bg": (5, 5, 7, 225),
                "border": (235, 178, 55, 255),
                "accent": (245, 190, 70, 255),
                "title": (255, 255, 255, 255),
                "sub": (240, 190, 75, 255),
            },

            8: {
                "box": (300, 300, 1620, 790),
                "bg": (240, 247, 252, 235),
                "border": (30, 80, 135, 255),
                "accent": (20, 65, 120, 255),
                "title": (15, 48, 90, 255),
                "sub": (45, 70, 100, 255),
            },

            7: {
                "box": (320, 285, 1600, 800),
                "bg": (30, 10, 45, 225),
                "border": (225, 170, 60, 255),
                "accent": (235, 185, 65, 255),
                "title": (255, 255, 255, 255),
                "sub": (235, 185, 75, 255),
            },

            6: {
                "box": (300, 300, 1620, 790),
                "bg": (246, 241, 220, 238),
                "border": (65, 105, 75, 255),
                "accent": (55, 95, 65, 255),
                "title": (35, 70, 50, 255),
                "sub": (145, 105, 45, 255),
            },

            5: {
                "box": (320, 290, 1600, 800),
                "bg": (10, 12, 15, 230),
                "border": (235, 105, 20, 255),
                "accent": (245, 110, 20, 255),
                "title": (255, 255, 255, 255),
                "sub": (245, 125, 35, 255),
            },

            4: {
                "box": (300, 300, 1620, 790),
                "bg": (225, 247, 248, 235),
                "border": (35, 145, 155, 255),
                "accent": (25, 130, 145, 255),
                "title": (20, 90, 105, 255),
                "sub": (35, 105, 115, 255),
            },

            3: {
                "box": (315, 275, 1605, 810),
                "bg": (8, 28, 48, 232),
                "border": (215, 165, 65, 255),
                "accent": (235, 185, 75, 255),
                "title": (250, 235, 190, 255),
                "sub": (225, 180, 80, 255),
            },

            2: {
                "box": (300, 285, 1620, 805),
                "bg": (247, 242, 225, 240),
                "border": (190, 145, 55, 255),
                "accent": (180, 130, 40, 255),
                "title": (35, 35, 35, 255),
                "sub": (120, 90, 45, 255),
            },

            1: {
                "box": (285, 265, 1635, 820),
                "bg": (4, 5, 7, 238),
                "border": (245, 190, 60, 255),
                "accent": (255, 200, 70, 255),
                "title": (255, 244, 205, 255),
                "sub": (245, 195, 80, 255),
            },
        }

        style = designs.get(
            hotel_number,
            designs[9]
        )

        box = style["box"]

        # -----------------------------------------------------
        # SHADOW
        # -----------------------------------------------------

        self._shadow_panel(
            overlay,
            box,
            radius=48
        )

        draw = ImageDraw.Draw(
            overlay,
            "RGBA"
        )

        x1, y1, x2, y2 = box

        # -----------------------------------------------------
        # MAIN PANEL
        # -----------------------------------------------------

        draw.rounded_rectangle(
            box,
            radius=48,
            fill=style["bg"],
            outline=style["border"],
            width=6
        )

        # Inner border
        draw.rounded_rectangle(
            (
                x1 + 14,
                y1 + 14,
                x2 - 14,
                y2 - 14
            ),
            radius=38,
            outline=(
                style["border"][0],
                style["border"][1],
                style["border"][2],
                120
            ),
            width=2
        )

        # -----------------------------------------------------
        # TOP ACCENT
        # -----------------------------------------------------

        draw.rounded_rectangle(
            (
                x1 + 160,
                y1 - 5,
                x2 - 160,
                y1 + 9
            ),
            radius=8,
            fill=style["accent"]
        )

        # -----------------------------------------------------
        # RANK BADGE
        # -----------------------------------------------------

        badge_x = self.width // 2
        badge_y = y1 + 40
        badge_r = 92

        # Badge shadow
        draw.ellipse(
            (
                badge_x - badge_r - 8,
                badge_y - badge_r + 8,
                badge_x + badge_r + 8,
                badge_y + badge_r + 24
            ),
            fill=(0, 0, 0, 100)
        )

        draw.ellipse(
            (
                badge_x - badge_r,
                badge_y - badge_r,
                badge_x + badge_r,
                badge_y + badge_r
            ),
            fill=(8, 8, 10, 255),
            outline=style["accent"],
            width=7
        )

        draw.ellipse(
            (
                badge_x - badge_r + 12,
                badge_y - badge_r + 12,
                badge_x + badge_r - 12,
                badge_y + badge_r - 12
            ),
            outline=(
                style["accent"][0],
                style["accent"][1],
                style["accent"][2],
                150
            ),
            width=2
        )

        number_font = self._font(
            92 if hotel_number != 1 else 100
        )

        rank = f"#{hotel_number}"

        rank_box = draw.textbbox(
            (0, 0),
            rank,
            font=number_font
        )

        rank_w = rank_box[2] - rank_box[0]
        rank_h = rank_box[3] - rank_box[1]

        draw.text(
            (
                badge_x - rank_w // 2,
                badge_y - rank_h // 2 - 10
            ),
            rank,
            font=number_font,
            fill=style["accent"]
        )

        # -----------------------------------------------------
        # TITLE AUTO FIT
        # -----------------------------------------------------

        title_font = self._fit_font(
            draw,
            title,
            max_width=(x2 - x1) - 150,
            start_size=112,
            min_size=52,
            bold=True
        )

        title_box = draw.textbbox(
            (0, 0),
            title,
            font=title_font
        )

        title_h = (
            title_box[3] -
            title_box[1]
        )

        title_y = y1 + 235

        self._center(
            draw,
            title,
            title_y,
            title_font,
            style["title"]
        )

        # -----------------------------------------------------
        # DECORATIVE LINE
        # -----------------------------------------------------

        line_y = title_y + title_h + 45

        draw.line(
            (
                x1 + 180,
                line_y,
                self.width // 2 - 80,
                line_y
            ),
            fill=style["accent"],
            width=3
        )

        draw.line(
            (
                self.width // 2 + 80,
                line_y,
                x2 - 180,
                line_y
            ),
            fill=style["accent"],
            width=3
        )

        # Center diamond
        cx = self.width // 2

        draw.polygon(
            [
                (cx, line_y - 10),
                (cx + 10, line_y),
                (cx, line_y + 10),
                (cx - 10, line_y),
            ],
            fill=style["accent"]
        )

        # -----------------------------------------------------
        # SUBTITLE AUTO FIT
        # -----------------------------------------------------

        if subtitle:

            sub_font = self._fit_font(
                draw,
                subtitle,
                max_width=(x2 - x1) - 220,
                start_size=48,
                min_size=30,
                bold=True
            )

            self._center(
                draw,
                subtitle,
                line_y + 45,
                sub_font,
                style["sub"]
            )

        # -----------------------------------------------------
        # #1 EXTRA WINNER DETAIL
        # -----------------------------------------------------

        if hotel_number == 1:

            winner_font = self._font(
                28,
                bold=True
            )

            self._center(
                draw,
                "★  TOP PICK  ★",
                y2 - 70,
                winner_font,
                style["accent"]
            )

        # -----------------------------------------------------
        # OUTPUT
        # -----------------------------------------------------

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