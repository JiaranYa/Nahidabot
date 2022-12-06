from nonebot.log import logger

from .Shougun import *


async def role_dmg(role: Role) -> list[DmgInfo]:
    if role.fight_prop is None or role.talent is None or role.scaling_table is None:
        logger.opt(colors=True).error("获取角色增益信息不足")
        return []

    try:
        return await eval(f"{role.talent.abbr}")(
            role.talent, role.fight_prop, role.scaling_table, role.buff_list
        )
    except NameError:
        return []


async def role_buff(role: Role) -> list[BuffList]:
    if role.fight_prop is None or role.talent is None or role.scaling_table is None:
        logger.opt(colors=True).error("获取角色增益信息不足")
        return []
    if not role.buff_list:
        role.buff_list = await role_setting(role)

    try:
        return await eval(f"{role.talent.abbr}_buff")(
            role.talent, role.scaling_table, role.buff_list
        )
    except NameError:
        return []


async def role_setting(role: Role) -> list[BuffList]:
    if role.talent is None or role.scaling_table is None:
        logger.opt(colors=True).error("获取角色增益信息不足")
        return []

    try:
        return await eval(f"{role.talent.abbr}_setting")(
            role.talent, role.scaling_table, role.buff_list
        )
    except NameError:
        return []
