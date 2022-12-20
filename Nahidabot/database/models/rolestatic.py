from pathlib import WindowsPath

from tortoise import fields
from tortoise.models import Model

from Nahidabot.utils.classmodel import RoleInfo, SkillMultiplier
from Nahidabot.utils.file import load_json
from Nahidabot.utils.path import STATIC_PATH

ROLE_TABLE_PATH = STATIC_PATH / "roletable.json"
SCALING_TABLE_PATH = STATIC_PATH / "scaling_table"


class RoleBasicInfo(Model):
    """不随玩家变化的角色信息"""

    index = fields.IntField(pk=True, generated=True, auto_increment=True)
    aid = fields.CharField(max_length=8, unique=True)
    """角色id"""
    name = fields.CharField(max_length=16, unique=True, null=True)
    info = fields.JSONField(
        encoder=RoleInfo.json, decoder=RoleInfo.parse_raw, null=True
    )
    """基础信息"""

    class Meta:
        table = "basic_role_info"
        table_description = "角色信息表"

    @classmethod
    async def update_infotable(cls):
        role_table: dict[str, dict] = load_json(ROLE_TABLE_PATH)
        for key, value in role_table.items():
            roleinfo = RoleInfo(
                name=value.get("Name", ""),
                weapon_type=value.get("WeaponType", ""),
                elem_type=value.get("ElemType", ""),
                region=value.get("Region", ""),
                abbr=value.get("Abbr", ""),
                energy_cost=value.get("EnergyCost", 0),
                skill_order=value.get("SkillOrder", []),
                proud_map=value.get("ProudMap", {}),
                extra_info=value.get("Extra"),
            )

            path: WindowsPath = SCALING_TABLE_PATH / (value["Abbr"] + ".json")
            if path.is_file():
                scaling_table = load_json(path)
                ((_, contents),) = scaling_table.items()
                multiplier_table_list = []
                for index, cont in enumerate(contents):
                    multiplier_table_list.append(
                        SkillMultiplier(
                            skillindex=index + 1,
                            dsc=cont["dsc"],
                            multiplier=cont["table"],
                        )
                    )
                roleinfo.scaling_table = multiplier_table_list

            role, _ = await cls.get_or_create(aid=key)
            role.name = value["Name"]
            role.info = roleinfo
            await role.save()
