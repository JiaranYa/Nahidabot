from Nahidabot.utils.classmodel import Buff, BuffList, BuffSetting, PropInfo, Weapon


async def polearm(talent: PropInfo, weapon: Weapon, buff_info: BuffList):
    output = BuffList(source="武器")

    if weapon.name == "决斗之枪":
        # 生成设置
        setting = BuffSetting(
            name="决斗之枪-角斗士",
            dsc="敌人数量||①最多1：攻击+24%；②至少2：攻击+16%，防御+16%",
            label=1,
        )
        for s in buff_info.setting:
            if s.name == "决斗之枪-角斗士":
                setting = s
        # 生成增益
        if setting.label <= 1:
            setting.state = "最多1"
            output.buff.append(
                Buff(
                    name="决斗之枪-角斗士",
                    dsc="身边敌人>=2, 攻击+16%，防御+16%",
                )
            )
        else:
            setting.state = "至少2"
            output.buff.append(Buff())
        output.setting.append(setting)

    return [output]
