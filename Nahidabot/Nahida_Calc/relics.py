from typing import Optional

from nonebot.log import logger

from Nahidabot.utils.classmodel import (
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    PoFValue,
    PropInfo,
    Relicset,
)

from .dmg_model import DMGCalc, reserve_setting


async def artifacts(buff_list: list[BuffInfo], talent: PropInfo, prop: DMGCalc):
    """
    提供圣遗物buff
    Args:
        buff_list:
        talent:
        prop:
    """
    for buff_info in buff_list:
        setting = buff_info.setting

        if buff_info.name == "战狂4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="角色生命<70%,暴击+24%",
                    crit_rate=0.24,
                )

        if buff_info.name == "行者4":
            buff_info.buff = Buff(
                dsc="重击暴击+30%",
                target="CA",
                crit_rate=0.3,
            )

        if buff_info.name == "勇士4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="敌方生命>50%，增伤+30%",
                    dmg_bonus=0.3,
                )

        if buff_info.name == "教官4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="触发反应8s内，精通+120",
                    elem_mastery=120,
                )

        if buff_info.name == "赌徒2":
            buff_info.buff = Buff(
                dsc="元素战技增伤+30%",
                target="E",
                dmg_bonus=0.3,
            )

        if buff_info.name == "武人2":
            buff_info.buff = Buff(
                dsc="普攻与重击增伤+15%",
                target=["NA", "CA"],
                dmg_bonus=0.15,
            )

        if buff_info.name == "武人4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="施放元素战技8秒内，普攻与重击增伤+25%",
                    target=["NA", "CA"],
                    dmg_bonus=0.25,
                )

        if buff_info.name == "冰风4":
            if setting.label == "0":
                setting.state = "×"
            elif setting.label in ["1", "冰附着"]:
                setting.state = "冰附着"
                buff_info.buff = Buff(
                    dsc="敌人冰附着，暴击+20%",
                    crit_rate=0.2,
                )
            else:
                setting.state = "冻结"
                buff_info.buff = Buff(
                    dsc="敌人冻结，暴击+40%",
                    crit_rate=0.4,
                )

        if buff_info.name == "平雷4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="敌人雷附着，增伤+35%",
                    dmg_bonus=0.35,
                )

        if buff_info.name == "渡火4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="敌人火附着，增伤+35%",
                    dmg_bonus=0.35,
                )

        if buff_info.name == "少女4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    target="H",
                    dsc="施放元素战技或元素爆发10秒内，全队受治疗+20%",
                    healing=0.2,
                )

        if buff_info.name == "角斗4":
            if talent.weapon_type in ["单手剑", "长柄", "双手剑"]:
                buff_info.buff = Buff(
                    dsc="单手剑，长柄，双手剑角色，普攻增伤+35%",
                    target="NA",
                    dmg_bonus=0.35,
                )

        if buff_info.name == "翠绿4-1":
            buff_info.buff = Buff(
                dsc="扩散反应系数+60%",
                elem_type=["pyro", "electro", "hydro", "cryo"],
                reaction_type="扩散",
                reaction_coeff=0.6,
            )

        if buff_info.name == "翠绿4-2":
            buff_info.buff = Buff(
                elem_type=[],
                dsc="触发扩散10s内，对应元素抗性-40%",
                resist_reduction=0.4,
            )
            if (a in setting.label for a in ["火", "1"]):
                setting.state += "火"
                buff_info.buff.elem_type.append("pyro")  # type: ignore
            if (a in setting.label for a in ["水", "2"]):
                setting.state += "水"
                buff_info.buff.elem_type.append("hydro")  # type: ignore
            if (a in setting.label for a in ["雷", "3"]):
                setting.state += "雷"
                buff_info.buff.elem_type.append("electro")  # type: ignore
            if (a in setting.label for a in ["冰", "4"]):
                setting.state += "冰"
                buff_info.buff.elem_type.append("cryo")  # type: ignore
            if setting.state == "":
                setting.state = "无"

        if buff_info.name == "流浪大地的乐团":
            if talent.weapon_type in ["弓", "法器"]:
                buff_info.buff = Buff(
                    dsc="弓，法器角色，重击增伤+35%",
                    target="CA",
                    dmg_bonus=0.35,
                )

        if buff_info.name == "如雷4-1":
            buff_info.buff = Buff(
                dsc="超载、感电、超导、超绽放反应系数+40%",
                elem_type=["pyro", "electro", "cryo", "dendro"],
                reaction_type=["超载", "感电", "超导", "超绽放"],
                reaction_coeff=0.4,
            )

        if buff_info.name == "如雷4-2":
            buff_info.buff = Buff(
                dsc="超激化反应系数+20%",
                elem_type=["electro"],
                reaction_type=["超激化"],
                reaction_coeff=0.2,
            )

        if buff_info.name == "魔女4-1":
            buff_info.buff = Buff(
                dsc="超载、燃烧、烈绽放反应系数+40%",
                elem_type=["pyro", "dendro"],
                reaction_type=["超载", "燃烧", "烈绽放"],
                reaction_coeff=0.4,
            )

        if buff_info.name == "魔女4-2":
            buff_info.buff = Buff(
                dsc="蒸发、融化反应系数+15%",
                elem_type=["pyro", "hydro", "cryo"],
                reaction_type=["火蒸发", "冰融化", "水蒸发", "火融化"],
                reaction_coeff=0.15,
            )

        if buff_info.name == "魔女4-3":
            if setting.label == "0":
                setting.state = "×"
            elif setting.label == "1":
                setting.state = "1层"
                buff_info.buff = Buff(
                    elem_type="pyro",
                    dsc="施放元素战技10秒内，火伤+7.5%",
                    elem_dmg_bonus=DMGBonus(pyro=0.075),
                )
            elif setting.label == "2":
                setting.state = "2层"
                buff_info.buff = Buff(
                    elem_type="pyro",
                    dsc="施放元素战技10秒内，火伤+15%",
                    elem_dmg_bonus=DMGBonus(pyro=0.15),
                )
            else:
                setting.state = "3层"
                buff_info.buff = Buff(
                    elem_type="pyro",
                    dsc="施放元素战技10秒内，火伤+22.5%",
                    elem_dmg_bonus=DMGBonus(pyro=0.225),
                )

        if buff_info.name == "宗室2":
            buff_info.buff = Buff(
                target="Q",
                dsc="元素爆发增伤+20％",
                dmg_bonus=0.2,
            )

        if buff_info.name == "宗室4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc=f"施放元素爆发12秒内，全队攻击+20% => {prop.atk_base * 0.2}",
                    triger_type="active",
                    atk=PoFValue(percent=0.2),
                )

    return buff_list


async def artifacts_setting(
    relics: Optional[Relicset],
    buff_list: list[BuffInfo],
    name: str = "",
):
    """"""
    if relics is None:
        return []
    output: list[BuffInfo] = []
    labels = reserve_setting(buff_list)

    for name, num in relics.set_info.items():
        source = f"{name}-圣遗物"

        if name == "战狂":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="战狂4",
                        setting=BuffSetting(
                            dsc="角色生命||⓪高于70%（×）：无增益；①低于70（✓）：暴击+24%",
                            label=labels.get("战狂4", "1"),
                        ),
                    )
                )

        if name == "行者之心":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="行者4",
                    )
                )

        if name == "勇士之心":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="勇士4",
                        setting=BuffSetting(
                            dsc="敌方生命||⓪低于50%（×）：无增益；①高于50（✓）：增伤+30%",
                            label=labels.get("勇士4", "1"),
                        ),
                    )
                )

        if name == "教官":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="教官4",
                        range="all",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="元素反应||⓪未触发（×）：无增益；①触发（✓）：全队精通+120",
                            label=labels.get("教官4", "1"),
                        ),
                    )
                )

        if name == "赌徒":
            if num >= 2:
                output.append(
                    BuffInfo(
                        source=source,
                        name="赌徒2",
                    )
                )

        if name == "武人":
            if num >= 2:
                output.append(
                    BuffInfo(
                        source=source,
                        name="武人2",
                    )
                )

            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="武人4",
                        setting=BuffSetting(
                            dsc="元素战技||⓪未施放（×）：无增益；①施放（✓）：普攻与重击增伤+25%",
                            label=labels.get("武人4", "1"),
                        ),
                    )
                )

        if name == "冰风迷途的勇士":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="冰风4",
                        setting=BuffSetting(
                            dsc="敌方状态||⓪其余（×）：无增益；①冰附着：暴击+20%；②冻结：暴击+40%",
                            label=labels.get("冰风4", "2"),
                        ),
                    )
                )

        if name == "平息鸣雷的尊者":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="平雷4",
                        setting=BuffSetting(
                            dsc="敌方状态||⓪其余（×）：无增益；①雷附着（✓）：增伤+35%",
                            label=labels.get("平雷4", "1"),
                        ),
                    )
                )

        if name == "渡过烈火的贤人":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="渡火4",
                        setting=BuffSetting(
                            dsc="敌方状态||⓪其余（×）：无增益；①火附着（✓）：增伤+35%",
                            label=labels.get("渡火4", "1"),
                        ),
                    )
                )

        if name == "被怜爱的少女":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="少女4",
                        setting=BuffSetting(
                            dsc="元素战技或元素爆发||⓪未施放（×）：无增益；①施放（✓）：全队受治疗+20%",
                            label=labels.get("少女4", "1"),
                        ),
                    )
                )

        if name == "角斗士的终幕礼":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="角斗4",
                    )
                )

        if name == "翠绿之影":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="翠绿4-1",
                    )
                )
                output.append(
                    BuffInfo(
                        source=source,
                        name="翠绿4-2",
                        range="all",
                        setting=BuffSetting(
                            dsc="触发扩散（可重复）||⓪无：无增益；"
                            + "①火：火抗-40%；②水：水抗-40%；"
                            + "③雷：雷抗-40%；④冰：冰抗-40%；",
                            label=labels.get("翠绿4-2", "火"),
                        ),
                    )
                )

        if name == "流浪大地的乐团":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="乐团4",
                    )
                )

        if name == "如雷的盛怒":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="如雷4-1",
                    )
                )
                output.append(
                    BuffInfo(
                        source=source,
                        name="如雷4-2",
                    )
                )

        if name == "炽烈的炎之魔女":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="魔女4-1",
                    )
                )
                output.append(
                    BuffInfo(
                        source=source,
                        name="魔女4-2",
                    )
                )
                output.append(
                    BuffInfo(
                        source=source,
                        name="魔女4-3",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="施放元素战技叠层||⓪0层：无增益；"
                            + "①1层：火伤+7.5%；②2层：火伤+15%；③3层：火伤+22.5%",
                            label=labels.get("魔女4-3", "3"),
                        ),
                    )
                )

        if name == "昔日宗室之仪":
            if num >= 2:
                output.append(
                    BuffInfo(
                        source=source,
                        name="宗室2",
                    )
                )
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="宗室4",
                        range="all",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="元素爆发||⓪未施放（×）：无增益；①施放（✓）：全队攻击+20%",
                            label=labels.get("宗室4", "1"),
                        ),
                    )
                )

    return output
