from Nahidabot.database.models import Player, PropList, RoleBasicInfo
from Nahidabot.utils.classmodel import BuffInfo, Role, RoleInfo

from .dmg_model import DMGCalc
from .relics import artifacts, artifacts_setting
from .role import role_buff, role_dmg
from .weapon import weapon_buff


class RoleModel(Role):
    """角色计算模型"""

    propbuff: list[BuffInfo] = []
    """面板型增益"""
    transbuff: list[BuffInfo] = []
    """转移型增益"""
    dmgbuff: list[BuffInfo] = []
    """伤害型增益"""

    async def update_from_database(self, user_qq):
        """从数据库更新"""
        (uid,) = await Player.filter(user_qq=user_qq, is_main_uid=True).values_list(
            "uid", flat=True
        )

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
        self.buff_list = roleinfo.buff_info  # type: ignore

    async def get_buff(self):
        """获取角色增益"""
        # 命座、天赋和技能增益
        self.buff_list.extend(await role_buff(self))
        # 武器增益
        self.buff_list.extend(await weapon_buff(self))
        # 圣遗物增益
        self.buff_list.extend(await relic_buff(self))

    async def get_dmg(self):
        self.damage = await role_dmg(self)
        pass

    @property
    def calculator(self):
        """战斗实时面板"""
        return (
            DMGCalc(self.fight_prop, self.talent.level)
            + self.propbuff
            + self.transbuff
            + self.dmgbuff
        )

    async def setting(self) -> list[BuffInfo]:
        """获取增益设置"""
        return []

    async def buff(self) -> list[BuffInfo]:
        """获取增益"""
        return []

    async def get_setting(self):
        """获取增益设定"""
        await self.setting()
        await artifacts_setting(self.artifacts, self.buff_list)

    def get_buff(self):
        """"""

    def get_dmg(self):
        """"""
