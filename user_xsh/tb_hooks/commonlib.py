def start_patching(print_exception, thread_excepthook):
    from unittest.mock import patch

    patch("xonsh.tools.print_exception", print_exception).start()
    patch("xonsh.events.print_exception", print_exception).start()
    patch("xonsh.completer.print_exception", print_exception).start()
    patch("threading.excepthook", thread_excepthook).start()
