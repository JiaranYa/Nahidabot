from typing import Dict, List, Literal, Optional, Union

import numpy as np
from pydantic import BaseModel, Field

# 以下用于数据获取存储


class EnkaInfo(BaseModel):
    """
    ENKA.network 获取的信息
    """

    uid: str
    """玩家uid"""
    playerInfo: Optional[Dict] = None
    """玩家信息"""
    avatarInfoList: Optional[List] = None
    """角色列表"""


class PlayerInfo(BaseModel):
    """
    玩家信息
    """

    uid: str
    """原神uid"""
    nickname: Optional[str]
    """玩家昵称"""
    level: int
    """玩家等级"""
    profile_id: Optional[int]
    """玩家头像"""
    namecard_id: Optional[int]
    """卡片id"""
    signature: Optional[str]
    """签名"""


class SkillMultiplier(BaseModel):
    """
    技能倍率
    """

    skillindex: int = 0
    """技能序号"""
    dsc: str = ""
    """技能描述"""
    multiplier: List[float] = []
    """等级倍率表"""


class RoleInfo(BaseModel):
    """
    角色的基础信息
    """

    name: str = ""
    """角色名"""
    weapon_type: Literal["单手剑", "弓", "长柄", "双手剑", "法器", ""] = ""
    """武器类型"""
    elem_type: Literal["Fire", "Elec", "Water", "Grass", "Wind", "Rock", "Ice", ""] = ""
    """元素类型"""
    region: Literal["蒙德", "璃月", "稻妻", "须弥", "枫丹", "纳塔", "至冬", ""] = ""
    """所属地区"""
    abbr: str = ""
    """缩写"""
    scaling_table: Optional[List[SkillMultiplier]] = None
    """技能倍率表"""
    skill_order: List[int]
    """天赋表"""
    energy_cost: int
    """元素爆发能量"""
    proud_map: dict = {}
    """命座天赋加成"""
    extra_info: Optional[Dict] = None
    """额外信息"""


class PropInfo(BaseModel):
    """
    角色能力信息
    """

    level: int
    """等级"""
    ascension: int
    """突破"""
    element: str
    """神之眼"""
    fetter: int
    """好感度"""
    weapon_type: Literal["单手剑", "弓", "长柄", "双手剑", "法器", ""]
    """武器类型"""
    region: str = ""
    """所属地区"""
    abbr: str
    """简称"""
    constellation: int
    """命座数"""
    skill_A: int
    """普攻等级"""
    skill_E_base: int
    """元素战技等级"""
    skill_Q_base: int
    """元素爆发等级"""
    Q_cost: int
    """元素爆发能量"""
    skill_E_prod: int = 0
    """元素战技加成"""
    skill_Q_prod: int = 0
    """元素爆发加成"""
    party_member: list[str] = []
    """队友"""

    @property
    def skill_icon(self) -> list[str]:
        """图标文件"""
        dic = {"单手剑": "01", "弓": "02", "长柄": "03", "双手剑": "04", "法器": "05"}
        return [
            f"Skill_A_{dic[self.weapon_type]}.png",
            f"Skill_E_{self.abbr}.png",
            f"Skill_Q_{self.abbr}.png",
        ]

    @property
    def skill_E(self):
        """"""
        return self.skill_E_base + self.skill_E_prod

    @property
    def skill_Q(self):
        """"""
        return self.skill_Q_base + self.skill_Q_prod


class DMGBonus(BaseModel):
    """伤害加成"""

    phy: float = 0
    """物理伤害加成"""
    pyro: float = 0
    """火元素伤害加成"""
    electro: float = 0
    """雷元素伤害加成"""
    hydro: float = 0
    """水元素伤害加成"""
    dendro: float = 0
    """草元素伤害加成"""
    anemo: float = 0
    """风元素伤害加成"""
    geo: float = 0
    """岩元素伤害加成"""
    cryo: float = 0
    """冰元素伤害加成"""
    all: float = 0
    """无条件伤害加成"""
    elem: float = 0
    """元素伤害加成"""

    def __add__(self, other: "DMGBonus"):
        return DMGBonus(
            phy=self.phy + other.phy,
            pyro=self.pyro + other.pyro,
            electro=self.electro + other.electro,
            hydro=self.hydro + other.hydro,
            dendro=self.dendro + other.dendro,
            anemo=self.anemo + other.anemo,
            geo=self.geo + other.geo,
            cryo=self.cryo + other.cryo,
            all=self.all + other.all,
            elem=self.elem + other.elem,
        )

    def __getitem__(self, key: str):
        return eval(f"self.{key.lower()}")


class FightProp(BaseModel):
    """
    面板属性
    """

    hp_base: float
    """基础生命值"""
    hp: float
    """生命值上限"""
    atk_base: float
    """基础攻击力"""
    atk: float
    """攻击力"""
    def_base: float
    """基础防御力"""
    defend: float
    """防御力"""
    crit_rate: float
    """暴击率"""
    crit_dmg: float
    """暴击伤害"""
    elemental_mastery: float
    """元素精通"""
    recharge: float
    """元素充能效率"""
    healing: float
    """治疗加成"""
    phy_dmg_bonus: float
    """物理伤害加成"""
    pyro_dmg_bonus: float
    """火元素伤害加成"""
    electro_dmg_bonus: float
    """雷元素伤害加成"""
    hydro_dmg_bonus: float
    """水元素伤害加成"""
    dendro_dmg_bonus: float
    """草元素伤害加成"""
    anemo_dmg_bonus: float
    """风元素伤害加成"""
    geo_dmg_bonus: float
    """岩元素伤害加成"""
    cryo_dmg_bonus: float
    """冰元素伤害加成"""

    @property
    def hp_extra(self) -> float:
        """生命值加成"""
        return self.hp - self.hp_base

    @property
    def atk_extra(self) -> float:
        """攻击力加成"""
        return self.atk - self.atk_base

    @property
    def def_extra(self) -> float:
        """防御力加成"""
        return self.defend - self.def_base

    def get_elem_dmg(self, prop) -> float:
        elem_dict = {
            "物理伤害加成": self.phy_dmg_bonus,
            "火元素伤害加成": self.pyro_dmg_bonus,
            "雷元素伤害加成": self.electro_dmg_bonus,
            "水元素伤害加成": self.hydro_dmg_bonus,
            "草元素伤害加成": self.dendro_dmg_bonus,
            "风元素伤害加成": self.anemo_dmg_bonus,
            "岩元素伤害加成": self.geo_dmg_bonus,
            "冰元素伤害加成": self.cryo_dmg_bonus,
        }
        return elem_dict[prop]


class PropertySlot(BaseModel):
    """
    词条
    """

    name: str
    """词条名"""
    value: float
    """数值"""

    @property
    def prop(self) -> str:
        """用于计算和表示"""
        if any(i in self.name for i in ["PERCENT", "ADD", "CHARGE", "CRITICAL"]):
            return str(self.value) + "%"
        else:
            return str(int(self.value))


class Weapon(BaseModel):
    """
    武器信息
    """

    name: str
    """武器名称"""
    icon: str
    """武器图标"""
    affix: int
    """武器精炼等级"""
    level: int
    """武器等级"""
    rank: int
    """武器稀有度"""


class Relic(BaseModel):
    """
    圣遗物信息
    """

    name: str
    """名称"""
    slot: str
    """部位"""
    set: str
    """所属套装"""
    level: int
    """圣遗物等级"""
    icon: str
    """圣遗物图标"""
    main_stat: PropertySlot
    """主属性"""
    sub_stat_list: List[PropertySlot]
    """副属性"""
    rank: int
    """稀有度"""
    score: Optional[float] = None
    """圣遗物评分"""


class Relicset(BaseModel):
    """
    圣遗物套装信息
    """

    flower: Optional[Relic] = None
    """生之花"""
    plume: Optional[Relic] = None
    """死之羽"""
    sands: Optional[Relic] = None
    """时之沙"""
    goblet: Optional[Relic] = None
    """空之杯"""
    circlet: Optional[Relic] = None
    """理之冠"""

    @property
    def set_info(self) -> dict:
        """套装信息"""
        dic = {}
        for slot in [self.flower, self.plume, self.sands, self.goblet, self.circlet]:
            if (item := slot) is not None:
                setname: str = item.set
                dic[setname] = dic.setdefault(setname, 0) + 1
        return dic

    @property
    def total_score(self) -> float:
        """圣遗物总分"""
        score = 0
        for slot in [self.flower, self.plume, self.sands, self.goblet, self.circlet]:
            if (item := slot) is not None:
                score += item.score if item.score else 0
        return score


# 以下用于计算
class CalcProp(BaseModel):
    """基础属性（三围）"""

    hp_base: float = 0
    """基础生命值"""
    hp: float = 0
    """生命值上限"""
    atk_base: float = 0
    """基础攻击力"""
    atk: float = 0
    """攻击力"""
    def_base: float = 0
    """基础防御力"""
    defend: float = 0
    """防御力"""

    def __add__(self, other: "PropBuff"):
        return CalcProp(
            hp_base=self.hp_base,
            atk_base=self.atk_base,
            def_base=self.def_base,
            hp=self.hp + other.hp_fix + self.hp_base * other.hp_percent,
            atk=self.atk + other.atk_fix + self.atk_base * other.atk_percent,
            defend=self.defend + other.def_fix + self.def_base * other.def_percent,
        )


class PropTensor(BaseModel):
    hp: float
    atk: float
    defend: float
    elem_mastery: float
    crit_rate: float
    crit_dmg: float
    recharge: float
    dmg_bonus: float
    healing: float


class Multiplier(BaseModel):
    """倍率"""

    atk: float = 0
    """基于攻击"""
    hp: float = 0
    """基于生命"""
    defend: float = 0
    """基于防御"""
    em: float = 0
    """基于精通"""

    def __add__(self, other: "Multiplier"):
        return Multiplier(
            atk=self.atk + other.atk,
            hp=self.hp + other.hp,
            defend=self.defend + other.defend,
            em=self.em + other.em,
        )


class PropBuff(BaseModel):
    hp_percent: float = 0
    hp_fix: float = 0
    atk_percent: float = 0
    atk_fix: float = 0
    def_percent: float = 0
    def_fix: float = 0

    def __add__(self, other: "PropBuff"):
        return PropBuff(
            hp_percent=self.hp_percent + other.hp_percent,
            hp_fix=self.hp_fix + other.hp_fix,
            atk_percent=self.atk_percent + other.atk_percent,
            atk_fix=self.atk_fix + other.atk_fix,
            def_percent=self.def_percent + other.def_percent,
            def_fix=self.def_fix + other.def_fix,
        )


class FixValue(BaseModel):
    """"""

    dmg: float = 0
    heal: float = 0
    shield: float = 0

    def __add__(self, other: "FixValue"):
        return FixValue(
            dmg=self.dmg + other.dmg,
            heal=self.heal + other.heal,
            shield=self.shield + other.shield,
        )


class TransMat(BaseModel):
    """
    转移矩阵
        0-生命值    1-攻击力    2-防御力
        3-精通      4-暴击      5-暴伤
        6-充能      7-增伤      8-治疗
    """

    class Config:
        arbitrary_types_allowed = True

    mask: np.ndarray = Field(default_factory=lambda: 0)
    """阈值矩阵"""
    t_mat: np.ndarray = Field(default_factory=lambda: 0)
    """属性转移矩阵"""

    def __add__(self, other: "TransMat"):
        if np.allclose(self.mask, other.mask):
            return TransMat(mask=self.mask, t_mat=self.t_mat + other.t_mat)
        else:
            raise ValueError("阈值矩阵不同，相加失败")


class TransMatList(List[TransMat]):
    """"""

    def __init__(self, inputs: list[TransMat] = [TransMat()]):
        super().__init__(inputs)

    def __add__(self, other: "TransMatList"):
        output = self.copy()
        adder = other.copy()
        for i, m_pair in enumerate(output):
            for j, m_add in enumerate(adder):
                if np.allclose(m_pair.mask, m_add.mask):
                    del output[i]
                    del adder[j]
                    output.append(m_pair + m_add)
                else:
                    output.append(m_add)
        return TransMatList(output)


class DmgInfo(BaseModel):
    """"""

    index: int
    dsc: str
    exp_hit: int
    crit_hit: int = 0


class DmgSetting(BaseModel):
    index: int
    dsc: str = ""
    weight: float


class Buff(BaseModel):
    """增益器"""

    name: str = ""
    """增益名"""
    dsc: str = ""
    """增益描述"""
    value_type: Union[List[str], str] = "ALL"
    """伤害加成类型：
        NA-普通攻击\\
        CA-重击\\
        PA-下落攻击\\
        A-普通攻击/重击/下落攻击\\
        E-元素战技\\
        Q-元素爆发\\
        H-治疗\\
        S-护盾\\
        ALL-所有类型\\
    """
    elem_type: Union[str, List[str]] = "all"
    """伤害元素类型：\\
        phy-物理\\
        pyro-火属性\\
        electro-雷属性\\
        hydro-水属性\\
        dendro-草属性\\
        anemo-风属性\\
        geo-岩属性\\
        cryo-冰属性\\
        all-所有类型\\
        elem-元素增伤
    """
    member_type: Union[str, List[str]] = "self"
    """成员加成类型：\\
        self-自身\\
        party-其余友方成员\\
        all-全部队伍成员\\
        active-场上角色\\
        off field-后台角色
    """
    reaction_type: Union[str, List[str]] = ""
    """元素反应类型：\\
        剧变："燃烧", "超导", "扩散", "感电", "碎冰", "超载", "原绽放", "烈绽放", "超绽放", "结晶"\\
        增幅："火蒸发", "冰融化", "水蒸发", "火融化", "蔓激化", "超激化"
    """
    basic_prop: PropBuff = PropBuff()
    """攻击/生命/防御增益"""
    mutiplier: Multiplier = Multiplier()
    """倍率增益"""
    crit_rate: float = 0
    """暴击增益"""
    crit_dmg: float = 0
    """暴伤增益"""
    elem_mastery: float = 0
    """精通增益"""
    recharge: float = 0
    """"""
    dmg_bonus: DMGBonus = DMGBonus()
    """"""
    healing: float = 0
    """"""
    resist_reduction: float = 0
    """"""
    def_reduction: float = 0
    """"""
    def_piercing: float = 0
    """"""
    fix_value: FixValue = FixValue()
    """"""
    reaction_coeff: float = 0
    """"""
    trans_matrix_list: TransMatList = TransMatList()
    """"""

    def __add__(self, other: "Buff"):

        if (
            self.value_type == other.value_type
            and self.elem_type == other.elem_type
            and self.member_type == other.member_type
            and self.reaction_type == other.reaction_type
        ):
            return Buff(
                value_type=self.value_type,
                elem_type=self.elem_type,
                member_type=self.member_type,
                reaction_type=self.reaction_type,
                basic_prop=self.basic_prop + other.basic_prop,
                mutiplier=self.mutiplier + other.mutiplier,
                crit_rate=self.crit_rate + other.crit_rate,
                crit_dmg=self.crit_dmg + other.crit_dmg,
                elem_mastery=self.elem_mastery + other.elem_mastery,
                recharge=self.recharge + other.recharge,
                dmg_bonus=self.dmg_bonus + other.dmg_bonus,
                healing=self.healing + other.healing,
                resist_reduction=self.resist_reduction + other.resist_reduction,
                def_reduction=self.def_reduction + other.def_reduction,
                def_piercing=self.def_piercing + other.def_piercing,
                fix_value=self.fix_value + other.fix_value,
                reaction_coeff=self.reaction_coeff + other.reaction_coeff,
                trans_matrix_list=self.trans_matrix_list + other.trans_matrix_list,
            )
        else:
            raise ValueError("Buff不兼容，不可相加")


class BuffSetting(BaseModel):
    """
    增益设置
    """

    name: str = ""
    """"""
    dsc: str = ""
    """描述"""
    label: int = 0
    """设置"""
    state: list = []


class BuffList(BaseModel):
    """增益列表"""

    source: str = ""
    """增益来源"""
    is_from_party: bool = False
    """是否为友方增益"""
    buff: List[Buff] = []
    """增益器列表"""
    setting: List[BuffSetting] = []
    """增益器设置列表"""


class Role(BaseModel):
    """
    角色
    """

    name: str
    """角色名"""
    scaling_table: Optional[List[SkillMultiplier]] = None
    """技能倍率表"""
    talent: Optional[PropInfo] = None
    """角色属性信息"""
    fight_prop: Optional[FightProp] = None
    """角色面板信息"""
    weapon: Optional[Weapon] = None
    """角色武器信息"""
    artifacts: Optional[Relicset] = None
    """角色圣遗物信息"""
    buff_list: Optional[List[BuffList]] = None
    """增益表"""
    dmg_setting: Optional[List[DmgSetting]] = None
    """伤害设置信息"""
    damage: Optional[List[DmgInfo]] = None
    """伤害信息"""