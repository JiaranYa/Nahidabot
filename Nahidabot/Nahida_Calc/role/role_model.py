from Nahidabot.database.models import Player, PropList, RoleBasicInfo
from Nahidabot.utils.classmodel import BuffInfo, Role, RoleInfo

from ..dmg_model import DMGCalc
from ..relics import artifacts, artifacts_setting

# from .role import role_buff, role_dmg
from ..weapon import weapon_buff, weapon_setting


class RoleModel(Role):
    """角色计算模型"""

    propbuff: list[BuffInfo] = []
    """面板型增益"""
    transbuff: list[BuffInfo] = []
    """转移型增益"""
    dmgbuff: list[BuffInfo] = []
    """伤害型增益"""

    async def update_from_database(self, user_qq, uid):
        """从数据库更新"""

        basicinfo: RoleInfo
        (basicinfo,) = await RoleBasicInfo.filter(name=self.name).values_list(
            "info", flat=True
        )
        self.scaling_table = basicinfo.scaling_table

        (roleinfo,) = await PropList.filter(
            user_qq=user_qq, uid=uid, role_name=self.name
        ).all()
        self.talent = roleinfo.talent  # type: ignore
        self.fight_prop = roleinfo.property  # type: ignore
        self.weapon = roleinfo.weapon  # type: ignore
        self.artifacts = roleinfo.artifacts  # type: ignore
        self.party_member = roleinfo.party_member  # type: ignore
        self.buff_list = roleinfo.buff_info  # type: ignore

    @property
    def calculator(self):
        """战斗实时面板"""
        if self.fight_prop is None or self.talent is None:
            return 0
        return (
            DMGCalc(self.fight_prop, self.talent.level)
            + self.propbuff
            + self.transbuff
            + self.dmgbuff
        )

    async def setting(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """获取增益设置"""
        return []

    async def buff(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """获取增益"""
        return []

    async def get_setting(self):
        """获取增益设定"""
        buff_list = self.buff_list.copy()
        self.buff_list = []
        self.buff_list.extend(await self.setting(buff_list))
        self.buff_list.extend(await weapon_setting(self.weapon, self.talent, buff_list))
        self.buff_list.extend(await artifacts_setting(self.artifacts, buff_list))

    async def get_buff(self, mode: str):
        """获取角色增益"""
        # 命座、天赋和技能增益
        input_buff: list[BuffInfo] = []
        for buff in self.buff_list:
            if buff.buff_type == mode:
                input_buff.append(buff)
        # 自身增益
        await self.buff(input_buff)
        # 武器增益
        await weapon_buff(input_buff, self.talent, self.calculator)
        # 圣遗物增益
        await artifacts(input_buff, self.talent, self.calculator)

        if mode == "propbuff":
            self.propbuff.extend(input_buff)
        elif mode == "transbuff":
            self.transbuff.extend(input_buff)
        else:
            self.dmgbuff.extend(input_buff)

        output_buff: list[BuffInfo] = []
        for buff in input_buff:
            if buff.range != "self":
                output_buff.append(buff)
        return output_buff

    async def save_buff(self):
        output: list[BuffInfo] = []
        output.extend(self.propbuff)
        output.extend(self.transbuff)
        output.extend(self.dmgbuff)
        return output

    async def get_partner(self):
        """"""
        return self.party_member

    async def load_buff(self, input_buff: list[BuffInfo], mode: str):
        """"""
        partner_buff = []
        for buff in input_buff:
            if self.name not in buff.source:
                partner_buff.append(buff)

        if mode == "propbuff":
            self.propbuff.extend(partner_buff)
        elif mode == "transbuff":
            self.transbuff.extend(partner_buff)
        else:
            self.dmgbuff.extend(partner_buff)

    async def get_dmg(self):
        # self.damage = await role_dmg(self)
        pass
