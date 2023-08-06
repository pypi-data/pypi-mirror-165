# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"basic"


import time


from gcid.handler import Commands
from gcid.run import starttime
from gcid.utils import elapsed


def cmd(event):
    event.reply(",".join(sorted(Commands.cmds)))


def upt(event):
    event.reply(elapsed(time.time()-starttime))
