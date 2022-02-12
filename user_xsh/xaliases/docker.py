from user_xsh.bakery import current_folder_name
from xontrib_commands.utils import Command, run as R


def stop(cont, current_check=False):
    remove = True
    if current_check:
        remove = not running_wd(cont)
    if remove:
        R("docker", "container", "stop", cont)
        R("docker", "container", "rm", cont)


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


@Command.reg
def docker_stop_all():
    for cont in R("docker", "container", "ls", "-aq", capture=True).splitlines():
        stop(cont, True)
