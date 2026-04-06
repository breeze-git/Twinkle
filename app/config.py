import sys
from pathlib import Path


def get_base_dir():

    if getattr(sys, "frozen", False):

        meipass = getattr(sys, "_MEIPASS", None)

        if meipass:
            return Path(meipass)

        exe_dir = Path(sys.executable).parent
        if (exe_dir / "assets").exists():
            return exe_dir

        internal_dir = exe_dir / "_internal"
        if (internal_dir / "assets").exists():
            return internal_dir

        return exe_dir

    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()

ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"

APP_NAME = "TIMER"
