from copy import deepcopy
from typing import Literal

from Nahidabot.utils.classmodel import (
    DMG,
    BuffInfo,
    DMGBonus,
    FightProp,
    FixValue,
    Multiplier,
    PoFValue,
)
from Nahidabot.utils.file import load_json

factor_map = load_json(path="./base_factor.json")

ValueType = Literal["NA", "CA", "PA", "E", "Q", "H", "S", ""]
ElemType = Literal[
    "phy", "pyro", "electro", "hydro", "dendro", "anemo", "geo", "cryo", ""
]
MemberType = Literal["active", "off"]
ReaType = Literal[
    "火蒸发",
    "冰融化",
    "水蒸发",
    "火融化",
    "蔓激化",
    "超激化",
    "燃烧",
    "超导",
    "扩散",
    "感电",
    "碎冰",
    "超载",
    "原绽放",
    "烈绽放",
    "超绽放",
    "结晶",
    "",
]


class DMGCalc:
    """
    伤害计算器
    """

    def __init__(
        self,
        prop: FightProp,
        level: int = 90,
    ) -> None:

        self.value_type: ValueType = ""
        """数值类型:NA-普攻 CA-重击 PA-下落攻击 E-战技 Q-爆发 H-治疗 S-护盾"""
        self.elem_type: ElemType = ""
        """元素类型"""
        self.member_type: MemberType = "active"
        """出伤类型：
            active-前台结算
            off-后台结算
        """
        self.reaction_type: ReaType = ""
        """元素反应类型：\\
        剧变："燃烧", "超导", "扩散", "感电", "碎冰", "超载", "原绽放", "烈绽放", "超绽放", "结晶"\\
        增幅："火蒸发", "冰融化", "水蒸发", "火融化", "蔓激化", "超激化"
        """
        self.level = level
        """等级"""
        self.hp = prop.hp
        """生命上限"""
        self.atk = prop.atk
        """攻击力"""
        self.defend = prop.defend
        """防御力"""
        self.hp_base = prop.hp_base
        """基础生命上限"""
        self.atk_base = prop.atk_base
        """基础攻击力"""
        self.def_base = prop.def_base
        """基础防御力"""
        self.multiplier = Multiplier()
        """倍率"""
        self.crit_rate = prop.crit_rate
        """暴击率"""
        self.crit_dmg = prop.crit_dmg
        """暴击伤害"""
        self.elem_mastery = prop.elemental_mastery
        """元素精通"""
        self.recharge = prop.recharge
        """充能"""
        self.elem_dmg_bonus = DMGBonus(
            phy=prop.phy_dmg_bonus,
            pyro=prop.pyro_dmg_bonus,
            electro=prop.electro_dmg_bonus,
            hydro=prop.hydro_dmg_bonus,
            dendro=prop.dendro_dmg_bonus,
            anemo=prop.anemo_dmg_bonus,
            geo=prop.geo_dmg_bonus,
            cryo=prop.cryo_dmg_bonus,
        )
        """元素增伤加成"""
        self.healing = prop.healing
        """治疗"""
        self.shield_strength: float = 0
        """护盾强效"""
        self.dmg_bonus: float = 0
        """增伤"""
        self.elem_resistance: float = 0.1
        """元素抗性"""
        self.def_resistance: float = 0
        """防御抗性"""
        self.def_piercing: float = 0
        """无视防御"""
        self.fix_value = FixValue()
        """固定伤害/治疗/盾量"""
        self.rea_factor = 1
        """反应系数加成"""

    def copy(self):
        return deepcopy(self)

    def set(
        self,
        value_type: ValueType = "",
        elem_type: ElemType = "",
        member_type: MemberType = "active",
        reaction_type: ReaType = "",
        multiplier: Multiplier = Multiplier(),
        fix_value: FixValue = FixValue(),
    ):
        """
        函数：复制/设定伤害属性\\
        Params:
            value_type  :数值类型
            elem_type   :伤害元素类型
            member_type :是否脱手
            reaction_type :反应类型
            multiplier   :倍率
            fix_value   :基础值
        """
        self.value_type = value_type
        self.elem_type = elem_type
        self.member_type = member_type
        self.reaction_type = reaction_type
        self.multiplier = multiplier
        self.fix_value = fix_value
        return self

    def buff(
        self,
        extra_hp: PoFValue = PoFValue(),
        extra_atk: PoFValue = PoFValue(),
        extra_def: PoFValue = PoFValue(),
        extra_mutiplier: Multiplier = Multiplier(),
        extra_crit_rate: float = 0,
        extra_crit_dmg: float = 0,
        extra_elem_mastery: float = 0,
        extra_recharge: float = 0,
        extra_elem_dmg_bonus: DMGBonus = DMGBonus(),
        extra_healing: float = 0,
        extra_shield: float = 0,
        extra_dmg_bonus: float = 0,
        resist_reduction: float = 0,
        def_reduction: float = 0,
        def_piercing: float = 0,
        extra_fixvalue: FixValue = FixValue(),
        extra_reaction_coeff: float = 0,
    ):
        """
        函数：获取增益后的面板数值
        @params: 面板增益数值
        @returns: 新面板数值
        """
        self.hp += extra_hp.fix + extra_hp.percent * self.hp_base
        self.atk += extra_atk.fix + extra_atk.percent * self.atk_base
        self.defend += extra_def.fix + extra_def.percent * self.def_base
        self.multiplier += extra_mutiplier
        self.crit_rate += extra_crit_rate
        self.crit_dmg += extra_crit_dmg
        self.elem_mastery += extra_elem_mastery
        self.recharge += extra_recharge
        self.elem_dmg_bonus += extra_elem_dmg_bonus
        self.dmg_bonus += extra_dmg_bonus
        self.healing += extra_healing
        self.shield_strength += extra_shield
        self.elem_resistance -= resist_reduction
        self.def_resistance -= def_reduction
        self.def_piercing += def_piercing
        self.fix_value += extra_fixvalue
        self.rea_factor += extra_reaction_coeff
        return self

    @property
    def base_value(self):
        """基础数值"""
        return (
            self.multiplier.hp * self.hp
            + self.multiplier.atk * self.atk
            + self.multiplier.defend * self.defend
            + self.multiplier.em * self.elem_mastery
        ) / 100

    @property
    def base_dmg_zone(self):
        """基础伤害乘区"""
        return self.base_value + self.fix_value.dmg

    @property
    def dmg_bonus_zone(self):
        """增伤区"""
        return 1 + self.elem_dmg_bonus[self.elem_type] + self.dmg_bonus

    @property
    def expectation_hit_zone(self):
        """暴击期望区"""
        return 1 + min(max(self.crit_rate, 0), 1) * self.crit_dmg

    @property
    def crit_hit_zone(self):
        """必定暴击"""
        return 1 + self.crit_dmg

    @property
    def elem_res_zone(self):
        """抗性区"""
        if (elem_res := self.elem_resistance) < 0:
            return 1 - elem_res / 2
        elif elem_res <= 0.75:
            return 1 - elem_res
        else:
            return 1 / (1 + elem_res * 4)

    @property
    def def_res_zone(self):
        """防御区"""
        return (self.level + 100) / (
            (self.level + 100)
            + (1 - self.def_piercing) * (1 + self.def_resistance) * (90 + 100)
        )

    @property
    def reaction_zone(self):
        """反应区"""
        if self.reaction_type in ["火蒸发", "冰融化", "水蒸发", "火融化"]:
            return self.rea_factor + 2.78 * self.elem_mastery / (
                self.elem_mastery + 1400
            )
        elif self.reaction_type in ["蔓激化", "超激化"]:
            return self.rea_factor + 5 * self.elem_mastery / (self.elem_mastery + 1200)
        elif self.reaction_type == "结晶":
            return self.rea_factor + 4.44 * self.elem_mastery / (
                self.elem_mastery + 1400
            )
        else:
            return self.rea_factor + 16 * self.elem_mastery / (self.elem_mastery + 2000)

    def get_dmg(self, mode="") -> float:
        """
        非反应伤害计算器
        Params:
            mode:   "exp":期望伤害
                    "crit":暴击伤害
                    "":无暴击
        """
        if mode == "exp":
            crit_zone = self.expectation_hit_zone
        elif mode == "crit":
            crit_zone = self.crit_hit_zone
        else:
            crit_zone = 1

        return (
            self.base_dmg_zone
            * self.dmg_bonus_zone
            * self.elem_res_zone
            * self.def_res_zone
            * crit_zone
        )

    def get_amp_reac_dmg(
        self,
        mode,
        reaction_type: Literal["火蒸发", "冰融化", "水蒸发", "火融化", "蔓激化", "超激化", ""] = "",
    ):
        """
        增幅反应伤害
        Amplifying Reactions
        """
        if reaction_type in ["火蒸发", "冰融化"]:
            return 1.5 * self.reaction_zone * self.get_dmg(mode)
        elif reaction_type in ["水蒸发", "火融化"]:
            return 2 * self.reaction_zone * self.get_dmg(mode)
        elif reaction_type in ["蔓激化"]:
            boost = factor_map["TransReac"][self.level] * 1.25 * self.reaction_zone
            return self.buff(extra_fixvalue=FixValue(dmg=boost)).get_dmg(mode=mode)
        elif reaction_type in ["超激化"]:
            boost = factor_map["TransReac"][self.level] * 1.15 * self.reaction_zone
            return self.buff(extra_fixvalue=FixValue(dmg=boost)).get_dmg(mode=mode)
        # print("错误调用get_amp_reac_dmg，这不是增幅反应")
        return self.get_dmg(mode)

    def get_trans_reac_dmg(
        self,
        reaction_type: Literal[
            "", "燃烧", "超导", "扩散", "感电", "碎冰", "超载", "原绽放", "烈绽放", "超绽放"
        ] = "",
    ):
        """
        剧变反应伤害
        Transformative Reactions
        """
        factor_list = {
            "燃烧": 0.25,
            "超导": 0.5,
            "扩散": 0.6,
            "感电": 1.2,
            "碎冰": 1.5,
            "超载": 2,
            "原绽放": 2,
            "烈绽放": 3,
            "超绽放": 3,
        }
        if reaction_type in factor_list.keys():
            return (
                factor_list[reaction_type]
                * factor_map["TransReac"][self.level]
                * self.reaction_zone
                * self.elem_res_zone
            )
        else:
            # print("这不是剧变反应")
            return 0

    def get_crystall_shield(self):
        """结晶盾"""
        if self.reaction_zone == "结晶":
            return factor_map["Cryst"][self.level] * self.reaction_zone
        return 0

    def get_healing(self):
        """治疗量"""
        return (self.base_value + self.fix_value.heal) * (1 + self.healing)

    def get_shield(self):
        """盾量"""
        return self.base_value + self.fix_value.shield

    def __add__(self, other: list[BuffInfo]):
        output = self.copy()
        for buff_info in other:
            if (buff := buff_info.buff) is None:
                continue

            if all(e not in buff.reaction_type for e in ["", output.reaction_type]):
                break

            if all(e not in buff.target for e in ["ALL", output.value_type]):
                break

            if output.member_type == "active" and "off" in buff.triger_type:
                break
            if output.member_type == "off" and "active" in buff.triger_type:
                break

            if output.elem_type == "phy":
                if all(e not in buff.elem_type for e in ["all", "phy"]):
                    break
            else:
                if all(
                    e not in buff.elem_type for e in ["all", "elem", output.elem_type]
                ):
                    break

            output.buff(
                extra_hp=buff.hp,
                extra_atk=buff.atk,
                extra_def=buff.defend,
                extra_mutiplier=buff.mutiplier,
                extra_crit_rate=buff.crit_rate,
                extra_crit_dmg=buff.crit_dmg,
                extra_elem_mastery=buff.elem_mastery,
                extra_recharge=buff.recharge,
                extra_elem_dmg_bonus=buff.elem_dmg_bonus,
                extra_dmg_bonus=buff.dmg_bonus,
                extra_healing=buff.healing,
                extra_shield=buff.shield_strength,
                resist_reduction=buff.resist_reduction,
                def_reduction=buff.def_reduction,
                def_piercing=buff.def_piercing,
                extra_fixvalue=buff.fix_value,
                extra_reaction_coeff=buff.reaction_coeff,
            )
        return output


def reserve_setting(buff_list: list[BuffInfo]):
    """保留设置"""
    output: dict[str, str] = {}
    for buff in buff_list:
        output |= {buff.name: buff.setting.label}
    return output


def reserve_weight(dmg_list: list[DMG]):
    """保留权重"""
    output: dict[str, int] = {}
    for dmg in dmg_list:
        output |= {dmg.name: dmg.weight}
    return output
