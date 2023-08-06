# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/MrCode403/Jarves/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/MrCode403/Jarves/blob/main/LICENSE/>.

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from pyJarves import *
from pyJarves import _ult_cache
from pyJarves._misc import owner_and_sudos
from pyJarves._misc._assistant import asst_cmd, callback, in_pattern
from pyJarves.fns.helper import *
from pyJarves.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = ultroid_bot.full_name
OWNER_ID = ultroid_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException:
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
