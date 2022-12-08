from nonebot.log import logger

from Nahidabot.utils.classmodel import Role

from .pole import *


async def weapon_buff(role: Role):
    if (role.weapon is None) or (role.talent is None):
        logger.opt(colors=True).error("获取武器增益信息不足")
        return []

    buff_info = BuffInfo()
    for buff in role.buff_list:
        if buff.source == "武器":
            buff_info = buff

    if role.talent.weapon_type == "长柄":
        return await polearm(role.talent, role.weapon, buff_info)

    return []
