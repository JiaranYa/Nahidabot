from io import BytesIO
from typing import Any, Literal, Optional, Union

from nonebot.utils import run_sync
from PIL import Image, ImageDraw, ImageFont

from Nahidabot.utils.path import FONT_PATH


class ShowImage(object):
    """ """

    def __init__(
        self,
        image: Optional[Image.Image] = None,
        size: tuple[int, int] = (200, 200),
        color: Union[str, tuple[int, int, int, int]] = "#FFFF",
        mode: str = "RGBA",
    ) -> None:
        if image:
            self.image = image.copy().convert(mode)
        else:
            self.image = Image.new(mode=mode, size=size, color=color)

    @property
    def draw(self):
        return ImageDraw.Draw(self.image)

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    @property
    def size(self):
        return self.image.size

    def save_to_io(self, **kwargs):
        bio = BytesIO()
        self.image.save(bio, "png", **kwargs)
        return bio

    def show(self):
        self.image.show()

    def convert(self, mode: str):
        self.image.convert(mode)

    @run_sync
    def crop(self, box: tuple[int, int, int, int]):
        """
        裁剪图像
         box: 目标区域
        """
        self.image = self.image.crop(box)

    @run_sync
    def paste(
        self,
        image: Union[Image.Image, "ShowImage"],
        pos: tuple[int, int],
        alpha: bool = True,
    ):
        """
        粘贴图像
        Params:
            image: 图像
            pos: 位置
            alpha: 是否透明
        """
        if image is None:
            return
        if isinstance(image, ShowImage):
            image = image.image
        if alpha:
            image = image.convert("RGBA")
            self.image.alpha_composite(image, pos)
        else:
            self.image.paste(image, pos)

    @run_sync
    def text(
        self,
        text: Union[str, int, float],
        width: Union[float, tuple[float, float]],
        height: Union[float, tuple[float, float]],
        font: Optional[Any] = None,
        color: Union[str, tuple[int, int, int]] = "white",
        align: Literal["left", "center", "right"] = "left",
    ):

        if isinstance(text, (int, float)):
            text = str(text)

        if align == "left":
            if isinstance(width, tuple):
                width = width[0]
            if isinstance(height, tuple):
                height = height[0]
            self.draw.text(xy=(width, height), text=text, fill=color, font=font)
        elif align in ["center", "right"]:
            W, H = self.draw.textsize(text, font)
            if align == "center":
                w = (
                    width[0] + (width[1] - width[0] - W) / 2
                    if isinstance(width, tuple)
                    else width
                )
                h = (
                    height[0] + (height[1] - height[0] - H) / 2
                    if isinstance(height, tuple)
                    else height
                )
            else:
                if isinstance(width, tuple):
                    width = width[1]
                w = width - W
                h = height[0] if isinstance(height, tuple) else height
            self.draw.text(xy=(w, h), text=text, fill=color, font=font)
        else:
            raise ValueError("对齐类型必须为'left', 'center'或'right'")

    def text_length(self, text: str, font: ImageFont.ImageFont) -> int:
        return int(self.draw.textlength(text, font))

    @run_sync
    def stretch(
        self,
        pos: tuple[int, int],
        length: int,
        type: Literal["width", "height"] = "height",
    ):
        """
        将某一部分进行拉伸
         pos: 拉伸的部分
         length: 拉伸的目标长/宽度
         type: 拉伸方向，width:横向, height: 竖向
        """
        if pos[0] <= 0:
            raise ValueError("起始轴必须大于等于0")
        if pos[1] <= pos[0]:
            raise ValueError("结束轴必须大于起始轴")
        if type == "height":
            if pos[1] >= self.height:
                raise ValueError("终止轴必须小于图片高度")
            top = self.image.crop((0, 0, self.width, pos[0]))
            bottom = self.image.crop((0, pos[1], self.width, self.height))
            if length == 0:
                self.image = Image.new("RGBA", (self.width, top.height + bottom.height))
                self.image.paste(top, (0, 0))
                self.image.paste(bottom, (0, top.height))
            else:
                center = self.image.crop((0, pos[0], self.width, pos[1])).resize(
                    (self.width, length), Image.Resampling.LANCZOS
                )
                self.image = Image.new(
                    "RGBA", (self.width, top.height + center.height + bottom.height)
                )
                self.image.paste(top, (0, 0))
                self.image.paste(center, (0, top.height))
                self.image.paste(bottom, (0, top.height + center.height))
        elif type == "width":
            if pos[1] >= self.width:
                raise ValueError("终止轴必须小于图片宽度")
            top = self.image.crop((0, 0, pos[0], self.height))
            bottom = self.image.crop((pos[1], 0, self.width, self.height))
            if length == 0:
                self.image = Image.new("RGBA", (top.width + bottom.width, self.height))
                self.image.paste(top, (0, 0))
                self.image.paste(bottom, (top.width, 0))
            else:
                center = self.image.crop((pos[0], 0, pos[1], self.height)).resize(
                    (length, self.height), Image.Resampling.LANCZOS
                )
                self.image = Image.new(
                    "RGBA", (top.width + center.width + bottom.width, self.height)
                )
                self.image.paste(top, (0, 0))
                self.image.paste(center, (top.width, 0))
                self.image.paste(bottom, (top.width + center.width, 0))
        else:
            raise ValueError("类型必须为'width'或'height'")

    @run_sync
    def draw_line(
        self,
        begin: tuple[int, int],
        end: tuple[int, int],
        color: Union[str, tuple[int, int, int, int]] = "black",
        width: int = 1,
    ):
        """
        画线
         begin: 起始点
         end: 终点
         color: 颜色
         width: 宽度
        :return:
        """
        self.draw.line(begin + end, fill=color, width=width)

    @run_sync
    def draw_rounded_rectangle(
        self,
        pos: tuple[int, int, int, int],
        radius: int = 5,
        color: Union[str, tuple[int, int, int, int]] = "white",
        width: int = 1,
    ):
        """
        绘制圆角矩形
        :param pos: 圆角矩形的位置
        :param radius: 半径
        :param color: 颜色
        :param width: 宽度
        """
        self.convert("RGBA")
        self.draw.rounded_rectangle(xy=pos, radius=radius, fill=color, width=width)


class FontManager:
    """
    字体管理器，获取字体路径中的所有字体
    """

    def __init__(self):
        self.font_path = FONT_PATH
        self.fonts = [
            font_file.name for font_file in FONT_PATH.iterdir() if font_file.is_file()
        ]
        self.fonts_cache = {}

    def get(self, font_name: str = "hywh.ttf", size: int = 25) -> ImageFont.ImageFont:
        """
        获取字体，如果已在缓存中，则直接返回
        Paras:
            font_name: 字体名称
            size: 字体大小
            variation: 字体变体
        """
        if "ttf" not in font_name and "ttc" not in font_name and "otf" not in font_name:
            font_name += ".ttf"
        if font_name not in self.fonts:
            font_name = font_name.replace(".ttf", ".ttc")
        if font_name not in self.fonts:
            raise FileNotFoundError(f"不存在字体文件 {font_name} ，请补充至字体资源中")
        if f"{font_name}-{size}" in self.fonts_cache:
            font = self.fonts_cache[f"{font_name}-{size}"]
        else:
            font = ImageFont.truetype(str(self.font_path / font_name), size)
            self.fonts_cache[f"{font_name}-{size}"] = font

        return font
