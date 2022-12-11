from typing import Optional

from nonebot.log import logger

from Nahidabot.utils.classmodel import PropInfo, Weapon, BuffInfo

from ..dmg_model import DMGCalc
from .pole import polearm, polearm_setting


async def weapon_buff(buff_list: list[BuffInfo], talent: PropInfo, prop: DMGCalc):
    if talent is None:
        logger.opt(colors=True).error("获取武器增益信息不足")
        return []

    buff_info = []
    for buff in buff_list:
        if buff.source == "武器":
            buff_info.append(buff)

    if talent.weapon_type == "长柄":
        return await polearm(buff_list=buff_info, talent=talent, prop=prop)

    return []


async def weapon_setting(
    weapon: Optional[Weapon],
    talent: PropInfo,
    buff_list: list[BuffInfo],
    name: str = "",
):
    """"""
    if talent.weapon_type == "单手剑":
        return []
    elif talent.weapon_type == "弓":
        return []
    elif talent.weapon_type == "长柄":
        return await polearm_setting(weapon=weapon, buff_list=buff_list, name=name)
    elif talent.weapon_type == "双手剑":
        return []
    elif talent.weapon_type == "法器":
        return []
    else:
        return []
