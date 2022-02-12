import threading
import xonsh.tools as xt
from rich import traceback, console

traceback.install(show_locals=True)


def print_err_msg(msg=None):
    import sys

    if msg:
        msg = msg if msg.endswith("\n") else msg + "\n"
        sys.stderr.write(msg)


def except_hook(type_, value, tb):
    import sys

    traceback_console = console.Console(file=sys.stderr)

    traceback_console.print(
        traceback.Traceback.from_exception(
            type_,
            value,
            tb,
            show_locals=True,
        )
    )


def thread_excepthook(args):
    """https://docs.python.org/3/library/threading.html#threading.excepthook"""

    except_hook(args.exc_type, args.exc_value, args.exc_traceback)


def print_exc(msg=None, **_):
    import sys

    except_hook(*sys.exc_info())
    print_err_msg(msg)


threading.excepthook = thread_excepthook
xt.print_exception = print_exc
