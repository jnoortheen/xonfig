# lf = "lefthook"
ll = "ls -alh"

dc = "docker compose"
dr = "docker run --rm -ti"
drun = "docker run --rm -ti"
dsa = "docker-stop-all"

pm = "python manage.py"
pmm = "python manage.py migrate"
pmk = "python manage.py makemigrations"
grep = "grep --ignore-case"

# nix os
osbuild = "sudo nixos-rebuild"
oswitch = "os-build switch"
ostest = "os-build test"

cat = "bat"
time = "time -p"

xodo = "subl ~/src/shell/TODO.todo"
xcode = "code ~/src/shell"
alias = "subl ~/src/shell/aliases.py"
abbr = "subl ~/src/shell/abbrevs.py"

cola = "git-cola 2> /dev/null &"
gl = "git log --oneline --all --graph"
gf = "git fetch --all --prune --tags"
gp = "git push --follow-tags"
gpl = "git pull"
# gc = "git commit -m ! "
# gca = "git commit --amend"
# gcan = "git commit --amend --no-edit"
# gsc = "git switch --create <edit> parent/main"
nproc = "sysctl -n hw.ncpu"


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


gcd = _git_checkout(_get_dev_branch)
gcdm = _git_checkout_merge(_get_dev_branch, _get_main_branch)
gcm = _git_checkout(_get_main_branch)
gcmd = _git_checkout_merge(_get_main_branch, _get_dev_branch)

# sstart = "sudo systemctl start"
# sstop = "sudo systemctl stop"
# srestart = "sudo systemctl restart"
# sstatus = "sudo systemctl status"
# senable = "sudo systemctl enable"
# sdisable = "sudo systemctl disable"
# smask = "sudo systemctl mask"
# sunmask = "sudo systemctl unmask"
# sreload = "sudo systemctl daemon-reload"
# sfailed = "sudo systemctl list-units --failed"
#
# ustart = "systemctl start --user"
# ustop = "systemctl stop --user"
# urestart = "systemctl restart --user"
# ustatus = "systemctl status --user"
# uenable = "systemctl enable --user"
# udisable = "systemctl disable --user"
# ureload = "sudo systemctl daemon-reload --user"

pipup = "pip install --upgrade pip"
pt = "poetry"

# yay = "yay --cleanafter"

vav = "vox activate .venv"
vd = "vox deactivate"
vap = "vox activate @$(poetry env info -p)"

ncdu = "dua i"
df = "duf"

yay = "paru"

# ps = "procs"
