def _get_branches() -> str:
    from xontrib_commands.utils import run

    output = run("git branch").strip()
    return output
    # return tuple(br.strip() for br in output.splitlines())


def _get_dev_branch():
    branches = _get_branches()
    if "develop" in branches:
        return "develop"
    return "dev"


def _get_main_branch():
    branches = _get_branches()
    if "master" in branches:
        return "master"
    return "main"


def _git_checkout(func):
    def _wrapper(buffer, word):
        branch = func()
        return "git checkout " + branch

    return _wrapper


def _git_checkout_merge(check_func, merge_func):
    def _wrapper(buffer, word):
        check = check_func()
        merge = merge_func()
        return f"git checkout {check} && git merge {merge}"

    return _wrapper


git_abbrevs = dict(
    # cola="git-cola 2> /dev/null &",
    gl="git log --oneline --all --graph",
    gf="git fetch --all --prune --tags",
    gp="git push --follow-tags",
    gpl="git pull",
    # git workflows
    # gc = "git commit -m ! ",
    # gca = "git commit --amend",
    # gcan = "git commit --amend --no-edit",
    # gsc = "git switch --create <edit> parent/main",
    gcd=_git_checkout(_get_dev_branch),
    gcdm=_git_checkout_merge(_get_dev_branch, _get_main_branch),
    gcm=_git_checkout(_get_main_branch),
    gcmd=_git_checkout_merge(_get_main_branch, _get_dev_branch),
)
# systemctl_abbrevs = dict(
#     # systemd
#     sstart="sudo systemctl start",
#     sstop="sudo systemctl stop",
#     srestart="sudo systemctl restart",
#     sstatus="sudo systemctl status",
#     senable="sudo systemctl enable",
#     sdisable="sudo systemctl disable",
#     smask="sudo systemctl mask",
#     sunmask="sudo systemctl unmask",
#     sreload="sudo systemctl daemon-reload",
#     sfailed="sudo systemctl list-units --failed",
#     ustart="systemctl start --user",
#     ustop="systemctl stop --user",
#     urestart="systemctl restart --user",
#     ustatus="systemctl status --user",
#     uenable="systemctl enable --user",
#     udisable="systemctl disable --user",
#     ureload="sudo systemctl daemon-reload --user",
# )

python_abbrevs = dict(
    pipup="pip install --upgrade pip",
    pt="poetry",
    vav="vox activate .venv",
    vd="vox deactivate",
    vap="vox activate @$(poetry env info -p)",
)

django_abbrevs = dict(
    pm="python manage.py",
    pmm="python manage.py migrate",
    pmk="python manage.py makemigrations",
)

# nixos_abbrevs = dict(
#     osbuild="sudo nixos-rebuild",
#     oswitch="os-build switch",
#     ostest="os-build test",
# )

# arch_linux_abbrevs = dict(
#     # yay = "yay --cleanafter",
#     yay="paru",
# )
clis_abbrevs = dict(
    # lf = "lefthook",
    ll="ls -alh",
    dc="docker compose",
    dr="docker run --rm -ti",
    drun="docker run --rm -ti",
    dsa="docker-stop-all",
    grep="grep --ignore-case",
    cat="bat",
    time="time -p",
    xodo="subl ~/src/shell/TODO.todo",
    xcode="code ~/src/shell",
    alias="subl ~/src/shell/aliases.py",
    abbr="subl ~/src/shell/abbrevs.py",
    # nproc="sysctl -n hw.ncpu",
    ncdu="dua i",
    df="duf",
    # ps = "procs",
)

shell_abbrevs = {"|&": "2>&1 |"}
