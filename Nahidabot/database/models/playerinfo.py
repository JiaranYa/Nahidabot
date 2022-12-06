from tortoise import fields
from tortoise.models import Model

from Nahidabot.utils.classmodel import (
    BuffList,
    DMGBonus,
    FightProp,
    PlayerInfo,
    PropertySlot,
    PropInfo,
    Relic,
    RelicScore,
    Relicset,
    RoleInfo,
    Weapon,
)
from Nahidabot.utils.file import load_json
from Nahidabot.utils.path import STATIC_PATH

from .rolestatic import RoleBasicInfo


class Player(Model):
    index = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_qq = fields.CharField(max_length=16, description="qq号")
    uid = fields.CharField(max_length=9, description="原神uid")
    player_info = fields.JSONField(
        encoder=PlayerInfo.json,
        decoder=PlayerInfo.parse_raw,
        description="玩家信息",
        null=True,
    )
    update_time = fields.DatetimeField(auto_now=True, description="最近更新时间")
    is_main_uid = fields.BooleanField(description="是否是主要账号", null=True)

    class Meta:
        table = "player_info"
        table_description = "uid绑定名册"

    @classmethod
    async def insert_or_update(cls, uid: str, data: dict, user_qq: int):
        is_old_user = await cls.exists(user_qq=str(user_qq))
        player, is_new_uid = await cls.get_or_create(user_qq=str(user_qq), uid=uid)
        player.player_info = PlayerInfo(
            uid=uid,
            nickname=data["nickname"],
            level=data["level"],
            profile_id=data["profilePicture"]["avatarId"],
            namecard_id=data["nameCardId"],
            signature=data["signature"],
        )
        if is_new_uid:
            player.is_main_uid = False if is_old_user else True
        await player.save()


class PropList(Model):
    index = fields.IntField(pk=True, generated=True, auto_increment=True)
    user_qq = fields.CharField(max_length=16)
    uid = fields.CharField(max_length=9)
    update_time = fields.DatetimeField(auto_now=True)
    role_name = fields.CharField(max_length=32)
    talent = fields.JSONField(
        encoder=PropInfo.json,
        decoder=PropInfo.parse_raw,
        description="等级，命座和天赋",
        null=True,
    )
    property = fields.JSONField(
        encoder=FightProp.json,
        decoder=FightProp.parse_raw,
        description="面板数值",
        null=True,
    )
    weapon = fields.JSONField(
        encoder=Weapon.json, decoder=Weapon.parse_raw, description="武器", null=True
    )
    artifacts = fields.JSONField(
        encoder=Relicset.json, decoder=Relicset.parse_raw, description="圣遗物", null=True
    )
    scores = fields.JSONField(
        encoder=RelicScore.json,
        decoder=RelicScore.parse_raw,
        description="圣遗物分数",
        null=True,
    )
    buff_info = fields.JSONField(description="增益列表", default=[])
    dmg_info = fields.JSONField(description="伤害数据", default=[])
    dmg_setting = fields.JSONField(description="伤害设置", default=[])

    class Meta:
        table = "role_property"
        table_description = "角色属性信息"

    @classmethod
    async def insert_or_update_role(cls, uid: str, data_list: list[dict], user_qq: str):
        weapon_map = load_json(STATIC_PATH / "weapon.json")
        artifact_map = load_json(STATIC_PATH / "artifact.json")

        for data in data_list:
            role_info: RoleInfo
            (role_info,) = await RoleBasicInfo.filter(
                aid=str(data["avatarId"])
            ).values_list("info", flat=True)
            role_name = role_info.name

            role: PropList
            role, _ = await cls.get_or_create(
                user_qq=user_qq, uid=uid, role_name=role_name
            )
            # 等级，命座和天赋
            skill_list = role_info.skill_order
            elem_type = role_info.elem_type
            abbr = role_info.abbr
            cost = role_info.energy_cost
            proud_map = role_info.proud_map
            if role_name in ["空", "荧"]:
                extrainfo: dict = role_info.extra_info  # type: ignore
                for playertype in extrainfo.values():
                    if data["skillLevelMap"].keys()[0] in playertype["Skillorder"]:
                        skill_list = playertype["SkillOrder"]
                        elem_type = playertype["ElemType"]
                        abbr = "Player" + playertype["ElemType"]
                        cost = playertype["energy_cost"]
                        proud_map = playertype["ProudMap"]
                        break

            role.talent = PropInfo(
                level=int(data["propMap"]["4001"]["val"]),
                ascension=int(data["propMap"]["1002"]["val"]),
                element=elem_type,
                fetter=data.get("fetterInfo", {}).get("expLevel", 0),
                weapon_type=role_info.weapon_type,
                abbr=abbr,
                constellation=len(data["talentIdList"])
                if "talentIdList" in data
                else 0,
                skill_A=data["skillLevelMap"][str(skill_list[0])],
                skill_E_base=data["skillLevelMap"][str(skill_list[1])],
                skill_Q_base=data["skillLevelMap"][str(skill_list[2])],
                Q_cost=cost,
                skill_E_prod=3
                if data.get("proudSkillExtraLevelMap", {}).get(
                    proud_map.get(str(skill_list[1]))
                )
                else 0,
                skill_Q_prod=3
                if data.get("proudSkillExtraLevelMap", {}).get(
                    proud_map.get(str(skill_list[2]))
                )
                else 0,
            )
            # 面板数值
            props = data["fightPropMap"]
            role.property = FightProp(
                hp_base=props["1"],
                hp=props["2000"],
                atk_base=props["4"],
                atk=props["2001"],
                def_base=props["7"],
                defend=props["2002"],
                crit_rate=props["20"],
                crit_dmg=props["22"],
                recharge=props["23"],
                healing=props["26"],
                elemental_mastery=props["28"],
                phy_dmg_bonus=props["30"],
                pyro_dmg_bonus=props["40"],
                electro_dmg_bonus=props["41"],
                hydro_dmg_bonus=props["42"],
                dendro_dmg_bonus=props["43"],
                anemo_dmg_bonus=props["44"],
                geo_dmg_bonus=props["45"],
                cryo_dmg_bonus=props["46"],
            )
            # 武器和圣遗物
            relic_list = Relicset()
            for item in data["equipList"]:
                if item["flat"]["itemType"] == "ITEM_WEAPON":
                    role.weapon = Weapon(
                        name=weapon_map[item["flat"]["nameTextMapHash"]],
                        icon=item["flat"]["icon"],
                        affix=list(item["weapon"]["affixMap"].values())[0] + 1,
                        level=item["weapon"]["level"],
                        rank=item["flat"]["rankLevel"],
                    )
                else:
                    icon = item["flat"]["icon"]
                    main_stat = PropertySlot(
                        name=item["flat"]["reliquaryMainstat"]["mainPropId"],
                        value=item["flat"]["reliquaryMainstat"]["statValue"],
                    )
                    sub_stat_list = []
                    for i in item["flat"]["reliquarySubstats"]:
                        sub_stat_list.append(
                            PropertySlot(name=i["appendPropId"], value=i["statValue"])
                        )

                    temp_relic = Relic(
                        name=artifact_map["Name"][icon],
                        slot=item["flat"]["equipType"],
                        set=artifact_map["SetName"][item["flat"]["setNameTextMapHash"]],
                        level=item["reliquary"]["level"],
                        icon=icon + ".png",
                        main_stat=main_stat,
                        sub_stat_list=sub_stat_list,
                        rank=item["flat"]["rankLevel"],
                    )
                    if temp_relic.slot == "EQUIP_BRACER":
                        relic_list.flower = temp_relic
                    elif temp_relic.slot == "EQUIP_NECKLACE":
                        relic_list.plume = temp_relic
                    elif temp_relic.slot == "EQUIP_SHOES":
                        relic_list.sands = temp_relic
                    elif temp_relic.slot == "EQUIP_RING":
                        relic_list.goblet = temp_relic
                    elif temp_relic.slot == "EQUIP_DRESS":
                        relic_list.circlet = temp_relic
            role.artifacts = relic_list
            await role.save()
