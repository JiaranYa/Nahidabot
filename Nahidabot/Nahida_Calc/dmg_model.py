from typing import Literal, Union

import numpy as np

from Nahidabot.utils.classmodel import (
    BuffList,
    CalcProp,
    DMGBonus,
    FixValue,
    Multiplier,
    PropBuff,
    PropTensor,
    TransMat,
)
from Nahidabot.utils.file import load_json

factor_map = load_json(path="./base_factor.json")

ValueType = Literal["NA", "CA", "PA", "E", "Q", "H", "S", ""]
ElemType = Literal[
    "phy", "pyro", "electro", "hydro", "dendro", "anemo", "geo", "cryo", ""
]
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
        value_type: ValueType = "",
        elem_type: ElemType = "",
        reaction_type: ReaType = "",
        level: int = 90,
        basic_prop: CalcProp = CalcProp(),
        mutiplier: Multiplier = Multiplier(),
        crit_rate: float = 0,
        crit_dmg: float = 0,
        elem_mastery: float = 0,
        recharge: float = 1,
        dmg_bonus: DMGBonus = DMGBonus(),
        healing: float = 0,
        elem_res: float = 0.1,
        def_res: float = 0,
        def_piercing: float = 0,
        fix_value: FixValue = FixValue(),
        reaction_factor: float = 1,
        trans_matrix: TransMat = TransMat().initialise(),
    ) -> None:

        self.value_type: ValueType = value_type
        """数值类型:NA-普攻 CA-重击 PA-下落攻击 E-战技 Q-爆发 H-治疗 S-护盾"""
        self.elem_type: ElemType = elem_type
        """元素类型"""
        self.reaction_type: ReaType = reaction_type
        """元素反应类型：\\
        剧变："燃烧", "超导", "扩散", "感电", "碎冰", "超载", "原绽放", "烈绽放", "超绽放", "结晶"\\
        增幅："火蒸发", "冰融化", "水蒸发", "火融化", "蔓激化", "超激化"
        """
        self.level = level
        """等级"""
        self.basic_prop = basic_prop
        """攻击/生命/防御"""
        self.multiplier = mutiplier
        """倍率"""
        self.crit_rate = crit_rate
        """暴击率"""
        self.crit_dmg = crit_dmg
        """暴击伤害"""
        self.elem_mastery = elem_mastery
        """元素精通"""
        self.recharge = recharge
        """充能"""
        self.dmg_bonus_list = dmg_bonus
        """增伤"""
        self.healing = healing
        """治疗"""
        self.elem_resistance = elem_res
        """元素抗性"""
        self.def_resistance = def_res
        """防御抗性"""
        self.def_piercing = def_piercing
        """无视防御"""
        self.fix_value = fix_value
        """固定伤害/治疗/盾量"""
        self.rea_factor = reaction_factor
        """反应系数加成"""
        self.matrix_list = trans_matrix
        """转移矩阵 可叠加为列表
            第一个为阈值矩阵，第二个为转移矩阵
            两两配对
        """

    def set(
        self,
        value_type: ValueType = "",
        elem_type: ElemType = "",
        reaction_type: ReaType = "",
        mutiplier: Union[Multiplier, None] = None,
    ):
        """
        函数：复制/设定伤害属性
        Args:
            value_type  :数值类型
            elem_type   :伤害元素类型
            mutiplier   :倍率
        Returns:
            新伤害属性
        """
        return DMGCalc(
            value_type=value_type if value_type else self.value_type,
            elem_type=elem_type if elem_type else self.elem_type,
            reaction_type=reaction_type if reaction_type else self.reaction_type,
            mutiplier=mutiplier if mutiplier else self.multiplier,
            level=self.level,
            basic_prop=self.basic_prop,
            crit_rate=self.crit_rate,
            crit_dmg=self.crit_dmg,
            elem_mastery=self.elem_mastery,
            recharge=self.recharge,
            dmg_bonus=self.dmg_bonus_list,
            healing=self.healing,
            elem_res=self.elem_resistance,
            def_res=self.def_resistance,
            def_piercing=self.def_piercing,
            fix_value=self.fix_value,
            reaction_factor=self.rea_factor,
            trans_matrix=self.matrix_list,
        )

    def buff(
        self,
        extra_prop: PropBuff = PropBuff(),
        extra_mutiplier: Multiplier = Multiplier(),
        extra_crit_rate: float = 0,
        extra_crit_dmg: float = 0,
        extra_elem_mastery: float = 0,
        extra_recharge: float = 0,
        extra_dmg_bonus: DMGBonus = DMGBonus(),
        extra_healing: float = 0,
        resist_reduction: float = 0,
        def_reduction: float = 0,
        def_piercing: float = 0,
        extra_fixvalue: FixValue = FixValue(),
        extra_reaction_coeff: float = 0,
        extra_trans_matrix: TransMat = TransMat(),
    ):
        """
        函数：获取增益后的面板数值
        @params: 面板增益数值
        @returns: 新面板数值
        """

        return DMGCalc(
            value_type=self.value_type,
            elem_type=self.elem_type,
            reaction_type=self.reaction_type,
            level=self.level,
            basic_prop=self.basic_prop + extra_prop,
            mutiplier=self.multiplier + extra_mutiplier,
            crit_rate=self.crit_rate + extra_crit_rate,
            crit_dmg=self.crit_dmg + extra_crit_dmg,
            elem_mastery=self.elem_mastery + extra_elem_mastery,
            recharge=self.recharge + extra_recharge,
            dmg_bonus=self.dmg_bonus_list + extra_dmg_bonus,
            healing=self.healing + extra_healing,
            elem_res=self.elem_resistance - resist_reduction,
            def_res=self.def_resistance - def_reduction,
            def_piercing=self.def_piercing + def_piercing,
            fix_value=self.fix_value + extra_fixvalue,
            reaction_factor=self.rea_factor + extra_reaction_coeff,
            trans_matrix=self.matrix_list + extra_trans_matrix,
        )

    # @property
    # def dmg_bonus(self) -> float:
    #     if self.elem_type in "phy":
    #         return self.dmg_bonus_list[self.elem_type] + self.dmg_bonus_list["all"]
    #     elif self.elem_type:
    #         return (
    #             self.dmg_bonus_list[self.elem_type]
    #             + self.dmg_bonus_list["elem"]
    #             + self.dmg_bonus_list["all"]
    #         )
    #     else:
    #         return 0

    @property
    def prop(self):
        """
        发生转移加成后的基础属性列表
        """
        row_vec = np.array(
            [
                self.basic_prop.hp,
                self.basic_prop.atk,
                self.basic_prop.defend,
                self.elem_mastery,
                self.crit_rate,
                self.crit_dmg,
                self.recharge,
                self.dmg_bonus_list[self.elem_type],
                self.healing,
                0,
            ]
        )
        # 属性向量
        #     0-生命值    1-攻击力    2-防御力
        #     3-精通      4-暴击      5-暴伤
        #     6-充能      7-增伤      8-治疗
        #     9-攻击倍率
        output: np.ndarray = np.zeros(10)
        output += np.dot(row_vec - self.matrix_list.mask, self.matrix_list.t_mat)

        if self.elem_type in "phy":
            dmg_bonus = output[7] + self.dmg_bonus_list["all"]
        elif self.elem_type:
            dmg_bonus = (
                output[7] + self.dmg_bonus_list["elem"] + self.dmg_bonus_list["all"]
            )
        else:
            dmg_bonus = 0

        return PropTensor(
            hp=output[0],
            atk=output[1],
            defend=output[2],
            elem_mastery=output[3],
            crit_rate=output[4],
            crit_dmg=output[5],
            recharge=output[6],
            dmg_bonus=dmg_bonus,
            healing=output[8],
            multiplier=Multiplier(atk=output[9]) + self.multiplier,
        )

    @property
    def base_value(self):
        """"""
        return (
            self.prop.hp * self.prop.multiplier.hp
            + self.prop.atk * self.prop.multiplier.atk
            + self.prop.defend * self.prop.multiplier.defend
            + self.prop.elem_mastery * self.prop.multiplier.em
        ) / 100

    @property
    def base_dmg_zone(self):
        """基础伤害乘区"""
        return self.base_value + self.fix_value.dmg

    @property
    def dmg_bonus_zone(self):
        """增伤区"""
        return 1 + self.prop.dmg_bonus

    @property
    def expectation_hit_zone(self):
        """暴击期望区"""
        return 1 + min(max(self.prop.crit_rate, 0), 1) * self.prop.crit_dmg

    @property
    def crit_hit_zone(self):
        """必定暴击"""
        return 1 + self.prop.crit_dmg

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
            return self.rea_factor + 2.78 * self.prop.elem_mastery / (
                self.prop.elem_mastery + 1400
            )
        elif self.reaction_type in ["蔓激化", "超激化"]:
            return self.rea_factor + 5 * self.prop.elem_mastery / (
                self.prop.elem_mastery + 1200
            )
        elif self.reaction_type == "结晶":
            return self.rea_factor + 4.44 * self.prop.elem_mastery / (
                self.prop.elem_mastery + 1400
            )
        else:
            return self.rea_factor + 16 * self.prop.elem_mastery / (
                self.prop.elem_mastery + 2000
            )

    def get_dmg(self, mode) -> float:
        """
        非反应伤害计算器
        Args:
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
        return (self.base_value + self.fix_value.heal) * self.prop.healing

    def get_shield(self):
        """盾量"""
        return self.base_value + self.fix_value.shield

    def __add__(self, other: BuffList):
        output = self.set()
        for buff in other.buff:
            if (
                output.value_type in buff.value_type
                and output.reaction_type in buff.reaction_type
            ):
                if output.elem_type == "phy":
                    if any(e in buff.elem_type for e in ["all", "phy"]):
                        pass
                    else:
                        break
                else:
                    if any(
                        e in buff.elem_type for e in ["all", "elem", output.elem_type]
                    ):
                        pass
                    else:
                        break
            else:
                break

            output = output.buff(
                extra_prop=buff.basic_prop,
                extra_mutiplier=buff.mutiplier,
                extra_crit_rate=buff.crit_rate,
                extra_crit_dmg=buff.crit_dmg,
                extra_elem_mastery=buff.elem_mastery,
                extra_recharge=buff.recharge,
                extra_dmg_bonus=buff.dmg_bonus,
                extra_healing=buff.healing,
                resist_reduction=buff.resist_reduction,
                def_reduction=buff.def_reduction,
                def_piercing=buff.def_piercing,
                extra_fixvalue=buff.fix_value,
                extra_reaction_coeff=buff.reaction_coeff,
                extra_trans_matrix=buff.trans_matrix_list,
            )
        return output


# class BufferList(List[Buff]):
#     """增益缓存表"""

#     def __init__(self, buff: List[Buff]):
#         super().__init__(buff)

#     def __add__(self, other: "BufferList"):
#         output = self.copy()
#         adder = other.copy()
#         for i, a in enumerate(output):
#             for j, b in enumerate(adder):
#                 if a.value_type == b.value_type and a.elem_type == b.elem_type:
#                     del output[i]
#                     del adder[j]
#                     output.append(a + b)
#                     break
#                 else:
#                     output.append(b)

#         return BufferList(output)
