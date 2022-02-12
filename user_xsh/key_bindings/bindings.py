from prompt_toolkit.key_binding import KeyPressEvent
from prompt_toolkit.keys import Keys
from xontrib.hist_navigator import insert_text

from . import filters


def complete_arg(event, arg: str):
    b = event.current_buffer
    if b.text:
        arg = ("" if b.text.endswith(" ") else " ") + "--" + arg
        insert_text(event, arg)


@events.on_ptk_create  # noqa
def custom_keybindings(bindings, **_):
    if not hasattr(bindings, "add"):
        return

    handler = bindings.add

    @handler(Keys.ControlE, filter=filters.suggestion_available)
    def execute_auto_suggestion(event):
        """it is equivalent to ctrl+j and enter.
        in single step execute the suggestion
        """
        suggestion = event.current_buffer.suggestion

        if suggestion:
            insert_text(event, suggestion.text)

    @handler("escape", "h", filter=filters.cmd_text_available)
    def execute_help(event):
        """equivalent to typing --help + <enter>

        Usage: one should press Alt+h
        """
        complete_arg(event, "help")

    @handler("escape", "v", filter=filters.cmd_text_available)
    def execute_version(event):
        """equivalent to typing `cmd --version`"""
        complete_arg(event, "version")

    @handler("escape", "s", filter=filters.cmd_text_available)
    def run_git_status(event):
        """Show git status"""
        insert_text(event, "git status")

    @handler("escape", "b", filter=filters.cmd_text_available)
    def run_git_status(event):
        """Show git status"""
        insert_text(event, "git branch")

    @handler("escape", "p", filter=filters.cmd_text_available)
    def run_git_status(event):
        """Show git status"""
        insert_text(event, "git push")

    @handler("escape", "c", filter=filters.cmd_text_available)
    def start_cola(event: KeyPressEvent):
        """start cola"""
        insert_text(event, "git-cola 2> /dev/null &")
