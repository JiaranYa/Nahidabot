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


class Yae(RoleModel):
    name = "神子"

    E_rank = 0
    """杀生樱初始位阶"""

    def C2(self, buff_info: BuffInfo):
        """望月吼哕声"""
        buff_info.buff = Buff(
            dsc="杀生樱初始位阶提升至贰阶",
        )
        self.E_rank = 1

    def C4(self, buff_info: BuffInfo):
        """绯樱引雷章"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            buff_info.buff = Buff(
                dsc="杀生樱命中5秒内,全队雷伤+20%",
                elem_type="electro",
                elem_dmg_bonus=DMGBonus(electro=0.2),
            )

    C6_to_E = 0.0
    """C6无视防御"""

    def C6(self, buff_info: BuffInfo):
        """大杀生咒禁"""
        buff_info.buff = Buff(
            dsc="杀生樱无视防御+60%",
        )
        self.C6_to_E = 0.6

    T2_to_E = 0.0
    """T2杀生樱增伤"""

    def T2(self, buff_info: BuffInfo):
        """启蛰之祝词"""
        self.T2_to_E = self.calculator.elem_mastery * 0.15 / 100
        buff_info.buff = Buff(
            dsc=f"每点元素精通，杀生樱增伤+0.15% => +{self.T2_to_E*100}%",
        )

    def skill_E(self, dmg_info: DMG, reaction=""):
        """野干役咒·杀生樱"""
        calc = self.calculator
        scale = self.scaling_table[0 + self.E_rank].multiplier[self.info.skill_E - 1]
        if reaction == "超激化":
            calc.set(
                value_type="E",
                elem_type="electro",
                reaction_type="超激化",
                multiplier=Multiplier(atk=scale),
            )
            calc.def_piercing = self.C6_to_E
            calc += self.dmgbuff
            dmg_info.exp_value = int(calc.get_amp_reac_dmg("exp"))
            dmg_info.crit_value = int(calc.get_amp_reac_dmg("crit"))
        else:
            calc.set(
                value_type="E",
                elem_type="electro",
                multiplier=Multiplier(atk=scale),
            )
            calc.def_piercing = self.C6_to_E
            calc += self.dmgbuff
            dmg_info.exp_value = int(calc.get_dmg("exp"))
            dmg_info.crit_value = int(calc.get_dmg("crit"))

    def skill_Q(self, dmg_info: DMG, reaction=""):
        """大密法·天狐显真"""
        calc = self.calculator
        scale = self.scaling_table[2].multiplier[self.info.skill_Q - 1]
        if reaction == "超激化":
            calc.set(
                value_type="Q",
                elem_type="electro",
                reaction_type="超激化",
                multiplier=Multiplier(atk=scale),
            )
            calc += self.dmgbuff
            dmg_info.exp_value = int(calc.get_amp_reac_dmg("exp"))
            dmg_info.crit_value = int(calc.get_amp_reac_dmg("crit"))
        else:
            calc.set(
                value_type="Q",
                elem_type="electro",
                multiplier=Multiplier(atk=scale),
            )
            calc += self.dmgbuff
            dmg_info.exp_value = int(calc.get_dmg("exp"))
            dmg_info.crit_value = int(calc.get_dmg("crit"))

    @property
    def valid_prop(self) -> list[str]:
        """有效属性"""
        return ["atk", "atk_per", "electro", "crit", "crit_hurt", "elem_ma"]

    @run_sync
    def setting(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益设置"""
        output: list[BuffInfo] = []
        labels = reserve_setting(buff_list)

        if self.info.constellation >= 2:
            output.append(
                BuffInfo(
                    source=f"{self.name}-C2",
                    name="望月吼哕声",
                )
            )
            if self.info.constellation >= 4:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-C4",
                        name="绯樱引雷章",
                        buff_range="all",
                        buff_type="probuff",
                        setting=BuffSetting(
                            dsc="杀生樱命中||⓪（×）：无增益；①（✓）：全队雷伤+20%",
                            label=labels.get("绯樱引雷章", "1"),
                        ),
                    )
                )
                if self.info.constellation >= 6:
                    output.append(
                        BuffInfo(
                            source=f"{self.name}-C6",
                            name="大杀生咒禁",
                        )
                    )
        if self.info.ascension >= 4:
            output.append(
                BuffInfo(
                    source=f"{self.name}-T2",
                    name="启蛰之祝词",
                    buff_type="transbuff",
                )
            )

        return output

    @run_sync
    def buff(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益列表"""
        for buff in buff_list:
            if buff.name == "望月吼哕声":
                self.C2(buff)
            if buff.name == "绯樱引雷章":
                self.C4(buff)
            if buff.name == "大杀生咒禁":
                self.C6(buff)
            if buff.name == "启蛰之祝词":
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
                weight=weights.get("充能效率阈值", 140),
            )
        )
        output.append(
            DMG(
                index=1,
                source="E",
                name="野干役咒·杀生樱",
                dsc="E每段落雷",
                weight=weights.get("野干役咒·杀生樱", 0),
            )
        )
        output.append(
            DMG(
                index=2,
                source="E",
                name="野干役咒·杀生樱-激化",
                dsc="E每段落雷",
                weight=weights.get("野干役咒·杀生樱-激化", 10),
            )
        )
        output.append(
            DMG(
                index=3,
                source="Q",
                name="大密法·天狐显真",
                dsc="Q每段天狐霆雷",
                weight=weights.get("大密法·天狐显真", 0),
            )
        )
        output.append(
            DMG(
                index=4,
                source="Q",
                name="大密法·天狐显真-激化",
                dsc="Q每段天狐霆雷",
                weight=weights.get("大密法·天狐显真-激化", 5),
            )
        )
        return output

    @run_sync
    def dmg(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害列表"""
        for dmg in dmg_list:
            if dmg.name == "野干役咒·杀生樱" and dmg.weight != 0:
                self.skill_E(dmg)
            if dmg.name == "野干役咒·杀生樱-激化" and dmg.weight != 0:
                self.skill_E(dmg, "超激化")
            if dmg.name == "大密法·天狐显真" and dmg.weight != 0:
                self.skill_Q(dmg)
            if dmg.name == "大密法·天狐显真-激化" and dmg.weight != 0:
                self.skill_Q(dmg, "超激化")
        return dmg_list
