from copy import deepcopy

import numpy as np

from Nahidabot.utils.classmodel import (
    DMG,
    Buff,
    BuffInfo,
    DMGBonus,
    PoFValue,
    PropertySlot,
    Relic,
    RelicScore,
)

from .role import RoleModel

slot_dict = {
    "hp_per": 5.83,
    "hp": 298.75,
    "atk_per": 5.83,
    "atk": 19.45,
    "def_per": 7.29,
    "def": 23.15,
    "elem_ma": 23.31,
    "crit": 3.89,
    "crit_hurt": 7.77,
    "charge": 6.48,
    "heal": 4.49,
    "elem": 5.83,
    "phy": 7.29,
}

sub_prop = [
    "hp_per",
    "hp",
    "atk_per",
    "atk",
    "def_per",
    "def",
    "elem_ma",
    "crit",
    "crit_hurt",
    "charge",
]
sands_main_prop = ["hp_per", "atk_per", "def_per", "elem_ma", "charge"]
goblet_main_prop = ["hp_per", "atk_per", "def_per", "elem_ma", "elem", "phy"]
circlet_main_prop = [
    "hp_per",
    "atk_per",
    "def_per",
    "elem_ma",
    "crit",
    "crit_hurt",
    "heal",
]
element = ["pyro", "electro", "hydro", "dendro", "anemo", "geo", "cryo"]


async def get_scores(role: RoleModel):
    """"""
    assert (relic := role.artifacts), "计算分数缺少圣遗物信息"
    output = RelicScore()
    for item in [relic.flower, relic.plume, relic.sands, relic.goblet, relic.circlet]:
        if item is None:
            continue
        new_role = await take_off_item(role, item)
        score = await get_score(new_role, item.type, await role.get_dmg())
        output.set_score(item.type, score)

    return output


async def take_off_item(role: RoleModel, item: Relic):
    """脱圣遗物"""
    new_role = deepcopy(role)
    await extract_prop(new_role, item.main_stat)
    for sub in item.sub_stat_list:
        await extract_prop(new_role, sub)
    return new_role


async def extract_prop(role: RoleModel, slot: PropertySlot):
    """去除属性"""
    assert (prop := role.fight_prop), "计算分数缺少面板信息"
    if slot.name == "FIGHT_PROP_HP_PERCENT":
        prop.hp -= prop.hp_base * slot.value / 100
    elif slot.name == "FIGHT_PROP_HP":
        prop.hp -= slot.value
    elif slot.name == "FIGHT_PROP_ATTACK_PERCENT":
        prop.atk -= prop.atk_base * slot.value / 100
    elif slot.name == "FIGHT_PROP_ATTACK":
        prop.atk -= slot.value
    elif slot.name == "FIGHT_PROP_DEFENSE_PERCENT":
        prop.defend -= prop.def_base * slot.value / 100
    elif slot.name == "FIGHT_PROP_DEFENSE":
        prop.defend -= slot.value
    elif slot.name == "FIGHT_PROP_ELEMENT_MASTERY":
        prop.elemental_mastery -= slot.value
    elif slot.name == "FIGHT_PROP_CRITICAL":
        prop.crit_rate -= slot.value / 100
    elif slot.name == "FIGHT_PROP_CRITICAL_HURT":
        prop.crit_dmg -= slot.value / 100
    elif slot.name == "FIGHT_PROP_HEAL_ADD":
        prop.healing -= slot.value / 100
    elif slot.name == "FIGHT_PROP_CHARGE_EFFICIENCY":
        prop.recharge -= slot.value / 100
    elif slot.name == "FIGHT_PROP_PHYSICAL_ADD_HURT":
        prop.phy_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_FIRE_ADD_HURT":
        prop.pyro_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_WATER_ADD_HURT":
        prop.hydro_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_GRASS_ADD_HURT":
        prop.dendro_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_ELEC_ADD_HURT":
        prop.electro_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_WIND_ADD_HURT":
        prop.anemo_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_ICE_ADD_HURT":
        prop.cryo_dmg_bonus -= slot.value / 100
    elif slot.name == "FIGHT_PROP_ROCK_ADD_HURT":
        prop.geo_dmg_bonus -= slot.value / 100


async def get_score(role: RoleModel, type: str, dmg_true: list[DMG]):
    """计算圣遗物分数"""
    valid_prop = role.valid_prop
    threshold = role.dmg_list[0].weight / 100
    if threshold > role.fight_prop.recharge:
        valid_prop.append("charge")
    max_charge = max(
        np.ceil((threshold - role.fight_prop.recharge) / slot_dict["charge"]), 0
    )
    #
    main_prop_list = await get_main_prop(valid_prop, type)
    prop_list: list[dict[str, int]] = []
    for main_prop in main_prop_list:
        sub_props = [p for p in valid_prop if p not in main_prop and p in sub_prop]
        sub_prop_list = await get_sub_prop(sub_props)
        for props in sub_prop_list:
            for i in range(6):
                for j in range(6 - i):
                    for m in range(6 - i - j):
                        for n in range(6 - i - j - m):
                            sub_prop_dist: dict[str, int] = {}
                            for idx, p in enumerate(props):
                                sub_prop_dist |= {p: [i + 1, j + 1, m + 1, n + 1][idx]}
                            if (
                                sum(sub_prop_dist.values()) == len(sub_prop_dist) + 5
                                and sub_prop_dist.get("charge", 0) <= max_charge
                            ):
                                prop_list.append(main_prop | sub_prop_dist)
    buff_list, prop_valid_list = await get_buff(prop_list)

    def compens_curve(x):
        """
        充能修正曲线:\\
        y= (b-1) / ( (1+7.29/6.48*(thr-x)) * b - 1)\\
        b 为每个圣遗物预期提升\\
        目前b 取 +inf
        """
        if x < threshold:
            return 1 / (1 + 7.29 / slot_dict["charge"] * (threshold - x))
        return 1

    dmg_base = await role.get_dmg()

    async def calc_score(dmg_list: list[DMG], role: RoleModel):
        score = 0.0
        for i, info in enumerate(dmg_list):
            if i == 0:
                continue
            score += info.weight * (info.exp_value / dmg_base[i].exp_value - 1)
        score *= compens_curve(role.get_recharge())
        return score

    true_score = await calc_score(dmg_true, role)

    # true_score = 0.0
    # for i, info in enumerate(dmg_true):
    #     if i == 0:
    #         continue
    #     true_score += info.weight * (info.exp_value / dmg_base[i].exp_value - 1)
    # true_score *= compens_curve(role.fight_prop.recharge)
    max_main_score = 0.01
    for main in main_prop_list:
        (main_buff,), _ = await get_buff([main])
        role_main_prop = deepcopy(role)
        await role_main_prop.load_buff(main_buff, "propbuff")
        dmg_main = await role_main_prop.get_dmg()
        main_score = await calc_score(dmg_main, role_main_prop)
        if max_main_score < main_score:
            max_main_score = main_score

    scores = []
    max_score = 0.1
    for relic_buff in buff_list:
        role_est = deepcopy(role)
        await role_est.load_buff(relic_buff, "propbuff")
        dmg_est = await role_est.get_dmg()
        est_score = await calc_score(dmg_est, role_est)
        if max_score < est_score:
            max_score = est_score
        scores.append(est_score)

    if true_score <= max_main_score:
        return true_score / max_main_score * 20
    else:
        return (true_score - max_main_score) / (max_score - max_main_score) * 40 + 20
    # return true_score / max_score * 60


async def get_main_prop(valid_prop: list[str], type: str):
    """主词条"""
    if type == "flower":
        return [{"hp": 16}]
    if type == "plume":
        return [{"atk": 16}]
    output: list[dict[str, int]] = []
    if type == "sands":
        for prop in valid_prop:
            if prop in sands_main_prop:
                output.append({prop: 8})
    if type == "goblet":
        for prop in valid_prop:
            if prop in goblet_main_prop or prop in element:
                output.append({prop: 8})
    if type == "circlet":
        for prop in valid_prop:
            if prop in circlet_main_prop:
                output.append({prop: 8})
    return output


async def get_sub_prop(props: list[str]):
    """副词条"""
    if (length := len(props)) <= 4:
        return [props]

    output = []
    for i in range(length - 3):
        for j in range(i + 1, length - 2):
            for m in range(j + 1, length - 1):
                for n in range(m + 1, length):
                    output.append(
                        [
                            props[i],
                            props[j],
                            props[m],
                            props[n],
                        ]
                    )

    return output


async def get_buff(props: list[dict[str, int]]):
    """生成圣遗物增益"""
    buff_list: list[list[BuffInfo]] = []
    relic_list: list[dict[str, int]] = []
    for prop in props:
        if (hp := prop.get("hp", 0)) != 16 and prop.get("hp_per", 0) != 8 and hp > 1:
            continue
        if (
            (atk := prop.get("atk", 0)) != 16
            and prop.get("atk_per", 0) != 8
            and atk > 1
        ):
            continue
        if prop.get("def_per", 0) != 8 and prop.get("def", 0) > 1:
            continue
        buff_list.append(await create_buff(prop))
        relic_list.append(prop)
    return buff_list, relic_list


async def create_buff(dic: dict[str, int]):
    output: list[BuffInfo] = []
    for key, value in dic.items():
        buff = BuffInfo(
            buff_type="propbuff",
        )
        if key == "hp":
            buff.buff = Buff(hp=PoFValue(fix=slot_dict["hp"] * value))
        elif key == "hp_per":
            buff.buff = Buff(hp=PoFValue(percent=slot_dict["hp_per"] * value / 100))
        elif key == "atk":
            buff.buff = Buff(atk=PoFValue(fix=slot_dict["atk"] * value))
        elif key == "atk_per":
            buff.buff = Buff(atk=PoFValue(percent=slot_dict["atk_per"] * value / 100))
        elif key == "def":
            buff.buff = Buff(defend=PoFValue(fix=slot_dict["def"] * value))
        elif key == "def_per":
            buff.buff = Buff(
                defend=PoFValue(percent=slot_dict["def_per"] * value / 100)
            )
        elif key == "elem_ma":
            buff.buff = Buff(elem_mastery=slot_dict["elem_ma"] * value)
        elif key == "crit":
            buff.buff = Buff(crit_rate=slot_dict["crit"] * value / 100)
        elif key == "crit_hurt":
            buff.buff = Buff(crit_dmg=slot_dict["crit_hurt"] * value / 100)
        elif key == "charge":
            buff.buff = Buff(recharge=slot_dict["charge"] * value / 100)
        elif key == "heal":
            buff.buff = Buff(healing=slot_dict["heal"] * value / 100)
        elif key in element:
            buff.buff = Buff(
                elem_dmg_bonus=DMGBonus().set(key, slot_dict["elem"] * value / 100)
            )
        elif key == "phy":
            buff.buff = Buff(
                elem_dmg_bonus=DMGBonus().set(key, slot_dict["phy"] * value / 100)
            )
        output.append(buff)

    return output
