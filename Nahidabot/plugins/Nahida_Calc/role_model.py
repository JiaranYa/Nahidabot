from Nahidabot.database.models import PropList, RoleBasicInfo
from Nahidabot.utils.classmodel import Role

from .role import buff_info, dmg_info


class RoleModel:
    """角色计算模型"""

    def __init__(self, role: Role) -> None:
        self.name = role.name
        if role:
            scaling_table
        self.scaling_table

    def get_dmg(self):
        return dmg_info(self.prop)

    def create_buff(self):
        return buff_info(self.prop)
