"""subprocess call utils"""

import glob
import os

import funcy
from xonsh.built_ins import XSH as xsh
from xontrib_commands.utils import run

poetry_run = lambda x: run(f"poetry run {x}")
poetry_run_py = lambda x: run(f"poetry run python {x}")


# $RAISE_SUBPROC_ERROR = True


@funcy.decorator
def run_in_path(call, path):
    if "~" in path:
        path = os.path.expanduser(path)
    full_path = glob.glob(path)[0]
    run("pushd", full_path)
    call()
    run("popd")


@funcy.decorator
def trace_(call):
    xsh.env["XONSH_TRACE_SUBPROC"] = True
    result = call()
    xsh.env["XONSH_TRACE_SUBPROC"] = False
    return result


def current_folder_name() -> str:
    return os.path.split(os.path.abspath(os.curdir))[-1]
