from nonebot.utils import run_sync

from Nahidabot.utils.classmodel import (
    DMG,
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    Multiplier,
)

from ..dmg_model import reserve_setting, reserve_weight
from ..role_model import RoleModel


class Ganyu(RoleModel):
    name = "甘雨"

    def C1(self, buff_info: BuffInfo):
        """饮露"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            buff_info.buff = Buff(
                dsc="霜华矢命中6秒内，冰抗-15%",
                elem_type="cryo",
                resist_reduction=0.15,
            )

    def C4(self, buff_info: BuffInfo):
        """西狩"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        elif setting.label == "1":
            setting.state = "1层"
            buff_info.buff = Buff(
                dsc="降众天华领域内，对敌增伤+5%",
                dmg_bonus=0.05,
            )
        elif setting.label == "2":
            setting.state = "2层"
            buff_info.buff = Buff(
                dsc="降众天华领域内，对敌增伤+10%",
                dmg_bonus=0.1,
            )
        elif setting.label == "3":
            setting.state = "3层"
            buff_info.buff = Buff(
                dsc="降众天华领域内，对敌增伤+15%",
                dmg_bonus=0.15,
            )
        elif setting.label == "4":
            setting.state = "4层"
            buff_info.buff = Buff(
                dsc="降众天华领域内，对敌增伤+20%",
                dmg_bonus=0.2,
            )
        else:
            setting.state = "5层"
            buff_info.buff = Buff(
                dsc="降众天华领域内，对敌增伤+25%",
                dmg_bonus=0.25,
            )

    def T1(self, buff_info: BuffInfo):
        """唯此一心"""
        buff_info.buff = Buff(
            dsc="霜华矢发射5秒内，霜华矢和霜华绽发暴击+20%",
            target="CA",
            crit_rate=0.2,
        )

    def T2(self, buff_info: BuffInfo):
        """天地交泰"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            buff_info.buff = Buff(
                dsc="降众天华领域内,冰伤+20%",
                elem_type="cryo",
                elem_dmg_bonus=DMGBonus(cryo=0.2),
            )

    melt = False
    """判断是否需要精通"""

    def skill_A(self, dmg_info: DMG, reaction=""):
        """流天射术·霜华矢"""
        calc = self.calculator
        scale = (
            self.scaling_table[0].multiplier[self.info.skill_A - 1]
            + self.scaling_table[1].multiplier[self.info.skill_A - 1]
        )
        if reaction == "冰融化":
            calc.set(
                value_type="CA",
                elem_type="cryo",
                reaction_type="冰融化",
                multiplier=Multiplier(atk=scale),
            )
            calc += self.dmgbuff
            dmg_info.exp_value = int(calc.get_amp_reac_dmg("exp"))
            dmg_info.crit_value = int(calc.get_amp_reac_dmg("crit"))
            self.melt = True
        else:
            calc.set(
                value_type="CA",
                elem_type="cryo",
                multiplier=Multiplier(atk=scale),
            )
            calc += self.dmgbuff
            dmg_info.exp_value = int(calc.get_dmg("exp"))
            dmg_info.crit_value = int(calc.get_dmg("crit"))

    def skill_Q(self, dmg_info: DMG):
        """降众天华"""
        calc = self.calculator
        calc.set(
            value_type="Q",
            elem_type="cryo",
            multiplier=Multiplier(
                atk=self.scaling_table[2].multiplier[self.info.skill_Q - 1]
            ),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_dmg("exp"))
        dmg_info.crit_value = int(calc.get_dmg("crit"))

    @property
    def valid_prop(self) -> list[str]:
        """有效属性"""
        props = ["atk", "atk_per", "cryo", "crit", "crit_hurt"]
        if self.melt:
            props.append("elem_ma")
        return props

    @run_sync
    def setting(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益设置"""
        output: list[BuffInfo] = []
        labels = reserve_setting(buff_list)

        if self.info.constellation >= 1:
            output.append(
                BuffInfo(
                    source=f"{self.name}-C1",
                    name="饮露",
                    buff_range="all",
                    setting=BuffSetting(
                        dsc="二段蓄力命中||⓪（×）：无增益；①（✓）：冰抗-15%",
                        label=labels.get("饮露", "1"),
                    ),
                )
            )
            if self.info.constellation >= 4:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-C4",
                        name="西狩",
                        buff_range="all",
                        setting=BuffSetting(
                            dsc="降众天华领域内||⓪（×）：无增益；①~⑤每层：增伤5%",
                            label=labels.get("西狩", "3"),
                        ),
                    )
                )

        if self.info.ascension >= 2:
            output.append(
                BuffInfo(
                    source=f"{self.name}-T1",
                    name="唯此一心",
                )
            )
            if self.info.ascension >= 4:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-T2",
                        name="天地交泰",
                        buff_range="all",
                        setting=BuffSetting(
                            dsc="降众天华领域内||⓪（×）：无增益；①（✓）：冰伤+20%",
                            label=labels.get("天地交泰", "1"),
                        ),
                    )
                )

        return output

    @run_sync
    def buff(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益列表"""
        for buff in buff_list:
            if buff.name == "饮露":
                self.C1(buff)
            if buff.name == "西狩":
                self.C4(buff)
            if buff.name == "唯此一心":
                self.T1(buff)
            if buff.name == "天地交泰":
                self.T2(buff)
        return buff_list

    @run_sync
    def weight(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害权重"""
        output: list[DMG] = []
        weights = reserve_weight(dmg_list)

        output.append(
            DMG(
                index=0,
                name="充能效率阈值",
                weight=weights.get("充能效率阈值", 120),
            )
        )
        output.append(
            DMG(
                index=1,
                source="A",
                name="流天射术·霜华矢",
                dsc="A二段蓄力两段",
                weight=weights.get("流天射术·霜华矢", 5),
            )
        )
        output.append(
            DMG(
                index=2,
                source="A",
                name="流天射术·霜华矢-融化",
                dsc="A二段蓄力两段",
                weight=weights.get("流天射术·霜华矢-融化", 0),
            )
        )
        output.append(
            DMG(
                index=3,
                source="Q",
                name="降众天华",
                dsc="冰棱每段",
                weight=weights.get("降众天华", 10),
            )
        )
        return output

    @run_sync
    def dmg(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害列表"""
        for dmg in dmg_list:
            if dmg.name == "流天射术·霜华矢" and dmg.weight != 0:
                self.skill_A(dmg)
            if dmg.name == "流天射术·霜华矢-融化" and dmg.weight != 0:
                self.skill_A(dmg, "冰融化")
            if dmg.name == "降众天华" and dmg.weight != 0:
                self.skill_Q(dmg)

        return dmg_list
