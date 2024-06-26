import os.path

from user_xsh.bakery import current_folder_name, trace_
from xonsh.built_ins import XSH
from xontrib_commands.argerize import Command
from xontrib_commands.utils import run as R


@Command.reg
@trace_
def node_modules_cleanup(path="."):
    """Remove node_modules folders in the current directory and levels below"""
    folders = R(path, "-name", "node_modules", "-type", "d")
    for fold in folders.strip().splitlines():
        R("node-prune", fold)


@Command.reg
@trace_
def os_build(args):
    R("sudo", "nixos-rebuild", args)
    R(
        "nix-store",
        "--query",
        "--requisites",
        "/run/current-system",
        "|",
        "cut",
        "-d-",
        "-f2-",
        "|",
        "sort",
        "|",
        "uniq",
        ">",
        "/etc/nixos/pkgs.txt",
    )


@Command.reg_no_thread
@trace_
def record_stats(pkg_name=".", path=".local/stats.txt"):
    stat = R("scc", pkg_name)
    date = R("date")
    R(["echo", date + stat], ["tee", "-a", path])


def cmd(fn):
    name = fn.__name__
    name = name.replace("_", "-")
    XSH.aliases[name] = fn
    return fn


def _start_cola():
    folder = current_folder_name()
    cola_ps = R("ps x | grep cola").strip()
    if cola_ps:
        ps_dir = R("pwdx", cola_ps.split()[0])
        if folder in ps_dir:
            return
    R("poetry run cola &")


@Command.reg_no_thread
@trace_
def release_poetry_sof(version="patch"):
    """
        Release a new version for poetry based projects
    Parameters
    ----------
    version
        type of the new version. could be one of patch/minor/major...
    """
    msg = R("poetry", "version", version)
    print(msg)
    version = msg.split()[-1]
    ans = input(f"Upload version {version} ? [Y/n]")
    if ans and ans.lower()[0] in {"n"}:
        return

    R("git", "commit", "-a", "-m", msg)
    R("git", "tag", f"v{version}")
    R("git", "push")
    R("git", "push", "--tags")
    R("poetry", "publish", "--build")


@Command.reg_no_thread
@trace_
def release_pdm_sof(version="patch"):
    """
        Release a new version for poetry based projects
    Parameters
    ----------
    version
        type of the new version. could be one of patch/minor/major...
    """
    msg = R("pdm", "bump", version)
    version = R("pdm", "show", "--version").strip()
    ans = input(f"Upload version {version} ? [Y/n]")
    if ans and ans.lower()[0] in {"n"}:
        return

    R("git", "commit", "-a", "-m", msg)
    R("git", "tag", f"v{version}")
    R("git", "push")
    R("git", "push", "--tags")

    if not os.path.exists(".github"):
        R("pdm", "publish")
