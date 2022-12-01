from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.rule import to_me

from Nahidabot.database import Player, PropList

from .draw_panel import draw_role_info

info_panel = on_command("面板", rule=to_me(), priority=5, block=True)


@info_panel.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    feedback = Message()
    [uid,] = await Player.filter(
        user_qq=event.user_id
    ).values_list("uid", flat=True)
    # TODO: 角色名来自于查询命令
    [
        role,
    ] = await PropList.filter(user_qq=event.user_id, uid=uid, role_name="雷电将军").all()
    if img := await draw_role_info(role):
        feedback += img
        await info_panel.finish(feedback)
    else:
        await info_panel.finish("没有该角色信息")


# dmg_panel = on_command("伤害",rule=to_me(),priority=5,block=True)

# @dmg_panel.handle()
# async def _(event:MessageEvent,msg:Message = CommandArg()):
#     from Nahida_Calc.role import dmg_info

#     dmg_info()
