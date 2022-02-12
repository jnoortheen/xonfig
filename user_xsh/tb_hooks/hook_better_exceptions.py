"""integration better-exceptions with Xonsh"""

import threading

import better_exceptions
import xonsh.tools as xt

better_exceptions.hook()


def thread_excepthook(args):
    """https://docs.python.org/3/library/threading.html#threading.excepthook"""
    print(args, [type(t) for t in dir(args)])
    better_exceptions.excepthook(args.exc_type, args.exc_value, args.exc_traceback)


def print_exc(msg=None, **_):
    import sys

    better_exceptions.excepthook(*sys.exc_info())
    if msg:
        msg = msg if msg.endswith("\n") else msg + "\n"
        sys.stderr.write(msg)
        sys.stderr.flush()


threading.excepthook = thread_excepthook
xt.print_exception = print_exc
