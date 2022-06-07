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


def _load():
    # put this in a function so that namespace is not polluted
    from pathlib import Path
    from xonsh.xontribs import xontribs_load

    xontribs_load(
        [
            # venv
            "vox",
            # "avox_poetry",
            # --- completions --- #
            "argcomplete",
            "jedi",
            # --- prompt --- #
            "cmd_done",
            # cli integration
            "broot",
            "fzf_widgets",
            # theme
            "powerline3",
            # keybindings
            "hist_navigator",
            # misc
            # "back2dir",
            "commands",
            "term_integration",
            "fish_completer",
            "django",
        ]
    )
    from user_xsh.config_loader import Loader

    if "pytest" in str(sys.argv):
        raise Exception(" do not call rc")

    XSH_ROOT_PATH = Path(__file__).parent

    Loader(XSH_ROOT_PATH / "configs").normal()


_load()
del _load

# usable objects to the console
from pipe import *  # noqa - import pipe enabled functions
from lambdax import X  # noqa
