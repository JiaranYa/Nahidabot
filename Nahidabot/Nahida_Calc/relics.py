from typing import Optional

from Nahidabot.utils.classmodel import (
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    Multiplier,
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
            if setting.state == "-":
                setting.state = "×"

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
                    dsc=f"施放元素爆发12秒内，全队攻击+20% => +{round(prop.atk_base * 0.2)}",
                    triger_type="active",
                    atk=PoFValue(percent=0.2),
                )

        if buff_info.name == "骑士4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="击败敌方10秒内，重击增伤+50%",
                    target="CA",
                    dmg_bonus=0.5,
                )

        if buff_info.name == "磐岩4":
            if setting.label == "0":
                setting.state = "×"
            else:
                buff_info.buff = Buff(
                    dsc="获得结晶片10s内，对应元素增伤+35%",
                )
                if setting.label in ["火", "1"]:
                    setting.state = "火"
                    buff_info.buff.elem_type = "pyro"
                    buff_info.buff.elem_dmg_bonus = DMGBonus(pyro=0.35)
                elif setting.label in ["水", "2"]:
                    setting.state = "水"
                    buff_info.buff.elem_type = "hydro"
                    buff_info.buff.elem_dmg_bonus = DMGBonus(hydro=0.35)
                elif setting.label in ["雷", "3"]:
                    setting.state = "雷"
                    buff_info.buff.elem_type = "electro"
                    buff_info.buff.elem_dmg_bonus = DMGBonus(electro=0.35)
                elif setting.label in ["冰", "4"]:
                    setting.state = "冰"
                    buff_info.buff.elem_type = "cryo"
                    buff_info.buff.elem_dmg_bonus = DMGBonus(cryo=0.35)
                else:
                    setting.state = "×"

        if buff_info.name == "流星4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="护盾庇护下，普攻和重击增伤+40%",
                    target=["NA", "CA"],
                    dmg_bonus=0.4,
                )

        if buff_info.name == "沉沦4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="施放元素战技15秒内，普攻和重击增伤+30%",
                    target=["NA", "CA"],
                    dmg_bonus=0.3,
                )

        if buff_info.name == "千岩4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc=f"元素战技命中3秒内，全队护盾强效+30%且攻击+20% => +{prop.atk_base * 0.2}",
                    atk=PoFValue(percent=0.2),
                )

        if buff_info.name == "苍白4":
            if setting.label == "0":
                setting.state = "×"
            elif setting.label == "1":
                setting.state = "1层"
                buff_info.buff = Buff(
                    dsc=f"元素战技命中7秒内，攻击+9% => +{prop.atk_base * 0.09}",
                    atk=PoFValue(percent=0.09),
                )
            else:
                setting.state = "2层"
                buff_info.buff = Buff(
                    dsc=f"元素战技命中7秒内，物伤+25%，攻击+18% => +{prop.atk_base * 0.09}",
                    atk=PoFValue(percent=0.09),
                    elem_dmg_bonus=DMGBonus(phy=0.25),
                )

        if buff_info.name == "追忆4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="施放元素战技10秒内，流失15点能量，普攻、重击和下落增伤+50%",
                    target=["NA", "CA", "PA"],
                    dmg_bonus=0.5,
                )

        if buff_info.name == "绝缘4":
            buff_info.buff = Buff(
                dsc=f"基于充能的25%，元素爆发增伤 => +{min(prop.recharge * 25,75)}%，至多75%",
                target=["Q"],
                dmg_bonus=min(prop.recharge * 0.25, 0.75),
            )

        if buff_info.name == "华馆4-问答":
            if setting.label == "0":
                setting.state = "×"
                s = 0
                return
            elif setting.label == "1":
                setting.state = "1层"
                s = 1
            elif setting.label == "2":
                setting.state = "2层"
                s = 2
            elif setting.label == "3":
                setting.state = "3层"
                s = 3
            else:
                setting.state = "4层"
                s = 4

            buff_info.buff = Buff(
                dsc=f"岩元素命中敌方获得一层，{s}层，岩伤+{s*6}%，防御+{s*6}% => {prop.def_base*s*0.06}",
                defend=PoFValue(percent=s * 0.06),
                elem_dmg_bonus=DMGBonus(geo=s * 0.06),
            )

        if buff_info.name == "辰砂4-潜光":
            if setting.label == "0":
                setting.state = "0层"
                s = 0
            elif setting.label == "1":
                setting.state = "1层"
                s = 1
            elif setting.label == "2":
                setting.state = "2层"
                s = 2
            elif setting.label == "3":
                setting.state = "3层"
                s = 3
            else:
                setting.state = "4层"
                s = 4

            buff_info.buff = Buff(
                dsc="施放元素爆发16秒内，攻击+8%，生命降低时叠层，"
                + f"{s}层额外攻击+{s*10}% => 共+{prop.atk_base * (0.08+s*0.1)}",
                atk=PoFValue(percent=(0.08 + s * 0.1)),
            )

        if buff_info.name == "青玉4-幽谷祝祀":
            buff_info.buff = Buff(
                dsc="普攻倍率期望+35.14%", target=["NA"], mutiplier=Multiplier(atk=0.3514)
            )

        if buff_info.name == "深林4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="元素战技或元素爆发命中8秒内，草抗-30%",
                    elem_type="dendro",
                    resist_reduction=0.3,
                )

        if buff_info.name == "饰金4":
            if setting.label == "4":
                setting.state = "×"
                return
            elif setting.label == "0":
                setting.state = "0名异色"
                s = 0
            elif setting.label == "1":
                setting.state = "1名异色"
                s = 1
            elif setting.label == "2":
                setting.state = "2名异色"
                s = 2
            else:
                setting.state = "3名异色"
                s = 3
            buff_info.buff = Buff(
                dsc=f"触发元素反应8秒内，元素精通+{s*50}，攻击力+{(3-s)*14}% => {prop.atk_base*(3 - s) * 0.14}",
                atk=PoFValue(percent=(3 - s) * 0.14),
                elem_mastery=s * 50,
            )

        if buff_info.name == "沙阁4":
            if setting.label == "0":
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="重击命中15秒内，攻速+10%，普攻、重击与下落增伤+40%",
                    target=["NA", "CA", "PA"],
                    dmg_bonus=0.4,
                )

        if buff_info.name == "花神4":
            if setting.label == "0":
                setting.state = "0层"
                s = 0
            elif setting.label == "1":
                setting.state = "1层"
                s = 1
            elif setting.label == "2":
                setting.state = "2层"
                s = 2
            elif setting.label == "3":
                setting.state = "3层"
                s = 3
            else:
                setting.state = "4层"
                s = 4

            buff_info.buff = Buff(
                dsc=f"绽放系列反应系数+40%，触发反应叠层，{s}层额外反应系数+{s*10}%",
                elem_type="dendro",
                reaction_type=["原绽放", "烈绽放", "超绽放"],
                reaction_coeff=0.4 + s * 0.1,
            )

    return buff_list


async def artifacts_setting(
    relics: Optional[Relicset],
    buff_list: list[BuffInfo],
    role_name: str = "",
):
    """"""
    if relics is None:
        return []
    output: list[BuffInfo] = []
    labels = reserve_setting(buff_list)

    for name, num in relics.set_info.items():
        source = f"{role_name}-圣遗物"

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
                        buff_range="all",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="触发元素反应||⓪关（×）：无增益；①开（✓）：全队精通+120",
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
                            dsc="施放元素战技||⓪关（×）：无增益；①开（✓）：普攻与重击增伤+25%",
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
                            dsc="施放元素战技或元素爆发||⓪关（×）：无增益；①开（✓）：全队受治疗+20%",
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
                        buff_range="all",
                        setting=BuffSetting(
                            dsc="触发扩散（可重复）||⓪无（×）：无增益；"
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
                        buff_range="all",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="施放元素爆发||⓪关（×）：无增益；①开（✓）：全队攻击+20%",
                            label=labels.get("宗室4", "1"),
                        ),
                    )
                )

        if name == "染血的骑士道":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="骑士4",
                        setting=BuffSetting(
                            dsc="击杀敌方||⓪关（×）：无增益；①开（✓）：重击增伤+50%",
                            label=labels.get("骑士4", "1"),
                        ),
                    )
                )

        if name == "悠古的磐岩":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="磐岩4",
                        buff_range="all",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="获取结晶片||⓪无（×）：无增益；"
                            + "①火：火伤+35%；②水：水伤+35%；"
                            + "③雷：雷伤+35%；④冰：冰伤+35%；",
                            label=labels.get("磐岩4", "火"),
                        ),
                    )
                )

        if name == "逆飞的流星":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="流星4",
                        setting=BuffSetting(
                            dsc="护盾存在||⓪关（×）：无增益；①开（✓）：普攻和重击增伤+40%",
                            label=labels.get("流星4", "1"),
                        ),
                    )
                )

        if name == "沉沦之心":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="沉沦4",
                        setting=BuffSetting(
                            dsc="施放元素战技||⓪关（×）：无增益；①开（✓）：普攻和重击增伤+30%",
                            label=labels.get("沉沦4", "1"),
                        ),
                    )
                )

        if name == "千岩牢固":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="千岩4",
                        buff_range="all",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="元素战技命中||⓪关（×）：无增益；①开（✓）：全队攻击+20%",
                            label=labels.get("千岩4", "1"),
                        ),
                    )
                )

        if name == "苍白之火":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="苍白4",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="元素战技命中叠层||⓪0层：无增益；①1层：攻击+9%；②2层：攻击+18%，物伤+25%",
                            label=labels.get("苍白4", "2"),
                        ),
                    )
                )

        if name == "追忆之注连":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="追忆4",
                        setting=BuffSetting(
                            dsc="施放元素战技||⓪关（×）：无增益；①开（✓）：普攻、重击和下落增伤+50%",
                            label=labels.get("追忆4", "1"),
                        ),
                    )
                )

        if name == "绝缘之旗印":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="绝缘4",
                    )
                )

        if name == "华馆梦醒形骸记":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="华馆4-问答",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="岩元素攻击命中||⓪0层：无增益；①1层：防御+6%，岩伤+6%；②2层：防御+12%，岩伤+12%"
                            + "③3层：防御+18%，岩伤+18%；④4层：防御+24%，岩伤+24%",
                            label=labels.get("华馆4-问答", "4"),
                        ),
                    )
                )

        if name == "辰砂往生录":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="辰砂4-潜光",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="施放元素爆发，降低生命叠层||⓪0层：攻击+8%；"
                            + "①1层：攻击+18%；②2层：攻击+28%；"
                            + "③3层：攻击+38%；④4层：攻击+48%",
                            label=labels.get("辰砂4-潜光", "3"),
                        ),
                    )
                )

        if name == "来歆余响":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="青玉4-幽谷祝祀",
                    )
                )

        if name == "深林的记忆":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="深林4",
                        buff_range="all",
                        setting=BuffSetting(
                            dsc="元素战技或元素爆发命中||⓪关（×）：无增益；①开（✓）：草抗-30%",
                            label=labels.get("深林4", "1"),
                        ),
                    )
                )

        if name == "饰金之梦":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="饰金4",
                        buff_type="propbuff",
                        setting=BuffSetting(
                            dsc="触发元素反应，其他角色的元素类型||⓪0名异色：攻击+42%；①1名异色：精通+50，攻击+28%"
                            + "②2名异色：精通+100，攻击+14%；③3名异色：精通+150；④关（×）：无增益",
                            label=labels.get("饰金4", "3"),
                        ),
                    )
                )

        if name == "沙上楼阁史话":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="沙阁4",
                        setting=BuffSetting(
                            dsc="重击命中||⓪关（×）：无增益；①开（✓）：普攻、重击与下落增伤+40%",
                            label=labels.get("沙阁4", "1"),
                        ),
                    )
                )

        if name == "乐园遗落之花":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="花神4",
                        setting=BuffSetting(
                            dsc="触发绽放、超绽放、烈绽放叠层||||⓪0层：绽放系列反应系数+40%；①1层：绽放系列反应系数+50%"
                            + "②2层：绽放系列反应系数+60%；③3层：绽放系列反应系数+70%；④4层：绽放系列反应系数+80%",
                            label=labels.get("花神4", "4"),
                        ),
                    )
                )

    return output
