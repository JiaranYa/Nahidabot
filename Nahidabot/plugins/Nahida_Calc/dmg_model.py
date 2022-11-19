from Nahidabot.utils.file import load_json
import asyncio

factor_map = asyncio.run(load_json(path="./base_factor.json"))

class DMGCalc(object):
    """
    伤害计算器
    """    
    def __init__(self,level=90,
                    baseprop=0,
                    mutiplier=0,
                    crit_rate=0,
                    crit_dmg=0,
                    elem_mastary=0,
                    dmg_bonus=0,
                    healing=0,
                    elem_res=0.1,
                    def_res=0,
                    fix_dmg=0,
                    fix_heal=0,
                    fix_shield=0,
                    reaction_factor=1) -> None:
        self.level = level
        """等级"""
        self.baseprop = baseprop
        """基础属性（三围）"""
        self.mutiplier = mutiplier
        """倍率"""
        self.crit_rate = crit_rate
        """暴击率"""
        self.crit_dmg = crit_dmg
        """暴击伤害"""
        self.elem_mastary = elem_mastary
        """元素精通"""
        self.dmg_bonus = dmg_bonus
        """增伤"""
        self.healing = healing
        """治疗"""
        self.elem_resistance = elem_res
        """元素抗性"""
        self.def_resistance = def_res
        """防御抗性"""
        self.fix_dmg = fix_dmg
        """固定伤害"""
        self.fix_heal = fix_heal
        """固定治疗"""
        self.fix_shield = fix_shield
        """固定盾量"""
        self.factor = reaction_factor
        """反应系数加成"""

    def buff(self,extra_baseprop=0,
                extra_mutiplier=0,
                extra_crit_rate=0,
                extra_crit_dmg=0,
                extra_elem_mastary=0,
                extra_dmg_bonus=0,
                extra_healing=0,
                resist_reduction=0,
                def_reduction=0,
                extra_fixdmg=0,
                extra_fixheal=0,
                extra_shield=0,
                extra_reaction_coeff=0):
        """
        函数：获取增益后的面板数值
        @params: 面板增益数值
        @returns: 新面板数值
        """
        return DMGCalc( level=self.level,
                        baseprop=self.baseprop+extra_baseprop,
                        mutiplier=self.mutiplier+extra_mutiplier,
                        crit_rate=self.crit_rate+extra_crit_rate,
                        crit_dmg=self.crit_dmg+extra_crit_dmg,
                        elem_mastary=self.elem_mastary+extra_elem_mastary,
                        dmg_bonus=self.dmg_bonus+extra_dmg_bonus,
                        healing=self.healing+extra_healing,
                        elem_res=self.elem_resistance+resist_reduction,
                        def_res=self.def_resistance+def_reduction,
                        fix_dmg=self.fix_dmg+extra_fixdmg,
                        fix_heal=self.fix_heal+extra_fixheal,
                        fix_shield=self.fix_shield+extra_shield,
                        reaction_factor=self.factor+extra_reaction_coeff)

    @property
    def base_dmg_zone(self):
        """基础伤害乘区"""
        return self.baseprop*self.mutiplier + self.fix_dmg

    @property
    def dmg_bonus_zone(self):
        """增伤区"""
        return 1 + self.dmg_bonus

    @property
    def expectation_hit_zone(self):
        """暴击期望区"""
        return 1+min(max(self.crit_rate,0),1)*self.crit_dmg

    @property
    def crit_hit_zone(self):
        """必定暴击"""
        return 1+self.crit_dmg

    @property
    def elem_res_zone(self):
        """抗性区"""
        if elem_res:=self.elem_resistance<0:
            return 1-elem_res/2
        elif elem_res<=0.75:
            return 1-elem_res
        else:
            return 1/(1+elem_res*4)

    @property
    def def_res_zone(self):
        """防御区"""
        return (90+100)/((self.level+100)+(1+self.def_resistance)*(90+100))
               
    
    def get_dmg(self,mode)->float:
        """
        非反应伤害计算器
        @params:
            mode:   "exp":期望伤害
                    "crit":暴击伤害
                    "":无暴击
        """
        if mode == "exp": crit_zone = self.expectation_hit_zone
        elif mode == "crit": crit_zone = self.crit_hit_zone
        else: crit_zone = 1

        return self.base_dmg_zone * self.dmg_bonus_zone * self.elem_res_zone * self.def_res_zone * crit_zone

    def get_amp_reac_dmg(self,mode,reaction_type = ""):
        """
        增幅反应伤害
        Amplifying Reactions
        """
        if reaction_type in ["火蒸发","冰融化"]:
            return 1.5*(1+self.factor+2.78*self.elem_mastary/(self.elem_mastary+1400)) * self.get_dmg(mode)
        elif reaction_type in ["水蒸发","火融化"]:
            return 2*(1+self.factor+2.78*self.elem_mastary/(self.elem_mastary+1400)) * self.get_dmg(mode)
        elif reaction_type in ["蔓激化"]:
            reaction_coeff =  factor_map["TransReac"][self.level] * 1.25 *(1+5*self.elem_mastary/
                                                                (self.elem_mastary+1200)+self.factor)
            return self.buff(extra_fixdmg=reaction_coeff).get_dmg(mode=mode)
        elif reaction_type in ["超激化"]:
            reaction_coeff =  factor_map["TransReac"][self.level] * 1.15 *(1+5*self.elem_mastary/
                                                                (self.elem_mastary+1200)+self.factor)
            return self.buff(extra_fixdmg=reaction_coeff).get_dmg(mode=mode)
        else: 
            print("错误调用get_amp_reac_dmg，这不是增幅反应")
            return self.get_dmg(mode)
            

    def get_trans_reac_dmg(self,reaction_type = ""):
        """
        剧变反应伤害
        Transformative Reactions
        """
        factor_list = {
            "燃烧":0.25,
            "超导":0.5,
            "扩散":0.6,
            "感电":1.2,
            "碎冰":1.5,
            "超载":2,
            "原绽放":2,
            "烈绽放":3,
            "超绽放":3,
        }
        if reaction_type in factor_list.keys():
            return factor_list[reaction_type] * factor_map["TransReac"][self.level] * (1+self.factor+16*self.elem_mastary/
                                                                                                    (self.elem_mastary+2000))
    def get_crystall_shield(self):
        """结晶盾"""
        return factor_map["Cryst"][self.level]*(1+4.44*self.elem_mastary/(self.elem_mastary+1400))

    def get_healing(self):
        """治疗量"""
        return (self.baseprop*self.mutiplier + self.fix_heal)*self.healing

    def get_shield(self):
        """盾量"""
        return self.baseprop*self.mutiplier + self.fix_shield

class Buffer(object):
    pass