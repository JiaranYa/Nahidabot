from typing import Optional

from nonebot.log import logger

from Nahidabot.utils.classmodel import BuffInfo, PropInfo, Weapon

from ..dmg_model import DMGCalc
from .bow import Bow, Bow_setting
from .cata import Catalyst, Catalyst_setting
from .claym import Claymore, Claymore_setting
from .pole import Polearm, Polearm_setting
from .sword import Sword, Sword_setting


async def weapon_buff(buff_list: list[BuffInfo], talent: PropInfo, prop: DMGCalc):
    if talent is None:
        logger.opt(colors=True).error("获取武器增益信息不足")
        return []

    buff_info = []
    for buff in buff_list:
        if buff.source == "武器":
            buff_info.append(buff)

    if talent.weapon_type == "单手剑":
        return await Sword(buff_list=buff_info, talent=talent, prop=prop)
    elif talent.weapon_type == "弓":
        return await Bow(buff_list=buff_info, talent=talent, prop=prop)
    elif talent.weapon_type == "长柄":
        return await Polearm(buff_list=buff_info, talent=talent, prop=prop)
    elif talent.weapon_type == "双手剑":
        return await Claymore(buff_list=buff_info, talent=talent, prop=prop)
    elif talent.weapon_type == "法器":
        return await Catalyst(buff_list=buff_info, talent=talent, prop=prop)

    return []


async def weapon_setting(
    weapon: Weapon,
    talent: PropInfo,
    buff_list: list[BuffInfo],
    name: str = "",
):
    """"""

    if talent.weapon_type == "单手剑":
        return await Sword_setting(weapon=weapon, buff_list=buff_list, name=name)
    elif talent.weapon_type == "弓":
        return await Bow_setting(weapon=weapon, buff_list=buff_list, name=name)
    elif talent.weapon_type == "长柄":
        return await Polearm_setting(weapon=weapon, buff_list=buff_list, name=name)
    elif talent.weapon_type == "双手剑":
        return await Claymore_setting(weapon=weapon, buff_list=buff_list, name=name)
    elif talent.weapon_type == "法器":
        return await Catalyst_setting(weapon=weapon, buff_list=buff_list, name=name)

    return []
