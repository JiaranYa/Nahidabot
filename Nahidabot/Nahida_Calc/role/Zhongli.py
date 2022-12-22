from nonebot.utils import run_sync

from Nahidabot.utils.classmodel import (
    DMG,
    Buff,
    BuffInfo,
    BuffSetting,
    FixValue,
    Multiplier,
)

from ..dmg_model import reserve_setting, reserve_weight
from ..role_model import RoleModel


class Ganyu(RoleModel):
    name = "钟离"

    def T1(self, buff_info: BuffInfo):
        """悬岩宸断"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        elif setting.label == "1":
            setting.state = "1层"
            buff_info.buff = Buff(
                dsc="护盾强效+5%",
                shield_strength=0.05,
            )
        elif setting.label == "2":
            setting.state = "2层"
            buff_info.buff = Buff(
                dsc="护盾强效+10%",
                shield_strength=0.1,
            )
        elif setting.label == "3":
            setting.state = "3层"
            buff_info.buff = Buff(
                dsc="护盾强效+15%",
                shield_strength=0.15,
            )
        elif setting.label == "4":
            setting.state = "4层"
            buff_info.buff = Buff(
                dsc="护盾强效+20%",
                shield_strength=0.2,
            )
        else:
            setting.state = "5层"
            buff_info.buff = Buff(
                dsc="护盾强效+25%",
                shield_strength=0.25,
            )

    T2_to_A = 0.0
    """普攻、重击与下落固伤"""
    T2_to_Q = 0.0
    """天星伤害固伤"""

    def T2(self, buff_info: BuffInfo):
        """炊金馔玉"""
        self.T2_to_A = self.calculator.hp * 0.0139
        self.T2_to_Q = self.calculator.hp * 0.33
        buff_info.buff = Buff(
            dsc=f"普攻、重击与下落额外固伤 => {self.T2_to_A}；天星额外固伤 => {self.T2_to_Q}",
        )

    def skill_A(self, dmg_info: DMG):
        """岩雨"""
        calc = self.calculator
        calc.set(
            value_type="Q",
            elem_type="phy",
            multiplier=Multiplier(
                atk=self.scaling_table[3].multiplier[self.info.skill_A - 1]
            ),
            fix_value=FixValue(dmg=self.T2_to_A),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_dmg("exp"))
        dmg_info.crit_value = int(calc.get_dmg("crit"))

    def skill_E(self, dmg_info: DMG):
        """地心·玉璋护盾"""
        calc = self.calculator
        calc.set(
            value_type="S",
            multiplier=Multiplier(
                hp=self.scaling_table[1].multiplier[self.info.skill_E - 1]
            ),
            fix_value=FixValue(
                shield=self.scaling_table[0].multiplier[self.info.skill_E - 1]
            ),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_dmg("exp"))
        dmg_info.crit_value = int(calc.get_dmg("crit"))

    def skill_Q(self, dmg_info: DMG):
        """天星"""
        calc = self.calculator
        calc.set(
            value_type="Q",
            elem_type="geo",
            multiplier=Multiplier(
                atk=self.scaling_table[2].multiplier[self.info.skill_Q - 1]
            ),
            fix_value=FixValue(dmg=self.T2_to_Q),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_dmg("exp"))
        dmg_info.crit_value = int(calc.get_dmg("crit"))

    @property
    def valid_prop(self) -> list[str]:
        """有效属性"""
        return []

    @run_sync
    def setting(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益设置"""
        output: list[BuffInfo] = []
        labels = reserve_setting(buff_list)

        if self.info.ascension >= 2:
            output.append(
                BuffInfo(
                    source=f"{self.name}-T1",
                    name="悬岩宸断",
                    setting=BuffSetting(
                        dsc="玉璋护盾受到伤害||⓪（×）：无增益；①~⑤每层：护盾强效+5%",
                        label=labels.get("悬岩宸断", "2"),
                    ),
                )
            )
            if self.info.ascension >= 4:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-T2",
                        name="炊金馔玉",
                    )
                )
        return output

    @run_sync
    def buff(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益列表"""
        for buff in buff_list:
            if buff.name == "悬岩宸断":
                self.T1(buff)
            if buff.name == "炊金馔玉":
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
                source="E",
                name="地心·玉璋护盾",
                type="S",
                dsc="E盾量",
                weight=weights.get("地心·玉璋护盾", 10),
            )
        )
        output.append(
            DMG(
                index=2,
                source="Q",
                name="天星",
                dsc="E盾量",
                weight=weights.get("天星", 2),
            )
        )
        output.append(
            DMG(
                index=2,
                source="A",
                name="岩雨",
                dsc="普攻一轮五段",
                weight=weights.get("岩雨", 10),
            )
        )

        return output

    @run_sync
    def dmg(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害列表"""
        for dmg in dmg_list:
            if dmg.name == "地心·玉璋护盾" and dmg.weight != 0:
                self.skill_E(dmg)
            if dmg.name == "天星" and dmg.weight != 0:
                self.skill_Q(dmg)
            if dmg.name == "岩雨" and dmg.weight != 0:
                self.skill_A(dmg)
        return dmg_list
