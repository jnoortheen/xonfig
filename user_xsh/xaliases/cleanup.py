from shutil import which

from user_xsh.bakery import trace_
from xontrib_commands.utils import run as R
from xontrib_commands.argerize import Command
import subprocess as sp


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

    if which("cargo"):
        # you first need to install cargo-cache with `cargo install cargo-cache`
        R("cargo cache -a")


def _cleanup_osx():
    """adapted from https://github.com/mac-cleanup/mac-cleanup-sh/blob/main/mac-cleanup"""
    #
    print("Emptying the Trash 🗑 on all mounted volumes and the main HDD...")
    R("sudo rm -rfv /Volumes/*/.Trashes/* &>/dev/null")
    R("sudo rm -rfv ~/.Trash/* &>/dev/null")

    print("Clearing System Cache Files...")
    R("sudo rm -rfv /Library/Caches/* &>/dev/null")
    R("sudo rm -rfv /System/Library/Caches/* &>/dev/null")
    R("sudo rm -rfv ~/Library/Caches/* &>/dev/null")
    R("sudo rm -rfv /private/var/folders/bh/*/*/*/* &>/dev/null")

    print("Clearing System Log Files...")
    R("sudo rm -rfv /private/var/log/asl/*.asl &>/dev/null")
    R("sudo rm -rfv /Library/Logs/DiagnosticReports/* &>/dev/null")
    R("sudo rm -rfv /Library/Logs/CreativeCloud/* &>/dev/null")
    R("sudo rm -rfv /Library/Logs/Adobe/* &>/dev/null")
    R("sudo rm -fv /Library/Logs/adobegc.log &>/dev/null")
    R(
        "rm -rfv ~/Library/Containers/com.apple.mail/Data/Library/Logs/Mail/* &>/dev/null"
    )
    R("rm -rfv ~/Library/Logs/CoreSimulator/* &>/dev/null")
    R("rm -rd ~/Library/Caches/Homebrew")
    R("rm -rd ~/Library/Caches/pypoetry")
    R("rm -rd ~/Library/Caches/pip")
    R("rm -rd ~/Library/Caches/lima")
    R("rm -rd ~/Library/Caches/pdm")


#
# if [ -d ~/Library/Logs/JetBrains/ ]; then
#   msg 'Clearing all application log files from JetBrains...'
#   rm -rfc ~/Library/Logs/JetBrains/*/ &>/dev/null
# fi
#
# if [ -d ~/Library/Application\ Support/Adobe/ ]; then
#   msg 'Clearing Adobe Cache Files...'
#   sudo rm -rfv ~/Library/Application\ Support/Adobe/Common/Media\ Cache\ Files/* &>/dev/null
# fi
#
# if [ -d ~/Library/Application\ Support/Google/Chrome/ ]; then
#   msg 'Clearing Google Chrome Cache Files...'
#   sudo rm -rfv ~/Library/Application\ Support/Google/Chrome/Default/Application\ Cache/* &>/dev/null
# fi
#
# msg 'Cleaning up iOS Applications...'
# rm -rfv ~/Music/iTunes/iTunes\ Media/Mobile\ Applications/* &>/dev/null
#
# msg 'Removing iOS Device Backups...'
# rm -rfv ~/Library/Application\ Support/MobileSync/Backup/* &>/dev/null
#
# msg 'Cleaning up XCode Derived Data and Archives...'
# rm -rfv ~/Library/Developer/Xcode/DerivedData/* &>/dev/null
# rm -rfv ~/Library/Developer/Xcode/Archives/* &>/dev/null
# rm -rfv ~/Library/Developer/Xcode/iOS Device Logs/* &>/dev/null
#
# if type "xcrun" &>/dev/null; then
# 	msg 'Cleaning up iOS Simulators...'
# 	osascript -e 'tell application "com.apple.CoreSimulator.CoreSimulatorService" to quit' &>/dev/null
# 	osascript -e 'tell application "iOS Simulator" to quit' &>/dev/null
# 	osascript -e 'tell application "Simulator" to quit' &>/dev/null
# 	xcrun simctl shutdown all &>/dev/null
# 	xcrun simctl erase all &>/dev/null
# fi
#
# # support deleting gradle caches
# if [ -d "/Users/${HOST}/.gradle/caches" ]; then
# 	msg 'Cleaning up Gradle cache...'
# 	rm -rfv ~/.gradle/caches/ &>/dev/null
# fi
#
# # support deleting Dropbox Cache if they exist
# if [ -d "/Users/${HOST}/Dropbox" ]; then
# 	msg 'Clearing Dropbox 📦 Cache Files...'
# 	sudo rm -rfv ~/Dropbox/.dropbox.cache/* &>/dev/null
# fi
#
# if [ -d ~/Library/Application\ Support/Google/DriveFS/ ]; then
#   msg 'Clearing Google Drive File Stream Cache Files...'
#   killall "Google Drive File Stream"
#   rm -rfv ~/Library/Application\ Support/Google/DriveFS/[0-9a-zA-Z]*/content_cache &>/dev/null
# fi
#
# if type "composer" &>/dev/null; then
# 	msg 'Cleaning up composer...'
# 	composer clearcache --no-interaction &>/dev/null
# fi
#
# # Deletes Steam caches, logs, and temp files
# # -Astro
# if [ -d ~/Library/Application\ Support/Steam/ ]; then
# 	msg 'Clearing Steam Cache, Log, and Temp Files...'
# 	rm -rfv ~/Library/Application\ Support/Steam/appcache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Steam/depotcache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Steam/logs &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Steam/steamapps/shadercache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Steam/steamapps/temp &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Steam/steamapps/download &>/dev/null
# fi
#
# # Deletes Minecraft logs
# # -Astro
# if [ -d ~/Library/Application\ Support/minecraft ]; then
# 	msg 'Clearing Minecraft Cache and Log Files...'
# 	rm -rfv ~/Library/Application\ Support/minecraft/logs &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/minecraft/crash-reports &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/minecraft/webcache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/minecraft/webcache2 &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/minecraft/crash-reports &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/minecraft/*.log &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/minecraft/launcher_cef_log.txt &>/dev/null
#
# 	if [ -d ~/Library/Application\ Support/minecraft/.mixin.out ]; then
# 		rm -rfv ~/Library/Application\ Support/minecraft/.mixin.out &>/dev/null
# 	fi
# fi
#
# # Deletes Lunar Client logs (Minecraft alternate client)
# # -Astro
# if [ -d ~/.lunarclient ]; then
# 	msg 'Deleting Lunar Client logs and caches...'
# 	rm -rfv ~/.lunarclient/game-cache &>/dev/null
# 	rm -rfv ~/.lunarclient/launcher-cache &>/dev/null
# 	rm -rfv ~/.lunarclient/logs &>/dev/null
# 	rm -rfv ~/.lunarclient/offline/*/logs &>/dev/null
# 	rm -rfv ~/.lunarclient/offline/files/*/logs &>/dev/null
# fi
#
# # Deletes Wget logs
# # -Astro
# if [ -d ~/wget-log ]; then
# 	msg 'Deleting Wget log and hosts file...'
# 	rm -fv ~/wget-log &>/dev/null
# 	rm -fv ~/.wget-hsts &>/dev/null
# fi
#
# # Deletes Cacher logs
# # I dunno either
# # -Astro
# if [ -d ~/.cacher ]; then
# 	msg 'Deleting Cacher logs...'
# 	rm -rfv ~/.cacher/logs
# fi
#
# # Deletes Android (studio?) cache
# # -Astro
# if [ -d ~/.android ]; then
# 	msg 'Deleting Android cache...'
# 	rm -rfv ~/.android/cache
# fi
#
# # Clears Gradle caches
# # -Astro
# if [ -d ~/.gradle ]; then
# 	msg 'Clearing Gradle caches...'
# 	rm -rfv ~/.gradle/caches
# fi
#
# # Deletes Kite Autocomplete logs
# # -Astro
# if [ -d ~/.kite ]; then
# 	msg 'Deleting Kite logs...'
# 	rm -rfv ~/.kite/logs
# fi
#
# if type "brew" &>/dev/null; then
# 	if [ "$update" = true ]; then
# 		msg 'Updating Homebrew Recipes...'
# 		brew update &>/dev/null
# 		msg 'Upgrading and removing outdated formulae...'
# 		brew upgrade &>/dev/null
# 	fi
# 	msg 'Cleaning up Homebrew Cache...'
# 	brew cleanup -s &>/dev/null
# 	rm -rfv "$(brew --cache)"
# 	brew tap --repair &>/dev/null
# fi
#
# if type "gem" &>/dev/null; then
# 	msg 'Cleaning up any old versions of gems'
# 	gem cleanup &>/dev/null
# fi
#
# if type "docker" &>/dev/null; then
# 	if ! docker ps >/dev/null 2>&1; then
# 		open --background -a Docker
# 	fi
# 	msg 'Cleaning up Docker'
# 	docker system prune -af &>/dev/null
# fi
#
# if [ "$PYENV_VIRTUALENV_CACHE_PATH" ]; then
# 	msg 'Removing Pyenv-VirtualEnv Cache...'
# 	rm -rfv "$PYENV_VIRTUALENV_CACHE_PATH" &>/dev/null
# fi
#
# if type "npm" &>/dev/null; then
# 	msg 'Cleaning up npm cache...'
# 	npm cache clean --force &>/dev/null
# fi
#
# if type "yarn" &>/dev/null; then
# 	msg 'Cleaning up Yarn Cache...'
# 	yarn cache clean --force &>/dev/null
# fi
#
# if type "pod" &>/dev/null; then
# 	msg 'Cleaning up Pod Cache...'
# 	pod cache clean --all &>/dev/null
# fi
#
# if type "go" &>/dev/null; then
# 	msg 'Clearing Go module cache...'
# 	go clean -modcache &>/dev/null
# fi
#
# # Deletes all Microsoft Teams Caches and resets it to default - can fix also some performance issues
# # -Astro
# if [ -d ~/Library/Application\ Support/Microsoft/Teams ]; then
# 	# msg 'Deleting Microsoft Teams logs and caches...'
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/IndexedDB &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/Cache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/Application\ Cache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/Code\ Cache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/blob_storage &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/databases &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/gpucache &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/Local\ Storage &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/tmp &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/*logs*.txt &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/watchdog &>/dev/null
# 	rm -rfv ~/Library/Application\ Support/Microsoft/Teams/*watchdog*.json &>/dev/null
# fi
#
# msg 'Cleaning up DNS cache...'
# sudo dscacheutil -flushcache &>/dev/null
# sudo killall -HUP mDNSResponder &>/dev/null
#
# msg 'Purging inactive memory...'
# sudo purge &>/dev/null
#
# msg "${GREEN}Success!${NOFORMAT}"
#
# newAvailable=$(df / | tail -1 | awk '{print $4}')
# count=$((newAvailable - oldAvailable))
# bytesToHuman $count


def _print_big_files():
    print("files bigger than 500MB")
    R("sudo find / -size +500000 -print")


@Command.reg_no_thread
@trace_
def cleanup():
    # old_available = sp.check_call("df / | tail - 1 | awk '{print $4}'", shell=True)
    _cleanup_tools()
    _cleanup_linux()
    _cleanup_package_managers()
    # _print_big_files()
