# from .dmg_model import *
from typing import Optional

from Nahidabot.database.models import Player, PropList, RoleBasicInfo
from Nahidabot.utils.classmodel import RoleInfo

from .role import RoleModel, get_role
from .score import get_scores


async def update_rolemodel(user_qq, aid):
    """"""
    info: RoleInfo
    (info,) = await RoleBasicInfo.filter(aid=aid).values_list("info", flat=True)

    (uid,) = await Player.filter(user_qq=user_qq, is_main_uid=True).values_list(
        "uid", flat=True
    )
    role: Optional[RoleModel] = await get_role(name=info.abbr, user_qq=user_qq, uid=uid)
    if role.name:
        party_list: list[RoleModel] = [role]
        for partner in await role.get_partner():
            (info,) = await RoleBasicInfo.filter(name=partner).values_list(
                "info", flat=True
            )
            party_list.append(await get_role(name=info.abbr, user_qq=user_qq, uid=uid))

        for partner in party_list:
            await partner.get_setting()

        for mode in ["propbuff", "transbuff", "dmgbuff"]:
            buff_list = []
            for partner in party_list:
                buff_list.extend(await partner.get_buff(mode=mode))
            for partner in party_list:
                await partner.load_buff(buff_list, mode=mode)

    role_info = await PropList.get(user_qq=user_qq, uid=uid, role_name=info.name)
    role_info.buff_info = await role.save_buff()
    role_info.dmg_info = await role.get_dmg()
    role_info.scores = await get_scores(role)
    await role_info.save()
