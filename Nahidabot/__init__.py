from nonebot import get_driver
from nonebot.log import logger
from Nahidabot import database

driver = get_driver()
@driver.on_startup
async def _():
    logger.opt(colors=True).success("纳西妲来帮忙！")
    await database.connect()
    
@driver.on_shutdown
async def _():
    await database.disconnect()
    logger.opt(colors=True).success("纳西妲要先休息了")