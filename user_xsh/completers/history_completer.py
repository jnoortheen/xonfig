import typing as tp

import xonsh.completers.completer
from xonsh.built_ins import XSH
from xonsh.completers.tools import RichCompletion, contextual_command_completer
from xonsh.parsers.completion_context import CommandContext

if tp.TYPE_CHECKING:
    from xonsh.history.base import History


@contextual_command_completer
def sqlite_hist_completer(ctx: CommandContext):
    """Xonsh history completer for sqlite backend."""
    args = ctx.words_before_cursor
    hist: "History" = XSH.history

    if (not ctx.text_before_cursor) or (not ctx.prefix):
        return

    for entry in hist.all_items(True):
        yield RichCompletion(
            str(entry),
            description=str(entry),
            style="bg:ansiyellow fg:ansiblack",
        )


xonsh.completers.completer.add_one_completer(
    "sqlite_history",
    sqlite_hist_completer,
    # "start"
)
