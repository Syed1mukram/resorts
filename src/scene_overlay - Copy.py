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

    # Smooth entrance + subtle hotel-name flash.
    number_alpha = (
        "if(lt(t\\,0.30)\\,"
        "t/0.30\\,"
        "1)"
    )

    name_alpha = (
        "if(lt(t\\,0.25)\\,"
        "t/0.25\\,"
        "1)"
    )

    return (
        # NUMBER — background is attached directly to the text.
        f"drawtext="
        f"fontfile='{font}':"
        f"text='{number}':"
        f"x=88:"
        f"y=h-260:"
        f"fontsize=44:"
        f"fontcolor=FFFFFF:"
        f"bordercolor=000000@0.35:"
        f"borderw=1:"
        f"box=1:"
        f"boxcolor=07131C@0.82:"
        f"boxborderw=5:"
        f"alpha='{number_alpha}':"
        f"enable='between(t,0,5)',"

        # HOTEL NAME — blue, premium font, attached background.
        f"drawtext="
        f"fontfile='{font_bold}':"
        f"text='{name}':"
        f"x=88:"
        f"y=h-216:"
        f"fontsize=68:"
        f"fontcolor=ebd90c:"
        f"bordercolor=000000@0.20:"
        f"borderw=2:"
                f"box=1:"
        f"boxcolor=07131C@0.82:"
        f"boxborderw=4:"
        f"alpha='{name_alpha}':"
        f"enable='between(t,0,5)',"

        # Underline directly under the hotel name.
        "drawbox="
        "x=88:"
        "y=h-154:"
        "w=620:"
        "h=4:"
        "color=19B5FE:"
        "t=fill:"
        "enable='between(t,0,5)'"
    )


def get_overlay(style, hotel_number, hotel_name):
    return style_7(hotel_number, hotel_name)