import json
from typing import Literal, Optional, Union

from pydantic import BaseModel, parse_raw_as

# 以下用于数据获取存储


class EnkaInfo(BaseModel):
    """
    ENKA.network 获取的信息
    """

    uid: str
    """玩家uid"""
    playerInfo: dict = {}
    """玩家信息"""
    avatarInfoList: list = []
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
    multiplier: list[float] = []
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
    scaling_table: Optional[list[SkillMultiplier]] = None
    """技能倍率表"""
    skill_order: list[int]
    """天赋表"""
    energy_cost: int
    """元素爆发能量"""
    proud_map: dict = {}
    """命座天赋加成"""
    extra_info: Optional[dict] = None
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

    def get_skill(self, key):
        if "A" in key:
            return self.skill_A
        if "E" in key:
            return self.skill_E
        if "Q" in key:
            return self.skill_Q
        else:
            return 0


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
        )

    def __getitem__(self, key: str):
        return eval(f"self.{key.lower()}")

    def set(self, key, value):
        if key == "phy":
            self.phy = value
        elif key == "pyro":
            self.pyro = value
        elif key == "electro":
            self.electro = value
        elif key == "hydro":
            self.hydro = value
        elif key == "dendro":
            self.dendro = value
        elif key == "anemo":
            self.anemo = value
        elif key == "geo":
            self.geo = value
        elif key == "cryo":
            self.cryo = value
        return self


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
        if any(i == self.name for i in ["攻击力", "生命值", "防御力", "元素精通"]):
            return "+" + str(int(self.value))
        else:
            return "+" + str(self.value) + "%"


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
    type: str
    """部位"""
    set: str
    """所属套装"""
    level: int
    """圣遗物等级"""
    icon: str
    """圣遗物图标"""
    main_stat: PropertySlot
    """主属性"""
    sub_stat_list: list[PropertySlot]
    """副属性"""
    rank: int
    """稀有度"""


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
    def set_info(self):
        """套装信息"""
        dic: dict[str, int] = {}
        for slot in [self.flower, self.plume, self.sands, self.goblet, self.circlet]:
            if (item := slot) is not None:
                setname: str = item.set
                dic[setname] = dic.setdefault(setname, 0) + 1
        return dic

    def get_item(self, key="total"):
        if key == "flower":
            return self.flower
        if key == "plume":
            return self.plume
        if key == "sands":
            return self.sands
        if key == "goblet":
            return self.goblet
        if key == "circlet":
            return self.circlet
        else:
            return self.set_info


# 以下用于计算
class RelicScore(BaseModel):
    """
    圣遗物评分
    """

    flower: float = -1
    """生之花"""
    plume: float = -1
    """死之羽"""
    sands: float = -1
    """时之沙"""
    goblet: float = -1
    """空之杯"""
    circlet: float = -1
    """理之冠"""

    @property
    def total_score(self) -> float:
        """圣遗物总分"""
        score = 0
        for s in [self.flower, self.plume, self.sands, self.goblet, self.circlet]:
            score += s if s else 0
        return score

    def get_score(self, key="total"):
        if key == "flower":
            return self.flower
        if key == "plume":
            return self.plume
        if key == "sands":
            return self.sands
        if key == "goblet":
            return self.goblet
        if key == "circlet":
            return self.circlet
        else:
            return self.total_score

    def set_score(self, key, value):
        if key == "flower":
            self.flower = value
        if key == "plume":
            self.plume = value
        if key == "sands":
            self.sands = value
        if key == "goblet":
            self.goblet = value
        if key == "circlet":
            self.circlet = value


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


class PoFValue(BaseModel):
    percent: float = 0
    fix: float = 0

    def __add__(self, other: "PoFValue"):
        return PoFValue(
            percent=self.percent + other.percent,
            fix=self.fix + other.fix,
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


class Buff(BaseModel):
    """增益器"""

    dsc: str = ""
    """增益描述"""
    target: Union[list[str], str] = "ALL"
    """增益目标：\\
        NA-普通攻击\\
        CA-重击\\
        PA-下落攻击\\
        E-元素战技\\
        Q-元素爆发\\
        ALL-所有类型\\
        H-治疗\\
        S-护盾
    """
    elem_type: Union[str, list[str]] = "all"
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
    triger_type: str = "all"
    """触发类型：\\
        all-均可触发或无关\\
        active-场上触发\\
        off field-后台触发
    """
    reaction_type: Union[str, list[str]] = ""
    """元素反应类型：\\
        剧变："燃烧", "超导", "扩散", "感电", "碎冰", "超载", "原绽放", "烈绽放", "超绽放", "结晶"\\
        增幅："火蒸发", "冰融化", "水蒸发", "火融化", "蔓激化", "超激化"
    """
    hp: PoFValue = PoFValue()
    """生命增益"""
    atk: PoFValue = PoFValue()
    """攻击增益"""
    defend: PoFValue = PoFValue()
    """防御增益"""
    mutiplier: Multiplier = Multiplier()
    """倍率增益"""
    crit_rate: float = 0
    """暴击增益"""
    crit_dmg: float = 0
    """暴伤增益"""
    elem_mastery: float = 0
    """精通增益"""
    recharge: float = 0
    """充能增益"""
    elem_dmg_bonus: DMGBonus = DMGBonus()
    """元素伤害加成增益"""
    healing: float = 0
    """治疗加成增益"""
    dmg_bonus: float = 0
    """增伤增益"""
    resist_reduction: float = 0
    """减抗"""
    def_reduction: float = 0
    """减防"""
    def_piercing: float = 0
    """无视防御"""
    fix_value: FixValue = FixValue()
    """固值加成"""
    reaction_coeff: float = 0
    """反应系数增益"""


class BuffSetting(BaseModel):
    """
    增益设置
    """

    dsc: str = "此增益为常驻增益"
    """描述"""
    label: str = ""
    """设置"""
    state: str = "-"


class BuffInfo(BaseModel):
    """增益列表"""

    source: str = ""
    """增益来源"""
    name: str = ""
    """增益名"""
    buff_range: str = "self"
    """加成范围：\\
        self-自身\\
        party-其余友方成员\\
        all-全部队伍成员
    """
    buff_type: str = "dmgbuff"
    """增益类型：\\
            propbuff-面板型增益
            transbuff-转移型增益
            dmgbuff-伤害型增益
    """
    # from_party_member: str = ""
    # """友方增益来源"""
    buff: Optional[Buff] = None
    """增益器"""
    setting: BuffSetting = BuffSetting()
    """增益器设置"""


class DMG(BaseModel):
    """"""

    index: int
    """序号"""
    source: str = ""
    """数值来源"""
    name: str = ""
    """技能名称"""
    type: str = "D"
    """类型：
        D：伤害
        H：治疗
        S：护盾
    """
    dsc: str = ""
    """描述"""
    exp_value: int = 0
    """"""
    crit_value: int = 0
    """"""
    weight: int = 0
    """权重 -1-10"""


class Role(BaseModel):
    """
    角色
    """

    name: str = ""
    """角色名"""
    scaling_table: Optional[list[SkillMultiplier]] = None
    """技能倍率表"""
    info: Optional[PropInfo] = None
    """角色杂项信息"""
    fight_prop: Optional[FightProp] = None
    """角色面板信息"""
    weapon: Optional[Weapon] = None
    """角色武器信息"""
    artifacts: Optional[Relicset] = None
    """角色圣遗物信息"""
    scores: Optional[RelicScore] = None
    """圣遗物评分"""
    party_member: list[str] = []
    """队友"""
    buff_list: list[BuffInfo] = []
    """增益表"""
    # dmg_setting: list[DmgSetting] = []
    # """伤害设置信息"""
    dmg_list: list[DMG] = []
    """伤害信息"""


class BuffList(BaseModel):
    @classmethod
    def encoder(cls, models: list["BuffInfo"]):
        return json.dumps(models, default=cls.dict)

    @classmethod
    def decoder(cls, json_data):
        return parse_raw_as(list[BuffInfo], json_data)


class DMGList(BaseModel):
    @classmethod
    def encoder(cls, models: list["DMG"]):
        return json.dumps(models, default=cls.dict)

    @classmethod
    def decoder(cls, json_data):
        return parse_raw_as(list[DMG], json_data)
