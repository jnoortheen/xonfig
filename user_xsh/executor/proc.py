import sys

import asyncio
from asyncio import subprocess as ap, transports, protocols, events
import subprocess
import typing as tp

Spreadable = "str|list[str]|tuple[str]"


class Proc(ap.Process):
    """add proc specific methods here"""


class ProcGroup(tp.NamedTuple):
    """Group of"""

    runnable: "Spec|PipeLine"

    def wait(self):
        """wait for process to exit"""
        # loop = asyncio.get_event_loop()
        # loop.create_task(self.runnable.run())
        # loop.run_forever()
        asyncio.run(self.runnable.run())


if tp.TYPE_CHECKING:
    C = tp.TypeVar("C", bound="IChainable")
    CaptureType = tp.Optional[tp.Literal["out", "all"]]

    class IChainable(tp.Protocol):
        def chain(self, other: "C") -> "C":
            ...

    class IRunnable(tp.Protocol):
        def __call__(self, *args, **kwargs):
            ...

        def run(self):
            ...


class Chainable:
    def __or__(self, other):
        """create a chain piping self.out -> other.in"""
        return self.chain(other)

    def chain(self, other):
        return PipeLine(self, other)


class Spec(Chainable):
    def __init__(self, program: str, *args: Spreadable):
        self.program = program
        self.args: "tuple[str]" = tuple(self._get_args(*args))

    def __str__(self):
        return f"<{self.__class__.__name__}>: {self.args}"

    def write_to(self):
        """any fd > outfile/fd"""

    #             # pytest 8>&1 9>&2 1>/dev/null 2>&1

    def append_to(self):
        """any fd >> outfile"""

    def read_from(self):
        """any < fd"""

    def _get_args(self, *args: Spreadable):
        for arg in args:
            if isinstance(arg, str):
                yield arg
            else:  # list[str], tuple[str]
                # we may extend support more number of Python types
                yield from arg

    def __getitem__(self, args: Spreadable):
        """plumbum style arguments"""
        return Spec(self.program, *self.args, args)

    def __or__(self, other):
        """create a chain piping self.out -> other.in"""
        return PipeLine(self, other)

    async def run(self):
        process = await ap.create_subprocess_exec(
            self.program,
            *self.args,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        await process.communicate()
        await process.wait()
        print(process)

    def __call__(self, capture: "CaptureType" = None):
        # create new loop and return ProcessGroup
        return ProcGroup(self)


class PipeLine(Chainable):
    """A source to destination flow"""

    def __init__(self, source: "IChainable", dest: "Spec"):
        # todo: update stdin, stdout of these specs
        self.source = source
        self.dest = dest


if __name__ == "__main__":
    ap.create_subprocess_exec("ls", "-alh")
