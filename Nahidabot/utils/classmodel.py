from typing import Optional, List, Dict, Literal
from pydantic import BaseModel

class EnkaInfo(BaseModel):
    """
    ENKA.network 获取的信息
    """
    uid:str
    """玩家uid"""
    playerInfo:Optional[Dict] = None
    """玩家信息"""
    avatarInfoList:Optional[List] = None
    """角色列表"""

class PlayerInfo(BaseModel):
    """
    玩家信息
    """
    uid:str
    """原神uid"""
    nickname:Optional[str]
    """玩家昵称"""
    level:int
    """玩家等级"""
    profile_id:Optional[int]
    """玩家头像"""
    namecard_id:Optional[int]
    """卡片id"""
    signature:Optional[str]
    """签名"""

class SkillMultiplier(BaseModel):
    """
    技能倍率
    """
    skillindex: int = 0
    """技能序号"""
    dsc:str = ""
    """技能描述"""
    multiplier:List[float] = []
    """等级倍率表"""

class RoleInfo(BaseModel):
    """
    角色的基础信息
    """
    name:str=""
    """角色名"""
    weapon_type:Literal["单手剑","弓","长柄","双手剑","法器"]
    """武器类型"""
    elem_type:Literal["Fire","Elec","Water","Grass","Wind","Rock","Ice",""]
    """元素类型"""
    abbr:str=""
    """缩写"""
    scaling_table:Optional[List[SkillMultiplier]] = None
    """技能倍率表"""
    skill_order:List[int] 
    """天赋表"""
    proud_map:dict = {}
    """命座天赋加成"""
    extra_info:Optional[Dict] = None
    """额外信息"""
    
class Talent(BaseModel):
    """
    角色能力信息
    """
    level:int
    """等级"""
    element:str
    """神之眼"""
    fetter:int
    """好感度"""
    weapon_type:Literal["单手剑","弓","长柄","双手剑","法器"]
    """武器类型"""
    abbr:str
    """简称"""
    constellation:int
    """命座数"""
    skill_A:int
    """普攻等级"""
    skill_E:int
    """元素战技等级"""
    skill_Q:int
    """元素爆发等级"""
    skill_E_prod:int=0
    """元素战技加成"""
    skill_Q_prod:int=0
    """元素爆发加成"""

    @property
    def skill_icon(self)-> list[str]: 
        dict = {
            "单手剑":"01",
            "弓":"02",
            "长柄":"03",
            "双手剑":"04",
            "法器":"05"
        }
        return [f"Skill_A_{dict[self.weapon_type]}.png",
                f"Skill_E_{self.abbr}.png",
                f"Skill_Q_{self.abbr}.png"]

class FightProp(BaseModel):
    """
    面板属性
    """
    hp_base:float
    """基础生命值"""
    hp:float
    """生命值上限"""
    atk_base:float
    """基础攻击力"""   
    atk:float
    """攻击力"""  
    def_base:float
    """基础防御力"""
    defend:float
    """防御力"""
    crit_rate:float
    """暴击率"""
    crit_dmg:float
    """暴击伤害"""
    elemental_mastery:float
    """元素精通"""
    recharge:float
    """元素充能效率"""
    healing:float
    """治疗加成"""
    phy_dmg_bonus:float
    """物理伤害加成"""
    pyro_dmg_bonus:float         
    """火元素伤害加成"""          
    electro_dmg_bonus:float      
    """雷元素伤害加成""" 
    hydro_dmg_bonus:float        
    """水元素伤害加成""" 
    dendro_dmg_bonus:float       
    """草元素伤害加成""" 
    anemo_dmg_bonus:float        
    """风元素伤害加成""" 
    geo_dmg_bonus:float          
    """岩元素伤害加成""" 
    cryo_dmg_bonus:float         
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

    def get_elem_dmg(self,prop) -> float:
        elem_dict = {
            "物理伤害加成"  : self.phy_dmg_bonus,
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
    name:str
    """词条名"""
    value:float
    """数值"""
    @property
    def prop(self)->str:
        """用于计算和表示"""
        if any(i in self.name for i in ["PERCENT","ADD","CHARGE","CRITICAL"]):
            return str(self.value)+"%"
        else: return str(int(self.value))

class Weapon(BaseModel):
    """
    武器信息
    """
    name:str
    """武器名称"""
    icon:str
    """武器图标"""
    affix:int
    """武器精炼等级"""
    level:int
    """武器等级"""
    rank:int
    """武器稀有度"""
    # type:Literal["单手剑","弓","长柄","双手剑","法器"]
    # """武器类型"""

class Relic(BaseModel):
    """
    圣遗物信息
    """
    name:str
    """名称"""
    slot:str
    """部位"""
    set:str
    """所属套装"""
    level:int
    """圣遗物等级"""
    icon:str
    """圣遗物图标"""
    main_stat: PropertySlot
    """主属性"""
    sub_stat_list: List[PropertySlot]
    """副属性"""
    rank:int
    """稀有度"""
    score:Optional[float] = None
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
        dict = {}
        for slot in [self.flower,self.plume,self.sands,self.goblet,self.circlet]:
            if (item:=slot) != None:
                setname:str = item.set
                dict[setname] = dict.setdefault(setname,0) + 1
        return dict

    @property
    def total_score(self) -> float:
        """圣遗物总分"""
        score = 0
        for slot in [self.flower,self.plume,self.sands,self.goblet,self.circlet]:
            if (item:=slot) != None:
                score += item.score if item.score else 0
        return score

class Role(BaseModel):
    """
    角色
    """
    name:str
    """角色名"""
    scaling_table:Optional[List[SkillMultiplier]] = None
    """技能倍率表"""
    talent:Optional[Talent] = None
    """角色属性信息"""
    fight_prop:Optional[FightProp] = None
    """角色面板信息"""
    weapon:Optional[Weapon] = None
    """角色武器信息"""
    artifacts:Optional[Relicset] = None
    """角色圣遗物信息"""
