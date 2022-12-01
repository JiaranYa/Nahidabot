import subprocess
from urllib.parse import urljoin

import aiohttp
import toml
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from Nahidabot.database.models.resource import RoleBasicInfo
from Nahidabot.utils.path import GITHUB_URL, NAHIDABOT_URL, VERION_FILE, VERSION_PATH

check_version = on_command(
    "查看版本", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@check_version.handle()
async def _(matcher: Matcher):
    version: dict = toml.load(VERSION_PATH)
    await matcher.finish(f"当前虚空版本:{version['BOT_VERSION']}\n" + f"最新虚空版本:\n")


upgrade_version = on_command(
    "更新版本", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@upgrade_version.handle()
async def _(matcher: Matcher):
    # TODO:版本检测更新
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(urljoin(NAHIDABOT_URL,str("Nahidabot"/VERION_FILE))) as response:
    #         new_version = await response.read()

    # old_version:dict = toml.load(VERSION_PATH)
    # if old_version['BOT_VERSION'] == new_version['BOT_VERSION']:
    #     await upgrade_version.finish("已是最新版本")
    # else:
    #     subprocess.run(["git","clone",GITHUB_URL,"."])

    await RoleBasicInfo.update_infotable()

    # await matcher.finish(f"虚空更新至版本 {old_version['BOT_VERSION']}")
