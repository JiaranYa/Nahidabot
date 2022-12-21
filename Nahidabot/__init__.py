from nonebot import get_driver
from nonebot.log import logger

from Nahidabot.database import RoleBasicInfo, connect, disconnect
from Nahidabot.utils.tools import check_version
driver = get_driver()


@driver.on_startup
async def _():
    logger.opt(colors=True).success("纳西妲来帮忙！")
    await connect()
    await RoleBasicInfo.update_infotable()
    await check_version()



@driver.on_shutdown
async def _():
    await disconnect()
    logger.opt(colors=True).success("纳西妲要先休息了")
