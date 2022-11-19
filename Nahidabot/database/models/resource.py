from pathlib import WindowsPath
from tortoise import fields
from tortoise.models import Model
from Nahidabot.utils.file import load_json
from Nahidabot.utils.path import STATIC_PATH
from Nahidabot.utils.classmodel import RoleInfo,SkillMultiplier

ROLE_TABLE_PATH = STATIC_PATH / "roletable.json"
SCALING_TABLE_PATH = STATIC_PATH / "scaling_table"

class RoleBasicInfo(Model):
    index = fields.IntField(pk=True, generated=True, auto_increment=True)
    # 角色id
    aid = fields.CharField(max_length=8,unique=True)
    # 基础信息
    info = fields.JSONField(encoder=RoleInfo.json,
                            decoder=RoleInfo.parse_raw,null=True)

    class Meta:
        table = "basic_role_info"
        table_description = "角色信息表"

    @classmethod
    async def update_infotable(cls):
        role_table:dict[str,dict] = await load_json(ROLE_TABLE_PATH)
        for key,value in role_table.items():
            roleinfo = RoleInfo(name=value["Name"],
                                weapon_type=value["WeaponType"],
                                elem_type=value["ElemType"],
                                abbr=value["Abbr"],
                                skill_order=value.get("SkillOrder",[]),
                                proud_map=value.get("ProudMap",{}),
                                extra_info = value.get("Extra"))

            path:WindowsPath = SCALING_TABLE_PATH / (value["Abbr"]+".json")
            if path.is_file():
                scaling_table = await load_json(path)
                (_,contents), = scaling_table.items()
                multiplier_table_list = []
                for index,cont in enumerate(contents):
                    multiplier_table_list.append(SkillMultiplier(skillindex=index+1,
                                                                dsc=cont["dsc"],
                                                                multiplier=cont["table"]))
                roleinfo.scaling_table = multiplier_table_list

            role,_ = await cls.get_or_create(aid=key)
            role.info = roleinfo
            await role.save()
