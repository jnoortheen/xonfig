from shutil import which

from user_xsh.bakery import trace_
from xontrib_commands.utils import Command, run as R


def _cleanup_linux():
    if which("snap"):
        print("Delete old snap packages")
        older_snaps = R("env LANG=en_US.UTF-8 snap list --all")
        for snap in older_snaps.splitlines():
            if "disabled" not in snap:
                continue
            snap_name, vers, revision, *_ = snap.split()
            R("sudo", "snap", "remove", snap_name, "--revision", revision)

    if which("pacman"):
        print("/n/n pacman cache clear")
        R("sudo paccache -rk1")

    if which("journalctl"):
        print("clean journalctl logs past 7days")
        R("sudo journalctl --vacuum-time=2d")


def _cleanup_tools():
    if which("docker"):
        print("docker clean")
        R("docker system prune -f")
        R("docker builder prune -f")


def _cleanup_package_managers():
    if which("nix"):
        print("delete old nix generations")
        R("nix-env --delete-generations old")
        R("sudo nix-env --delete-generations old")
        R("nix-collect-garbage --delete-old")
        R("sudo nix-collect-garbage --delete-old")
        R("nix-store --gc")

    if which("yarn"):
        print("clean yarn")
        R("yarn cache clean")

    if which("brew"):
        print("brew cleanup all files 0-days")
        R("brew autoremove")
        R("brew cleanup --prune 0")
        R("brew doctor")


def _cleanup_osx():
    """adapted from https://github.com/mac-cleanup/mac-cleanup-sh/blob/main/mac-cleanup"""


def _print_big_files():
    print("files bigger than 500MB")
    R("sudo find / -size +500000 -print")


@Command.reg_no_thread
@trace_
def cleanup():
    _cleanup_tools()
    _cleanup_linux()
    _cleanup_package_managers()
    _print_big_files()
