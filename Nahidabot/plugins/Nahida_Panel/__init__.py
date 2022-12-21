import math
import re

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import Arg, ArgPlainText, CommandArg
from nonebot.rule import to_me
from nonebot.typing import T_State

from Nahidabot.database import Player, PropList
from Nahidabot.utils.classmodel import Role

from .draw_panel import draw_role_info, draw_setting_info

# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
setting_panel = on_command("set", rule=to_me(), aliases={"设置"}, priority=5, block=True)


@setting_panel.handle()
async def _(event: MessageEvent, state: T_State, msg: Message = CommandArg()):
    name = msg.extract_plain_text()
    feedback = Message()
    (uid,) = await Player.filter(user_qq=event.user_id).values_list("uid", flat=True)

    (role,) = await PropList.filter(
        user_qq=event.user_id, uid=uid, role_name=name
    ).all()
    state["user_qq"] = event.user_id
    state["uid"] = uid
    state["name"] = name

    role_model = Role(
        name=name,
        info=role.info,
        buff_list=role.buff_info,
        dmg_list=role.dmg_info,
    )
    state["role"] = role_model
    if img := await draw_setting_info(role_model, role.uid):
        feedback += img
        await info_panel.send(feedback)
    else:
        await info_panel.finish("没有该角色信息")


@setting_panel.got("setting", prompt="请输入要更改的设置，或回答【取消】退出")
async def _(
    role: Role = Arg("role"),
    settings=ArgPlainText("setting"),
    user_qq=Arg("user_qq"),
    uid=Arg("uid"),
    role_name=Arg("name"),
):
    setting_list = settings.strip().split(" ")
    for setting in setting_list:
        key, value = setting.split("-")
        if "S" in key:
            if str := re.search(r"\d+", key):
                idx = int(str.group())
                b = role.buff_list[idx]
                b.setting.label = value
        if "W" in key:
            if str := re.search(r"\d+", key):
                idx = int(str.group())
                d = role.dmg_list[idx]
                if value.isdigit():
                    if idx == 0:
                        d.weight = max(math.ceil(float(value) / 5) * 5, 100)
                    else:
                        d.weight = math.ceil(min(max(float(value), -1), 10))
    role_model = await PropList.get(user_qq=user_qq, uid=uid, role_name=role_name)
    role_model.dmg_info = role.dmg_list
    role_model.buff_info = role.buff_list
    await role_model.save()
