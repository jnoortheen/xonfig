from user_xsh.bakery import current_folder_name, trace_
from xontrib_commands.utils import run as R
from xontrib_commands.argerize import Command


def stop(cont, current_check=False):
    remove = True
    if current_check:
        remove = not running_wd(cont)
    if remove:
        R("docker", "stop", cont)
        R("docker", "rm", cont)


def running_wd(cont):
    ps = R(
        "docker", "ps", "--filter", f"id={cont}", "--format", "{{.Names}}", capture=True
    )
    return current_folder_name() in ps


def compose_up(*services):
    # trace on
    docker_stop_all()
    R("docker-compose", "up", "-d", services)
    # trace off


@Command.reg_no_thread
@trace_
def docker_stop_all(no_cwd=False):
    """

    Parameters
    ----------
    no_cwd
        do not stop if started in current working directory using docker-compose

    """
    for cont in R("docker", "container", "ls", "-aq", capture=True).splitlines():
        print(f"stopping {cont}...")
        stop(cont, no_cwd)
