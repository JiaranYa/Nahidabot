from PIL import ImageFont

from Nahidabot.utils.path import FONT_PATH


class Font(object):
    def __init__(self) -> None:
        self.font_dict = {
            "Yozai":"Yozai-Bold.ttf",
            "HKFY":"华康方圆体W7.TTC"
    }

    def get(self,font:str,size:int):
        # TODO:下载字体
        if not (FONT_PATH / self.font_dict[font]).exists():
            pass
        return ImageFont.truetype(str(FONT_PATH / self.font_dict[font]),size=size, encoding="utf-8")
