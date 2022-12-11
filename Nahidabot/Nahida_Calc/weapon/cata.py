from Nahidabot.utils.classmodel import (
    Buff,
    BuffInfo,
    BuffSetting,
    PoFValue,
    PropInfo,
    Weapon,
)

from ..dmg_model import DMGCalc, reserve_setting


async def Catalyst(buff_list: list[BuffInfo], talent: PropInfo, prop: DMGCalc):
    # ============================
    # ************五星*************
    # ============================

    # ============================
    # ************四星*************
    # ============================

    # ============================
    # ************三星*************
    # ============================

    return buff_list


async def Catalyst_setting(weapon: Weapon, buff_list: list[BuffInfo], name: str):
    output: list[BuffInfo] = []
    labels = reserve_setting(buff_list)

    source = f"{name}-武器"
    # ============================
    # ************五星*************
    # ============================

    # ============================
    # ************四星*************
    # ============================

    # ============================
    # ************三星*************
    # ============================

    return output
