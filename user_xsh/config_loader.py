import functools
import shlex
import threading
import typing as tp
from pathlib import Path
from queue import Queue

import sys

from xonsh.aliases import Aliases


class BgThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    def run(self):
        while True:
            args = self.queue.get()
            if args is None:
                self.queue.task_done()
                return

            if callable(args):
                args()
            self.queue.task_done()

    def quit(self):
        self.queue.put(None)


def exec_module(path: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(f"uxsh.{path.name}", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def update_xonsh_dict(path: Path, var):
    module = exec_module(path)
    special = {}
    try:
        if callable(var):
            var = var()

        for key, val in vars(module).items():  # type: str, tp.Any
            if (not key.startswith("__")) and key.startswith("_") and key.endswith("_"):
                special[key] = val
            else:
                if isinstance(var, Aliases) and isinstance(val, str):
                    # list is faster than string as alias
                    val = shlex.split(val)
                if path.name.endswith("abbrevs.py") and key.endswith("_abbrevs"):
                    var.update(val)
                else:
                    var[key] = val

    except:
        from rich import console

        c = console.Console()
        c.print_exception(show_locals=True)

    return special


class Loader:
    """special importer with option to load in thread"""

    def __init__(
        self,
        root_path: Path,
        xontribs: tp.Tuple[str, ...] = (),
        modules: tp.Tuple[str, ...] = (),
    ):
        self.modules = modules + self.to_xontribs(*xontribs)
        self.root = root_path

    @staticmethod
    def to_xontribs(*names: str):
        return tuple(map(lambda x: f"xontrib.{x}", names))

    def import_mods(self, *mods):
        import importlib

        for mod in mods:
            try:
                imp_mod = importlib.import_module(mod)
                if not imp_mod.__file__.endswith(".py"):
                    print(
                        "Not a python module. may slowdown the loading",
                        imp_mod.__file__,
                    )
            except Exception as ex:
                print(f"Failed to import {mod} - {ex}", file=sys.stderr)

    def load_config_files(self, file: Path):
        from xonsh.built_ins import XSH
        from xontrib.abbrevs import abbrevs

        for x, var in (
            ("variables.py", XSH.env),
            ("abbrevs.py", abbrevs),
            ("aliases.py", XSH.aliases),
        ):
            ext_vars = update_xonsh_dict(file / x, var)
            if ext_vars:
                self.update_modules(ext_vars)

    def get_functions(self):
        yield functools.partial(self.load_config_files, file=self.root)
        for imp in self.modules:
            yield functools.partial(self.import_mods, imp)

    @functools.cached_property
    def _thread(self):
        thread = BgThread(daemon=True)
        thread.start()
        return thread

    def in_bgthread(self):
        for func in self.get_functions():
            self._thread.queue.put(func)

        # note: wait for threads before completing rc.py
        return lambda: self._thread.queue.join()

    def normal(self):
        for func in self.get_functions():
            func()
        return lambda: 1

    def with_futures(self):
        # running with this is slow
        import concurrent.futures as cf

        exc = cf.ThreadPoolExecutor(max_workers=2)
        futures = [exc.submit(fn) for fn in self.get_functions()]
        return lambda: list(cf.as_completed(futures))

    def update_modules(self, ext_vars: "dict[str, ...]"):
        if modules := ext_vars.get("_modules_"):
            self.modules += modules
