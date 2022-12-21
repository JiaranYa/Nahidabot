from nonebot.log import logger
import toml
from .path import VERSION_PATH


def rarity_rating(score: float, flag: str = "single") -> tuple[str, str]:
    """评分"""
    if flag == "total":
        score /= 5

    if score >= 55:
        return "PER", "Crimson"
    elif 50 <= score < 55:
        return "ACE", "DeepPink"
    elif 45 <= score < 50:
        return "UR", "OrangeRed"
    elif 40 <= score < 45:
        return "SSR", "Gold"
    elif 35 <= score < 40:
        return "SR", "Violet"
    elif 30 <= score < 35:
        return "R", "DeepSkyBlue"
    elif 25 <= score < 30:
        return "N", "LimeGreen"
    elif 0 <= score < 25:
        return "G", "white"
    else:
        return "UN", "#afafaf"


async def check_version():
    """版本检查"""
    logger.opt(colors=True).info("纳西妲开始检查虚空")
    version = toml.load(VERSION_PATH)["VERSION"]
    logger.opt(colors=True).info(f"本机版本:{version}")
