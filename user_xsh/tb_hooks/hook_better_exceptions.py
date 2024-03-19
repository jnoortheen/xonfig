"""integration better-exceptions with Xonsh"""

import better_exceptions

from user_xsh.tb_hooks.commonlib import start_patching

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


start_patching(print_exc, thread_excepthook)
