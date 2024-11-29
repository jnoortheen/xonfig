import os


VC_BRANCH_TIMEOUT = 10  # default 0.1 seconds
# ENABLE_ASYNC_PROMPT = True
ASYNC_PROMPT_THREAD_WORKERS = 10
VIRTUAL_ENV_DISABLE_PROMPT = False

AUTO_CD = True  # change directory without cd

XONSH_SHOW_TRACEBACK = True
# AUTO_SUGGEST_IN_COMPLETIONS = True
CASE_SENSITIVE_COMPLETIONS = False

BETTER_EXCEPTIONS = 1

# While tab-completions menu is displayed,
# press <Enter> to confirm completion instead of running command.
COMPLETIONS_CONFIRM = True
COMPLETION_IN_THREAD = True

COMPLETIONS_DISPLAY = (
    "single"
    # "multi"
)
COMPLETIONS_MENU_ROWS = 8

# The number of completions to display before the user is asked for confirmation.
COMPLETION_QUERY_LIMIT = 20

# PROMPT_REFRESH_INTERVAL = 10
# https://github.com/santagada/xontrib-powerline/blob/master/xontrib/powerline.xsh
PROMPT = "".join(
    [
        # "{vte_new_tab_cwd}",
        "{cwd:{}}",
        "{gitstatus:{}}",
        "{ret_code}",
        "{background_jobs}",
        "{long_cmd_duration:⌛{}}",
        os.linesep,
        "{prompt_end}",
    ]
)
RIGHT_PROMPT = "".join(
    (
        # "{long_cmd_duration:⌛{}}",
        "{full_env_name:🐍{}}",
        # "{user_at_host}",
        # "{localtime:{}}",
        # "{iterm2_end}",
    )
)
POWERLINE_MODE = (
    "up"
    # "round"
)

# Completions display is evaluated and presented whenever a key is pressed. This avoids the need to press TAB
# having some issues with history completer. It doesn't show full line. circling long python codes become a problem.
# UPDATE_COMPLETIONS_ON_KEYPRESS = True

# MOUSE_SUPPORT = True # scroll is not working if enabled

HISTCONTROL = "erasedups"
XONSH_AUTOPAIR = True  # paranthesis and brackets completion
XONSH_COLOR_STYLE = (
    # 'colorful'
    # "native"
    # 'vim'
    "default"
)

# https://xon.sh/tutorial_hist.html#sqlite-history-backend
XONSH_HISTORY_BACKEND = "sqlite"
XONSH_HISTORY_MATCH_ANYWHERE = True
XONSH_HISTORY_SIZE = (1_00_00_000, "commands")

# docker building using buildkit
COMPOSE_DOCKER_CLI_BUILD = 1
DOCKER_BUILDKIT = 1

# for making rich.console.pager work
# PAGER = 'bat --paging=always --pager "less -RF"'
PAGER = (
    "less"
    " --quit-if-one-screen"  # quit if one screen
    " --chop-long-lines"  # press right arrow to see more
    " --RAW-CONTROL-CHARS"  # support ansi color
    " --LONG-PROMPT"
    " --ignore-case"
)
# color support for less
# LESS = "-R"
# LESSOPEN = "|pygmentize -g %s"


# colorful man pages
MANPAGER = "sh -c 'col -bx | bat -l man -p'"

_base_src = "~/src"

PROJECT_PATHS = [
    f"{_base_src}/py/",
    f"{_base_src}/py/_repos/",
    f"{_base_src}/py/divisible/",
    f"{_base_src}/py/_forks/",
    f"{_base_src}/shell/xontribs",
]

COMMANDS_CACHE_SAVE_INTERMEDIATE = True

# fzf
fzf_history_binding = "c-r"  # Ctrl+R
fzf_ssh_binding = "c-s"  # Ctrl+S
fzf_file_binding = "c-t"  # Ctrl+T
fzf_dir_binding = "c-g"  # Ctrl+G

# If we disable it, then tab-completer prints things on prompt
# it enabled: on-cd writes to stdout suffers
THREAD_SUBPROCS = False

BASH_COMPLETIONS = ["/opt/homebrew/Cellar/bash-completion/1.3_3/etc/bash_completion"]

# RAISE_SUBPROC_ERROR = True

CMD_COMPLETIONS_SHOW_DESC = True
