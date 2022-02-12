import pytest
from .proc import *


@pytest.fixture(params=["fg", "bg"])
def wait_or_bg(request):
    return request.param


def test_single_cmd(wait_or_bg):
    # with cases
    #   in fg and bg
    #   1. without capture
    #  with or without pty
    #   2. capture out
    #   3. capture out/err
    ls = Spec("ls", "-a", "-l", "-h")

    pg = ls()
    if wait_or_bg == "fg":
        pg.wait()
    else:
        pytest.fail("Not implemented")
