from Nahidabot.database.models import Player, PropList, RoleBasicInfo
from Nahidabot.utils.classmodel import Role, RoleInfo

from .relics import relic_buff
from .role import role_buff, role_dmg
from .weapon import weapon_buff


class RoleModel(Role):
    """角色计算模型"""

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
