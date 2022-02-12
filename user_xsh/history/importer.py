import os
import sqlite3
import time
import uuid

FISH_HIST = "~/.local/share/fish/fish_history"
XONSH_HIST = "~/.local/share/xonsh/xonsh-history.sqlite"
# todo: change this to generic history backend -- append method
# todo: add this as a subcommand to `xonsh history`
SQL = f"""
INSERT INTO xonsh_history (inp, rtn, tsb, tse, sessionid, out, info)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

sess_id = uuid.uuid4()


def import_fish_history():
    fish_history = os.path.expanduser(FISH_HIST)
    from collections import OrderedDict
    cmds = OrderedDict()
    with open(fish_history) as fr:
        for line in fr.read().splitlines():
            if line.startswith("-"):
                _, cmd = line.split("cmd:")
                cmds[cmd.strip()] = None

    conn = sqlite3.connect(os.path.expanduser(XONSH_HIST))
    curr = conn.cursor()
    for cmd in cmds:
        curr.execute(SQL, (
            cmd, 0, time.time(), time.time() + 1, str(uuid), None, None
        ))
    conn.commit()
    conn.close()
