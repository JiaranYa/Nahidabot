from nonebot.log import logger
from tortoise import Tortoise

from Nahidabot.utils.path import DB_PATH

from .models import *

DATABASE = {
    "connections":  {
        "database":      {
            "engine":       "tortoise.backends.sqlite",
            "credentials":  {"file_path": DB_PATH},
        }
    },
    "apps":         {
        "resource":     {
            "models":               ['Nahidabot.database.models.resource'],
            "default_connection":   "database",
        },
        "data":     {
            "models":               ['Nahidabot.database.models.playerinfo'],
            "default_connection":   "database",
        }
    }
}

async def connect():
    """
    连接数据库
    """
    try:
        await Tortoise.init(DATABASE)
        await Tortoise.generate_schemas()
        logger.opt(colors=True).success("虚空已连接")
    except Exception as e:
        logger.opt(colors=True).error("虚空连接失败")
        raise e

async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("虚空已断开")
