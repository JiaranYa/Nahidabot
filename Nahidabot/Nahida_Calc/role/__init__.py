from nonebot.log import logger

from ..role_model import RoleModel
from .Xingqiu import Xingqiu


async def get_role(name: str, user_qq: str, uid: str):
    try:
        role: RoleModel = eval(f"{name}")()
        await role.update_from_database(user_qq=user_qq, uid=uid)
        return role
    except NameError:
        logger.opt(colors=True).warning(f"{name}的信息暂时没有登录虚空")
        return RoleModel(name="")
