from nonebot.utils import run_sync

from Nahidabot.utils.classmodel import DMG, Buff, BuffInfo, BuffSetting, Multiplier

from ..dmg_model import reserve_setting, reserve_weight
from ..role_model import RoleModel


class Xingqiu(RoleModel):
    name = "行秋"

    def C2(self, buff_info: BuffInfo):
        """天青现虹"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            buff_info.buff = Buff(
                dsc="剑雨攻击的敌人，水抗-15％，持续4秒",
                elem_type="hydro",
                resist_reduction=0.15,
            )

    C4_to_E = 1.0
    """E技能倍率加成（命座4）"""

    def C4(self, buff_info: BuffInfo):
        """孤舟斩蛟"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
            self.C4_to_E = 1.0
        else:
            setting.state = "✓"
            buff_info.buff = Buff(dsc="古华剑·裁雨留虹持续期间，古华剑·画雨笼山倍率×1.5")
            self.C4_to_E = 1.5

    def skill_E(self, dmg_info: DMG):
        """古华剑·画雨笼山"""
        calc = self.calculator
        calc.set(
            value_type="E",
            elem_type="hydro",
            multiplier=Multiplier(
                atk=self.scaling_table[0].multiplier[self.info.skill_E - 1]
                * self.C4_to_E
            ),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_dmg("exp"))
        dmg_info.crit_value = int(calc.get_dmg("crit"))

    def skill_Q(self, dmg_info: DMG):
        """古华剑·裁雨留虹"""
        calc = self.calculator
        calc.set(
            value_type="Q",
            elem_type="hydro",
            member_type="off",
            multiplier=Multiplier(
                atk=self.scaling_table[1].multiplier[self.info.skill_Q - 1]
            ),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_dmg("exp"))
        dmg_info.crit_value = int(calc.get_dmg("crit"))

    @property
    def valid_prop(self):
        return ["atk", "atk_per", "hydro", "crit", "crit_hurt"]

    @run_sync
    def setting(self, buff_list: list[BuffInfo]):
        """增益设置"""
        output: list[BuffInfo] = []
        labels = reserve_setting(buff_list)

        if self.info.constellation >= 2:
            output.append(
                BuffInfo(
                    source=f"{self.name}-C2",
                    name="天青现虹",
                    buff_range="all",
                    setting=BuffSetting(
                        dsc="敌人受到剑雨攻击4s内||⓪（×）：无增益；①（✓）：水抗-15%",
                        label=labels.get("天青现虹", "1"),
                    ),
                )
            )
            if self.info.constellation >= 4:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-C4",
                        name="孤舟斩蛟",
                        setting=BuffSetting(
                            dsc="古华剑·裁雨留虹持续期间||⓪（×）：无增益；①（✓）：古华剑·画雨笼山倍率×1.5",
                            label=labels.get("孤舟斩蛟", "1"),
                        ),
                    )
                )
        return output

    @run_sync
    def buff(self, buff_list: list[BuffInfo]):
        """增益列表"""
        for buff in buff_list:
            if buff.name == "天青现虹":
                self.C2(buff)
            if buff.name == "孤舟斩蛟":
                self.C4(buff)

        return buff_list

    @run_sync
    def weight(self, dmg_list: list[DMG]):
        """伤害权重"""
        output: list[DMG] = []
        weights = reserve_weight(dmg_list)

        output.append(
            DMG(
                index=0,
                name="充能效率阈值",
                weight=weights.get("充能效率阈值", 180),
            )
        )
        output.append(
            DMG(
                index=1,
                source="E",
                name="古华剑·画雨笼山",
                dsc="E两段",
                weight=weights.get("古华剑·画雨笼山", 5),
            )
        )
        output.append(
            DMG(
                index=2,
                source="Q",
                name="古华剑·裁雨留虹",
                dsc="Q剑雨每根",
                weight=weights.get("古华剑·裁雨留虹", 10),
            )
        )
        return output

    @run_sync
    def dmg(self, dmg_list: list[DMG]):
        """伤害列表"""
        for dmg in dmg_list:
            if dmg.name == "古华剑·画雨笼山" and dmg.weight != 0:
                self.skill_E(dmg)
            if dmg.name == "古华剑·裁雨留虹" and dmg.weight != 0:
                self.skill_Q(dmg)

        return dmg_list
