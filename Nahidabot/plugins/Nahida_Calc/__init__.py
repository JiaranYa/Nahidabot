from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.rule import to_me

from Nahidabot.database.models import PropList

from .dmg_model import *
from .role_model import *

dmg_panel = on_command("test", rule=to_me(), priority=5, block=True)


@dmg_panel.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    ((talent, prop),) = await PropList.filter(role_name="雷电将军").values_list(
        "talent", "property"
    )
    result = buff_info(Role(name="雷电将军", talent=talent, fight_prop=prop))
    print(result)
