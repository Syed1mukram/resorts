FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def _escape(text):
    text = str(text)
    text = text.replace("\\", r"\\")
    text = text.replace("'", r"\'")
    text = text.replace(":", r"\:")
    text = text.replace(",", r"\,")
    return text


def style_7(hotel_number, hotel_name):
    number = _escape(f"NO. {hotel_number}")
    name = _escape(hotel_name)

    font = FONT.replace("\\", "/").replace(":", r"\:")
    font_bold = FONT_BOLD.replace("\\", "/").replace(":", r"\:")

    # Smooth entrance, stays visible for 5 seconds, then disappears.
    alpha_expr = (
        "if(lt(t\\,0.25)\\,"
        "t/0.25\\,"
        "if(lt(t\\,5)\\,"
        "1\\,"
        "1-(t-5)/0.25))"
    )

    return (
        # ONE BLUE LINE — outside the boxes, aligned left with both texts.
        "drawbox="
        "x=60:"
        "y=h-280:"
        "w=6:"
        "h=140:"
        "color=19B5FE:"
        "t=fill:"
        "enable='between(t,0,5.25)',"

        # NO. 1 — on top.
        f"drawtext="
        f"fontfile='{font}':"
        f"text='{number}':"
        f"x=88:"
        f"y=h-270:"
        f"fontsize=60:"
        f"fontcolor=FFFFFF:"
        f"bordercolor=000000@0.45:"
        f"borderw=2:"
        f"box=1:"
        f"boxcolor=07131C@0.82:"
        f"boxborderw=8:"
        f"alpha='{alpha_expr}':"
        f"enable='between(t,0,5.25)',"

        # HOTEL NAME — below NO. 1 with a clear gap.
        f"drawtext="
        f"fontfile='{font_bold}':"
        f"text='{name}':"
        f"x=92:"
        f"y=h-200:"
        f"fontsize=75:"
        f"fontcolor=ebd90c:"
        f"bordercolor=000000@0.50:"
        f"borderw=2:"
        f"box=1:"
        f"boxcolor=07131C@0.82:"
        f"boxborderw=10:"
        f"alpha='{alpha_expr}':"
        f"enable='between(t,0,5.25)'"
    )


def get_overlay(style, hotel_number, hotel_name):
    return style_7(hotel_number, hotel_name)