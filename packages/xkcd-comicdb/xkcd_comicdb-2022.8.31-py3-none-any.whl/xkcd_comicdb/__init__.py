import os
XKCD_DATABASE_PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0], "xkcd.sqlite3")
__all__ = ["XKCD_DATABASE_PATH"]