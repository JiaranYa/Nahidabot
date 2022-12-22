import subprocess
from urllib.parse import urljoin

import aiohttp
import toml
from nonebot import on_command
from nonebot.log import logger
from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER

from Nahidabot.utils.path import NAHIDABOT_URL, VERION_FILE, VERSION_PATH

upgrade_version = on_command(
    "更新版本", aliases={"up"}, permission=SUPERUSER, priority=1, block=True
)


@upgrade_version.handle()
async def _():
    logger.opt(colors=True).info("纳西妲开始检查虚空")
    version = toml.load(VERSION_PATH)["VERSION"]
    logger.opt(colors=True).info(f"本机版本:{version}")

    url = urljoin(NAHIDABOT_URL, "/".join(["Nahidabot", VERION_FILE.as_posix()]))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            cloud_version = toml.loads(content.decode("utf-8"))["BOT_VERSION"]

    logger.opt(colors=True).info(f"云端版本:{cloud_version}")
    if cloud_version == version:
        await upgrade_version.finish("已是最新版本")
    else:
        pass


@upgrade_version.got("flag", prompt="检测到新版本，是否更新\n0.不更新\n1.更新")
async def _(flag=ArgPlainText("flag")):
    if flag == "1":
        logger.opt(colors=True).info("开始更新")
        subprocess.run(["git", "fetch", "origin"])
        logger.opt(colors=True).info("已更新至最新版本")
        await upgrade_version.finish("纳西妲已经更新了虚空")

    await upgrade_version.finish("有事再找纳西妲哦~")
