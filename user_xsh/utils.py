import typing as tp
from pathlib import Path

import sys
import time

from xonsh.lazyasd import lazyobject
from xonsh.built_ins import XSH


@lazyobject
def xsh():
    return XSH


def add_traceback(record):
    """
    https://loguru.readthedocs.io/en/stable/resources/recipes.html#displaying-a-stacktrace-without-using-the-error-context
    """
    import traceback

    # use it like
    # logger.bind(with_traceback=True).info("With traceback")
    extra = record["extra"]
    if extra.get("with_traceback", False):
        extra["traceback"] = "\n" + "".join(traceback.format_stack())
    else:
        extra["traceback"] = ""


@lazyobject
def logger():
    from loguru import logger

    logger.remove()
    log = logger.patch(add_traceback)
    log.add(
        Path(__file__).resolve().with_name("xsh.log"),
        format="{time}|{level}|{file}:{line}|{message}{extra[traceback]}",
        encoding="utf-8",
    )
    return log


def append_to_path(path: Path, *args):
    with path.open("a") as f:
        msg = " ".join(map(str, args))
        f.write(msg)
        f.write("\n")


class Durations:
    _indent = [-1]
    """class variable that gets changed inside instance as well"""

    def __init__(
        self,
        log: tp.Union[bool, Path] = True,
        disable=False,
        indent=None,
        show_time=False,
        prefix="",
    ):
        self.disable = disable
        self.start = time.time()
        self.last = time.time()
        self.show_time = show_time
        self.prefix = prefix
        self._indent[0] += 1
        self.indent = self._indent[0] if indent is None else indent
        self.log = log

    def print(self, *args, show_time=False, **kwargs):
        if self.disable:
            return
        delta = round(time.time() - self.last, 3)
        total = round(time.time() - self.start, 3)
        indent = max(self.indent, 0) * "\t"

        data = [
            f"{delta=}",
            f"{total=}",
            f'{" ".join((str(a) for a in args))}',
        ]
        if kwargs:
            data.append(str(kwargs))
        if self.show_time or show_time:
            from datetime import datetime

            now = datetime.now()
            data.insert(0, str(now))
        if self.prefix:
            data.insert(0, f"{self.prefix}:")
        msg = indent + " | ".join(data)

        if self.log:
            path = Path(__file__).resolve().with_name("xsh.out")
            if not isinstance(self.log, bool):
                path = self.log
            append_to_path(path, msg)
        else:
            print(msg, file=sys.stderr)
        self.last = time.time()


def set_env(name: str, value: tp.Any):
    xsh.env[name] = value


def get_env(name: str) -> tp.Any:
    return xsh.env.get(name)
