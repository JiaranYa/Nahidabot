from typing import Optional

import numpy as np

from Nahidabot.utils.classmodel import (
    DMG,
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    FightProp,
    FixValue,
    Multiplier,
    PoFValue,
    PropInfo,
    Role,
    SkillMultiplier,
)

from ..dmg_model import DMGCalc

# async def Shougun(
#     talent: PropInfo,
#     fightprop: FightProp,
#     scaling_table: list[SkillMultiplier],
#     buff_list: list[BuffInfo],
# ) -> list[DMG]:
#     """雷电影"""
#     output: list[DMG] = []

#     Shougun = DMGCalc(
#         level=talent.level,
#         basic_prop=CalcProp(atk=fightprop.atk, atk_base=fightprop.atk_base),
#         crit_rate=fightprop.crit_rate,
#         crit_dmg=fightprop.crit_dmg,
#         elem_mastery=fightprop.elemental_mastery,
#         recharge=fightprop.recharge,
#     )

#     # ----------------------------------------
#     # Q 梦想一刀
#     # ----------------------------------------
#     # 基础值
#     Shougun1 = Shougun.set(value_type="Q", elem_type="electro").buff(
#         extra_mutiplier=Multiplier(atk=scaling_table[0].multiplier[talent.skill_Q - 1]),
#         extra_elem_dmg_bonus=DMGBonus(electro=fightprop.electro_dmg_bonus),
#     )
#     # 增益加成
#     for buff in buff_list:
#         Shougun1 += buff

#     # 愿力加成
#     Shougun1.get_dmg(mode="exp")

#     output.append(
#         DMG(
#             index=1,
#             dsc="Q梦想一刀伤害",
#             exp_hit=int(Shougun1.get_dmg(mode="exp")),
#             crit_hit=int(Shougun1.get_dmg(mode="crit")),
#         )
#     )

#     return output


# async def Shougun_buff(
#     talent: PropInfo,
#     scaling_table: list[SkillMultiplier],
#     buff_list: list[BuffInfo],
#     prop: Optional[PropTensor] = None,
# ) -> list[BuffInfo]:
#     """
#     雷电影的增益表
#     Args:
#         prop:角色面板
#     """
#     for buff in buff_list:
#         # 二命
#         if buff.source == "C2":
#             buff.buff = [
#                 Buff(
#                     name="斩铁断金",
#                     dsc="Q无视60%防御力",
#                     target="Q",
#                     def_piercing=0.6,
#                 )
#             ]
#         # 四命
#         if buff.source == "C4":
#             (setting,) = buff.setting

#             if setting.label == 0:
#                 setting.state = "×"
#             else:
#                 setting.state = "✓"
#                 buff.buff.append(
#                     Buff(
#                         name="誓奉常道",
#                         dsc="梦想一心状态结束10s内，其余友方攻击+30%",
#                         triger_type="party",
#                         basic_prop=PoFValue(atk_percent=0.3),
#                     )
#                 )
#         # 固定天赋2
#         if buff.source == "T2":
#             dmg_bonus = (prop.recharge - 1) * 100 * 0.004 if prop else 0
#             buff.buff.append(
#                 Buff(
#                     name="殊胜之御体",
#                     dsc=f"充能效率转雷元素增伤 => +{dmg_bonus*100:.1f}%",
#                     elem_type="electro",
#                     triger_type="self",
#                     trans_matrix_list=TransMat()
#                     .set_mask(pos=[6], value=[1])
#                     .set_matrix(pos=[(6, 7)], value=[0.4]),
#                 )
#             )
#         # 元素战技
#         if buff.source == "E":
#             (setting,) = buff.setting

#             if setting.label == 0:
#                 setting.state = "×"
#             else:
#                 dmg_bonus = scaling_table[4].multiplier[talent.skill_E - 1]
#                 buff.buff.append(
#                     Buff(
#                         name="神变•恶曜开眼-雷罚恶曜之眼",
#                         dsc=f"元素爆发伤害+{dmg_bonus}%",
#                         target="Q",
#                         triger_type="all",
#                         elem_dmg_bonus=DMGBonus(all=dmg_bonus / 100),
#                     )
#                 )
#         # 元素爆发
#         if buff.source == "Q":
#             (setting,) = buff.setting

#             stack = max(0, min(60, setting.label))
#             setting.state = f"{stack}层"
#             scaling_bonus1 = scaling_table[1].multiplier[talent.skill_Q - 1] * stack
#             scaling_bonus2 = (
#                 scaling_table[2].multiplier[talent.skill_Q - 1] * prop.atk / 100
#                 if prop
#                 else 0
#             )

#             buff.buff.append(
#                 Buff(
#                     name="奥义•梦想真说-诸愿百眼",
#                     dsc=f"元素爆发倍率+{scaling_bonus1+scaling_bonus2}%",
#                     target="Q",
#                     mutiplier=Multiplier(atk=scaling_bonus1),
#                     trans_matrix_list=TransMat().set_matrix(
#                         pos=[(1, 9)],
#                         value=[scaling_table[2].multiplier[talent.skill_Q - 1] / 100],
#                     ),
#                 )
#             )

#     return buff_list


# async def Shougun_setting(
#     talent: PropInfo,
#     scaling_table: list[SkillMultiplier],
#     buff_list: list[BuffInfo],
# ) -> list[BuffInfo]:
#     """生成增益设置模板"""
#     output = []
#     # 命座
#     if talent.constellation >= 2:
#         output.append(BuffInfo(source="C2"))

#         if talent.constellation >= 4:
#             label = 1
#             for b in buff_list:
#                 if b.source == "C4":
#                     (s,) = b.setting
#                     label = s.label

#             output.append(
#                 BuffInfo(
#                     source="C4",
#                     setting=[
#                         BuffSetting(
#                             name="誓奉常道",
#                             dsc="梦想一心结束时||⓪（×）：无增益；①（✓）：全队攻击+20%",
#                             label=label,
#                         )
#                     ],
#                 )
#             )
#     # 固定天赋
#     if talent.ascension >= 4:
#         output.append(BuffInfo(source="T2"))
#     # 元素战技
#     label = 1
#     for b in buff_list:
#         if b.source == "E":
#             (s,) = b.setting
#             label = s.label

#     bonus = scaling_table[4].multiplier[talent.skill_E - 1]
#     output.append(
#         BuffInfo(
#             source="E",
#             setting=[
#                 BuffSetting(
#                     name="神变•恶曜开眼-雷罚恶曜之眼",
#                     dsc=f"元素战技||⓪（×）：无增益；①（✓）：元素爆发伤害提高{bonus}",
#                     label=label,
#                 )
#             ],
#         )
#     )
#     # 元素爆发
#     label = 30
#     for b in buff_list:
#         if b.source == "Q":
#             (s,) = b.setting
#             label = s.label
#     bonus1 = scaling_table[1].multiplier[talent.skill_Q - 1]
#     bonus2 = scaling_table[2].multiplier[talent.skill_Q - 1]
#     output.append(
#         BuffInfo(
#             source="Q",
#             setting=[
#                 BuffSetting(
#                     name="奥义•梦想真说-诸愿百眼",
#                     dsc=f"愿力层数||0~60层:元素爆发倍率，每层+{bonus1}%，每点攻击+{bonus2}",
#                     label=label,
#                 )
#             ],
#         )
#     )
#     return output
