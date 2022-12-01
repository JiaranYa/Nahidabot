import json
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urljoin

import aiofiles
import aiohttp
from nonebot.log import logger
from PIL import Image

from Nahidabot.utils.path import AKASHA_STORE_URL, GRAPHIC_PATH


async def load_json(path: Union[str, Path], encoding: str = "utf-8") -> dict:
    """
    读取json文件
    @params
        path: 文件路径
        encoding: 编码，默认为utf-8
    @return
        文件自身数据格式
    """
    if isinstance(path, str):
        path = Path(path)
    if path.exists():
        async with aiofiles.open(path, encoding=encoding) as f:
            return json.loads(await f.read())
    else:
        return {}


async def load_img(
    path: Union[Path, str], size: Optional[tuple[int, int]] = None, mode: str = "RGBA"
) -> Image.Image:
    """
    读取静态图片
    @params
        path:图片路径
        size:缩放大小
        mode:图片模式，默认“RGBA”
    """
    if isinstance(path, str):
        path = Path(path)

    if not Path.exists(file := GRAPHIC_PATH / path):
        file.parent.mkdir(parents=True, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                urljoin(AKASHA_STORE_URL, path.as_posix())
            ) as response:
                content = await response.read()
                if response.status != 200:
                    logger.opt(colors=True).error("不存在该图片")
                else:
                    async with aiofiles.open(file, "wb") as f:
                        await f.write(content)

    img = Image.open(file)

    if size:
        img = img.resize(size, Image.ANTIALIAS)
    img.convert(mode)

    return img
