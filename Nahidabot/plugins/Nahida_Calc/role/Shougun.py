import numpy as np

from Nahidabot.utils.classmodel import (Buff, BuffList, CalcProp, DMGBonus,
                                        DmgInfo, FixValue, Multiplier,
                                        PropBuff, PropTensor, Role, TransMat,
                                        TransMatList)

from ..dmg_model import DMGCalc


def Shougun(prop: Role, setting="") -> list[DmgInfo]:
    """雷电影"""
    output: list[DmgInfo] = []
    scaling_table = prop.scaling_table
    talent = prop.talent
    fightprop = prop.fight_prop

    if not scaling_table or not talent or not fightprop:
        return []

    Shougun = DMGCalc(
        level=talent.level,
        basic_prop=CalcProp(atk=fightprop.atk, atk_base=fightprop.atk_base),
        crit_rate=fightprop.crit_rate,
        crit_dmg=fightprop.crit_dmg,
        elem_mastery=fightprop.elemental_mastery,
        recharge=fightprop.recharge,
    )

    # ----------------------------------------
    # Q 梦想一刀
    # ----------------------------------------
    # 基础值
    Shougun1 = Shougun.set(value_type="Q", elem_type="electro").buff(
        extra_mutiplier=Multiplier(atk=scaling_table[0].multiplier[talent.level]),
        extra_dmg_bonus=DMGBonus(electro=fightprop.electro_dmg_bonus),
    )
    # 愿力加成
    Shougun1.get_dmg(mode="exp")

    output.append(
        DmgInfo(
            index=1,
            dsc="Q梦想一刀伤害",
            exp_hit=int(Shougun1.get_dmg(mode="exp")),
            crit_hit=int(Shougun1.get_dmg(mode="crit")),
        )
    )

    return output


def Shougun_buff(prop: Role) -> list[BuffList]:
    """
    雷电影的增益表
    Args:
        prop:角色面板
    """

    conste = prop.talent.constellation if prop.talent else 0
    ascension = prop.talent.ascension if prop.talent else 0
    E_level = prop.talent.skill_E if prop.talent else 0
    output = []

    if conste >= 2:
        buff = [
            Buff(
                name="斩铁断金",
                dsc="Q无视60%防御力",
                value_type="Q",
                member_type="self",
                def_piercing=0.6,
            )
        ]
        output.append(BuffList(source="C2", buff=buff))
        if conste >= 4:
            buff = [
                Buff(
                    name="誓奉常道",
                    dsc="Q状态结束，其余友方攻击力提升30%",
                    prop_type="atk",
                    member_type="party",
                    basic_prop=PropBuff(atk_percent=0.3),
                )
            ]
            output.append(BuffList(source="C4", buff=buff))

    if ascension >= 4:
        if prop.fight_prop:
            dmg_bonus = (prop.fight_prop.recharge - 1) * 100 * 0.004
            mask = np.zeros(9)
            mask[6] = 1
            t_mat = np.zeros([9, 9])
            t_mat[6, 7] = 0.4
            buff = [
                Buff(
                    name="殊胜之御体",
                    dsc=f"充能效率转雷元素增伤 => {dmg_bonus*100}%",
                    elem_type="electro",
                    member_type="self",
                    trans_matrix_list=TransMatList([TransMat(mask=mask, t_mat=t_mat)]),
                ),
            ]
            output.append(BuffList(source="T2", buff=buff))
        else:
            raise KeyError("面板数据不存在")

    if E_level:
        dmg_bonus = 1
        buff = [
            Buff(
                name="雷罚恶曜之眼",
                dsc=f"元素爆发伤害提高 => {dmg_bonus*100}%",
                value_type="Q",
                dmg_bonus=DMGBonus(all=dmg_bonus),
            ),
        ]
        output.append(BuffList(source="E", buff=buff))

    return output
