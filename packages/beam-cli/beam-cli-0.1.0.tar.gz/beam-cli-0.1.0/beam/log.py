import sys
import os
import datetime

from rich import print


OUTPUT_PREFIX = ""


def _timestamp(str):
    t = datetime.datetime.now()
    return f"{t.hour:02d}:{t.minute:02d}:{t.second:02d}  {str}"


def warn(str):
    print(f"{OUTPUT_PREFIX}{_timestamp(str)}")  # noqa


def debug(str):
    if int(os.getenv("BEAM_DEBUG", 0)) != 0:
        print(f"{OUTPUT_PREFIX}{_timestamp(str)}")  # noqa


def die(str):
    print(f"{OUTPUT_PREFIX}{_timestamp(str)}")  # noqa
    sys.exit(1)


def info(str):
    print(f"{OUTPUT_PREFIX}{_timestamp(str)}")  # noqa
