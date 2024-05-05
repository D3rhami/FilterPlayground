import os
import platform


def get_user_picture_folder():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Pictures")
    elif system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Pictures")
    elif system == "Linux":
        return os.path.join(os.path.expanduser("~"), "Pictures")
    else:
        return r"c"


FONT_SIZE = 18
FONTS = {
        "GeorgiaSans": "fonts/GeorgiaSans.ttf",
        "Montserrat": "fonts/Montserrat.ttf",
        "Arial": "fonts/Arial.ttf",
}
PIC_DIR = get_user_picture_folder()
BTN_FS = 15  # button font size
PADDING_APP = (100, 40)
