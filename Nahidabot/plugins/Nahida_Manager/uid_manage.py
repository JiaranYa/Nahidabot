import re, aiohttp, json
from datetime import datetime, timezone
from urllib.parse import urljoin
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.log import logger
from Nahidabot.database import Player, PropList
from Nahidabot.utils.classmodel import EnkaInfo

# *-----------------------------------------------*
uid_bind = on_command("绑定uid",rule=to_me(),aliases={"绑定"},priority=3,block=True)

@uid_bind.handle()
async def _(event:MessageEvent,msg:Message = CommandArg()):
    m = msg.extract_plain_text()
    if uid := re.search(r'\d{9}',m):
        data = await update_from_enka(uid.group())
        if player_info := data.playerInfo:
            if player_info["nickname"]:
                await update_display_box(uid=data.uid,data=data,user_qq=event.user_id)
                logger.opt(colors=True).success(f"虚空绑定了玩家 {uid.group()} 的信息")
                await uid_bind.send("初次更新展柜信息")
            else:
                await uid_bind.finish("你还没有降临提瓦特")
        else:
            await uid_bind.finish("虚空中还没有你的信息")
    else:
        await uid_bind.finish("是无效uid")

# *-----------------------------------------------*
uid_update = on_command("更新面板",rule=to_me(),priority=3,block=True)

@uid_update.handle()
async def _(event:MessageEvent):
    [(uid,update_time),] = await Player.filter(user_qq=event.user_id,is_main_uid=True).values_list("uid","update_time")
    if (datetime.utcnow().replace(tzinfo=timezone.utc)-update_time).total_seconds() < 600:
        await uid_update.finish("请等待10分钟再更新")
    else:
        data = await update_from_enka(uid=uid)
        await update_display_box(uid=uid,data=data,user_qq=event.user_id)
        await uid_update.finish("已更新完毕")

async def update_display_box(uid,data,user_qq):
    await Player.insert_or_update(uid=uid,data=data.playerInfo,user_qq=user_qq)
    await PropList.inser_or_update_role(uid=uid,data_list=data.avatarInfoList,user_qq=user_qq)
    logger.opt(colors=True).success(f"已更新{uid}的信息")

# *-----------------------------------------------*
async def update_from_enka(uid:str):
    url = urljoin("https://enka.network/u/","/".join([uid,"__data.json"]))

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            info:dict = json.loads(await response.text())
            return EnkaInfo(uid=uid,
                            playerInfo=info.get("playerInfo"),
                            avatarInfoList=info.get("avatarInfoList")) 