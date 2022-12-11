from Nahidabot.utils.classmodel import (
    Buff,
    BuffInfo,
    BuffSetting,
    PoFValue,
    PropInfo,
    Weapon,
)

from ..dmg_model import DMGCalc, reserve_setting


async def polearm(buff_list: list[BuffInfo], talent: PropInfo, prop: DMGCalc):
    # ============================
    # ************五星*************
    # ============================

    # ============================
    # ************四星*************
    # ============================
    for buff_info in buff_list:
        setting = buff_info.setting

        if buff_info.name == "决斗之枪-角斗士":
            if setting.label in ["0", "1"]:
                setting.state = "最多1"
                buff_info.buff = Buff(
                    dsc="身边敌人<=1, 攻击+24%",
                    atk=PoFValue(percent=0.24),
                )
            else:
                setting.state = "至少2"
                buff_info.buff = Buff(
                    dsc="身边敌人>=2, 攻击+16%，防御+16%",
                    atk=PoFValue(percent=0.16),
                    defend=PoFValue(percent=0.16),
                )

    # ============================
    # ************三星*************
    # ============================

    return buff_list


async def polearm_setting(weapon: Weapon, buff_list: list[BuffInfo], name: str):
    output: list[BuffInfo] = []
    labels = reserve_setting(buff_list)

    source = f"{name}-武器"
    # ============================
    # ************五星*************
    # ============================

    # ============================
    # ************四星*************
    # ============================
    if weapon.name == "决斗之枪":
        output.append(
            BuffInfo(
                source=source,
                name="决斗之枪-角斗士",
                buff_type="propbuff",
                setting=BuffSetting(
                    dsc="敌人数量||①最多1：攻击+24%；②至少2：攻击+16%，防御+16%",
                    label=labels.get("决斗之枪-角斗士", "1"),
                ),
            )
        )
    # ============================
    # ************三星*************
    # ============================

    return output
