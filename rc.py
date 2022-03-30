# import asyncio
# import uvloop
#
# # the output gets cut -- example 'ls' -- but it doesn't feel sluggish like that of with default ptk
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import io
import sys

# disable buffering outputs
sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), "wb", 0), write_through=True)
sys.stderr = io.TextIOWrapper(open(sys.stderr.fileno(), "wb", 0), write_through=True)

from pathlib import Path

from user_xsh.config_loader import Loader

if "pytest" in str(sys.argv):
    raise Exception(" do not call rc")

XSH_ROOT_PATH = Path(__file__).parent


Loader(XSH_ROOT_PATH / "configs").normal()

# usable objects to the console
from pipe import *  # noqa - import pipe enabled functions
from lambdax import X  # noqa

from user_xsh.completers import django_py_manage  # noqa
