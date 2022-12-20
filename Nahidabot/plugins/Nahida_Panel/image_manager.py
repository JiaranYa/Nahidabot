from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.rule import to_me

from Nahidabot.database import Player, PropList
from Nahidabot.utils.classmodel import Role

from .draw_panel import draw_role_info

info_panel = on_command("nhd", rule=to_me(), aliases={"角色面板"}, priority=5, block=True)


@info_panel.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    name = msg.extract_plain_text()
    feedback = Message()
    (uid,) = await Player.filter(user_qq=event.user_id).values_list("uid", flat=True)

    (role,) = await PropList.filter(
        user_qq=event.user_id, uid=uid, role_name=name
    ).all()
    role_model = Role(
        name=name,
        info=role.info,
        fight_prop=role.property,
        weapon=role.weapon,
        artifacts=role.artifacts,
        scores=role.scores,
        buff_list=role.buff_info,
        dmg_list=role.dmg_info,
    )
    if img := await draw_role_info(role_model, role.uid, role.update_time):
        feedback += img
        await info_panel.finish(feedback)
    else:
        await info_panel.finish("没有该角色信息")


dmg_panel = on_command("设置", rule=to_me(), aliases={"test"}, priority=5, block=True)


@dmg_panel.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    from Nahida_Calc.role_model import RoleModel

    role = RoleModel(name="行秋")
    # await role.update_from_database(user_qq=event.get_user_id())
    # await role.get_buff()
    # await role.get_dmg()

    pass
