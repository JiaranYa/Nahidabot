from nonebot.log import logger

from Nahidabot.utils.classmodel import (
    Buff,
    BuffList,
    BuffSetting,
    DMGBonus,
    PropBuff,
    PropInfo,
    Relicset,
    Role,
)


async def relic_buff(role: Role):
    if role.artifacts is None or role.talent is None or role.buff_list is None:
        logger.opt(colors=True).error("获取圣遗物增益信息不足")
        return []

    buff_info = BuffList()
    for buff in role.buff_list:
        if buff.source == "圣遗物":
            buff_info = buff
    try:

        return await artifacts(role.artifacts, buff_info, role.talent)
    except NameError:
        return []


async def artifacts(relic: Relicset, buff_info: BuffList, talent: PropInfo):
    """
    提供圣遗物buff
    Args:
        relic:
        setting:
        is_setting:
    """

    output = BuffList(source="圣遗物")
    for name, num in relic.set_info.items():

        if name == "战狂":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="战狂4",
                    dsc="角色生命||⓪高于70%（×）：无增益；①低于70（✓）：暴击+24%",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "战狂4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(name="战狂4", dsc="角色生命<70%,暴击+24%", crit_rate=0.24)
                    )
                output.setting.append(setting)

        if name == "行者之心":
            if num >= 4:
                # 生成增益
                output.buff.append(
                    Buff(
                        name="行者4",
                        dsc="重击暴击+30%",
                        value_type="CA",
                        crit_rate=0.3,
                    )
                )

        if name == "勇士之心":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="勇士4",
                    dsc="敌方生命||⓪低于50%（×）：无增益；①高于50（✓）：增伤+30%",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "勇士4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="勇士4",
                            dsc="敌方生命>50%，增伤+30%",
                            dmg_bonus=DMGBonus(all=0.3),
                        )
                    )
                output.setting.append(setting)

        if name == "教官":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="教官4",
                    dsc="元素反应||⓪未触发（×）：无增益；①触发（✓）：全队精通+120",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "教官4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="教官4",
                            dsc="触发反应8s内，精通+120",
                            member_type="all",
                            elem_mastery=120,
                        )
                    )
                output.setting.append(setting)

        if name == "赌徒":
            if num >= 2:
                # 生成增益
                output.buff.append(
                    Buff(
                        name="赌徒2",
                        dsc="元素战技增伤+30%",
                        value_type="E",
                        dmg_bonus=DMGBonus(all=0.3),
                    )
                )

        if name == "武人":
            if num >= 2:
                # 生成增益
                output.buff.append(
                    Buff(
                        name="武人2",
                        dsc="普攻与重击增伤+15%",
                        value_type=["NA", "CA"],
                        dmg_bonus=DMGBonus(all=0.15),
                    )
                )

            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="武人4",
                    dsc="元素战技||⓪未施放（×）：无增益；①施放（✓）：普攻与重击增伤+25%",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "武人4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="武人4",
                            dsc="施放元素战技8秒内，普攻与重击增伤+25%",
                            dmg_bonus=DMGBonus(all=0.25),
                        )
                    )
                output.setting.append(setting)

        if name == "冰风迷途的勇士":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="冰风4",
                    dsc="敌方状态||⓪其余（×）：无增益；①冰附着：暴击+20%；②冻结：暴击+40%",
                    label=2,
                )
                for s in buff_info.setting:
                    if s.name == "冰风4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                if setting.label == 1:
                    setting.state = "冰附着"
                    output.buff.append(
                        Buff(
                            name="冰风4",
                            dsc="敌人冰附着，暴击+20%",
                            crit_rate=0.2,
                        )
                    )
                else:
                    setting.state = "冻结"
                    output.buff.append(
                        Buff(
                            name="冰风4",
                            dsc="敌人冻结，暴击+40%",
                            crit_rate=0.4,
                        )
                    )
                output.setting.append(setting)

        if name == "平息鸣雷的尊者":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="平雷4",
                    dsc="敌方状态||⓪其余（×）：无增益；①雷附着（✓）：增伤+35%",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "平雷4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="平雷4", dsc="敌人雷附着，增伤+35%", dmg_bonus=DMGBonus(all=0.35)
                        )
                    )
                output.setting.append(setting)

        if name == "渡过烈火的贤人":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="渡火4",
                    dsc="敌方状态||⓪其余（×）：无增益；①火附着（✓）：增伤+35%",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "渡火4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="渡火4", dsc="敌人火附着，增伤+35%", dmg_bonus=DMGBonus(all=0.35)
                        )
                    )
                output.setting.append(setting)

        if name == "被怜爱的少女":
            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="少女4",
                    dsc="元素战技或元素爆发||⓪未施放（×）：无增益；①施放（✓）：全队受治疗+20%",
                    label=1,
                )
                for s in buff_info.setting:
                    if s.name == "少女4":
                        setting = s
                # 生成增益
                if setting.label == 0:
                    setting.state = "×"
                else:
                    setting.state = "✓"
                    output.buff.append(
                        Buff(
                            name="少女4",
                            dsc="施放元素战技或元素爆发10秒内，全队受治疗+20%",
                            member_type="all",
                            healing=0.2,
                        )
                    )
                output.setting.append(setting)

        if name == "角斗士的终幕礼":
            if num >= 4:
                # 生成增益
                if talent.weapon_type in ["单手剑", "长柄", "双手剑"]:
                    output.buff.append(
                        Buff(
                            name="角斗4",
                            dsc="单手剑，长柄，双手剑角色，普攻增伤+35%",
                            value_type="NA",
                            dmg_bonus=DMGBonus(all=0.35),
                        )
                    )

        # TODO:翠绿之影
        if name == "翠绿之影":
            pass

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
                            value_type="CA",
                            dmg_bonus=DMGBonus(all=0.35),
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
                        value_type="Q",
                        dsc="元素爆发增伤+20％",
                        dmg_bonus=DMGBonus(all=0.2),
                    )
                )

            if num >= 4:
                # 生成设置
                setting = BuffSetting(
                    name="宗室4",
                    dsc="元素爆发||⓪未施放（×）：无增益；①施放（✓）：全队攻击+20%",
                    label=1,
                )
                for s in buff_info.setting:
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

    return [output]


def artifacts_setting():
    """"""
