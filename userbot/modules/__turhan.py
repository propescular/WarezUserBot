# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# turhan UserBot - Yusuf Usta
#

""" UserBot yardım komutu """

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.turhan(?: |$)(.*)")
async def turhan(event):
    """ .turhan komutu için """
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Lütfen bir Turhan modülü adı belirtin.")
    else:
        await event.edit("Lütfen hangi Turhan modülü için yardım istediğinizi belirtin !!\
            \nKullanım: .turhan <modül adı>")
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)
