from nonebot.log import logger

from Nahidabot.utils.classmodel import (
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    PropBuff,
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
            if setting.label == 0:
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
            if setting.label == 0:
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="敌方生命>50%，增伤+30%",
                    dmg_bonus=0.3,
                )

        if buff_info.name == "教官4":
            if setting.label == 0:
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
            if setting.label == 0:
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="施放元素战技8秒内，普攻与重击增伤+25%",
                    target=["NA", "CA"],
                    dmg_bonus=0.25,
                )

        if buff_info.name == "冰风4":
            if setting.label == 0:
                setting.state = "×"
            elif setting.label == 1:
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
            if setting.label == 0:
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="敌人雷附着，增伤+35%",
                    dmg_bonus=0.35,
                )

        if buff_info.name == "渡火4":
            if setting.label == 0:
                setting.state = "×"
            else:
                setting.state = "✓"
                buff_info.buff = Buff(
                    dsc="敌人火附着，增伤+35%",
                    dmg_bonus=0.35,
                )

        if buff_info.name == "少女4":
            if setting.label == 0:
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
                elem_type=["pyro","electro","hydro","cryo"],
                reaction_type="扩散",
                reaction_coeff=0.6,
            )

        if buff_info.name == "翠绿4-2":
            if 0 in setting.label:
                

        if name == "流浪大地的乐团":
            if num >= 4:
                # 生成增益
                if talent.weapon_type in [
                    "弓",
                    "法器",
                ]:
                    output.buff.append(
                        Buff(
                            name="角斗4",
                            dsc="弓，法器角色，重击增伤+35%",
                            target="CA",
                            elem_dmg_bonus=DMGBonus(all=0.35),
                        )
                    )

        # TODO:如雷的盛怒
        if name == "如雷的盛怒":
            pass

        # TODO:炽烈的炎之魔女
        if name == "炽烈的炎之魔女":
            pass

        if name == "昔日宗室之仪":
            if num >= 2:
                # 生成增益
                output.buff.append(
                    Buff(
                        name="宗室2",
                        target="Q",
                        dsc="元素爆发增伤+20％",
                        elem_dmg_bonus=DMGBonus(all=0.2),
                    )
                )

            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="宗室4",
                    dsc="元素爆发||⓪未施放（×）：无增益；①施放（✓）：全队攻击+20%",
                    label=1,
                )
                for s in buff_list.setting:
                    if s.name == "宗室4":
                        setting = s

                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="宗室4",
                            dsc="施放元素爆发12秒内，全队攻击+20%",
                            basic_prop=PropBuff(atk_percent=0.2),
                        )
                    )
                output.setting.append(setting)

    return buff_list


async def artifacts_setting(relics: Relicset, buff_list: list[BuffInfo]):
    """"""
    output: list[BuffInfo] = []
    labels = reserve_setting(buff_list)

    for i, (name, num) in enumerate(relics.set_info.items()):
        source = f"圣遗物#{i+1}"
        source2 = f"圣遗物#{i+2}"

        if name == "战狂":
            if num >= 4:
                output.append(
                    BuffInfo(
                        source=source,
                        name="战狂4",
                        setting=BuffSetting(
                            dsc="角色生命||⓪高于70%（×）：无增益；①低于70（✓）：暴击+24%",
                            label=labels.get("战狂4", 1),
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
                            label=labels.get("勇士4", 1),
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
                            label=labels.get("教官4", 1),
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
                        source=source2,
                        name="武人4",
                        setting=BuffSetting(
                            dsc="元素战技||⓪未施放（×）：无增益；①施放（✓）：普攻与重击增伤+25%",
                            label=labels.get("武人4", 1),
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
                            label=labels.get("冰风4", 2),
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
                            label=labels.get("平雷4", 1),
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
                            label=labels.get("渡火4", 1),
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
                            label=labels.get("少女4", 1),
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
                        setting=BuffSetting(
                            dsc="",
                            label=labels.get("翠绿4-2", 1),
                        ),
                    )
                )

    return output
