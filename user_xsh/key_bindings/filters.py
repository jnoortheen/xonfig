from prompt_toolkit.application import get_app
from prompt_toolkit.filters import Condition


@Condition
def suggestion_available():
    app = get_app()
    return (
        app.current_buffer.suggestion is not None and
        app.current_buffer.document.is_cursor_at_the_end
    )


@Condition
def cmd_text_available():
    app = get_app()
    return (
        app.current_buffer.text is not None and
        app.current_buffer.document.is_cursor_at_the_end
    )
