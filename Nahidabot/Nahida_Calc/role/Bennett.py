from nonebot.utils import run_sync

from Nahidabot.utils.classmodel import (
    DMG,
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    FixValue,
    Multiplier,
    PoFValue,
)

from ..dmg_model import reserve_setting, reserve_weight
from ..role_model import RoleModel


class Bennett(RoleModel):
    name = "班尼特"

    C1_to_Q = 0.0
    """Q额外基础攻击加成"""

    def C1(self, buff_info: BuffInfo):
        """冒险憧憬"""
        buff_info.buff = Buff(dsc="美妙旅程额外追加20%基础攻击")
        self.C1_to_Q = 0.2

    def C4(self, buff_info: BuffInfo):
        """热情不灭"""

    def C6(self, buff_info: BuffInfo):
        """烈火与勇气"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            buff_info.buff = Buff(
                dsc="美妙旅程领域内，场上角色火伤+15%，单手剑、双手剑、长柄火附魔",
                triger_type="active",
                elem_dmg_bonus=DMGBonus(pyro=0.15),
            )

    healing_flag = False
    """治疗是否为评分指标"""

    def skill_Q1(self, dmg_info: DMG):
        """美妙旅程(治疗)"""
        calc = self.calculator
        calc.set(
            value_type="H",
            member_type="off",
            multiplier=Multiplier(
                hp=self.scaling_table[2].multiplier[self.info.skill_Q - 1]
            ),
            fix_value=FixValue(
                heal=self.scaling_table[1].multiplier[self.info.skill_Q - 1]
            ),
        )
        calc += self.dmgbuff
        dmg_info.exp_value = int(calc.get_healing())
        self.healing_flag = True

    def skill_Q_buff(self, buff_info: BuffInfo):
        """美妙旅程-鼓舞领域"""
        setting = buff_info.setting
        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            atk_per_bonus = (
                self.C1_to_Q + self.scaling_table[0].multiplier[self.info.skill_Q - 1]
            )
            buff_info.buff = Buff(
                dsc=f"领域内，攻击力加成 => +{round(self.fight_prop.atk_base*atk_per_bonus/100)}",
                triger_type="active",
                atk=PoFValue(percent=atk_per_bonus),
            )

    @property
    def valid_prop(self):
        props = []
        if self.healing_flag:
            props.extend(["hp", "hp_per", "heal"])
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
                    name="冒险憧憬",
                    buff_range="all",
                    buff_type="propbuff",
                )
            )
            if self.info.constellation >= 4:
                pass
                if self.info.constellation == 6:
                    output.append(
                        BuffInfo(
                            source=f"{self.name}-C6",
                            name="烈火与勇气",
                            buff_range="all",
                            setting=BuffSetting(
                                dsc="美妙旅程领域内||⓪（×）：无增益；①（✓）：火伤+15%",
                                label=labels.get("烈火与勇气", "1"),
                            ),
                        )
                    )
        output.append(
            BuffInfo(
                source=f"{self.name}-Q",
                name="美妙旅程-鼓舞领域",
                buff_range="all",
                buff_type="propbuff",
                setting=BuffSetting(
                    dsc="美妙旅程领域内||⓪（×）：无增益；①（✓）：获得攻击力加成",
                    label=labels.get("美妙旅程-鼓舞领域", "1"),
                ),
            )
        )
        return output

    @run_sync
    def buff(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益列表"""
        for buff in buff_list:
            if buff.name == "冒险憧憬":
                self.C1(buff)
            if buff.name == "烈火与勇气":
                self.C6(buff)
            if buff.name == "美妙旅程-鼓舞领域":
                self.skill_Q_buff(buff)

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
                weight=240,
            )
        )
        output.append(
            DMG(
                index=1,
                source="Q",
                name="鼓舞领域-治疗",
                type="H",
                dsc="生命回复每段",
                weight=weights.get("鼓舞领域-治疗", 10),
            )
        )
        return output

    @run_sync
    def dmg(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害列表"""
        for dmg in dmg_list:
            if dmg.name == "鼓舞领域-治疗" and dmg.weight != 0:
                self.skill_Q1(dmg)

        return dmg_list
