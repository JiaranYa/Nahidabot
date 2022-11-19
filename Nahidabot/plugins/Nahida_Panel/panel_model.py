from PIL import Image, ImageDraw
from io import BytesIO
from typing import Optional, Union, Literal, Tuple, Any

class ShowImage(object):
    """
    
    """
    def __init__(self,
                image:Optional[Image.Image] = None,
                size:tuple[int,int] = (200,200),
                color:Union[str,tuple[int,int,int,int]] = "#FFFF",
                mode:str = "RGBA"
                ) -> None:
        if image:
            self.image = image.copy().convert(mode)
        else:
            self.image = Image.new(mode=mode,size=size,color=color)

    @property
    def draw(self):
        return ImageDraw.Draw(self.image)

    @property
    def size(self):
        return self.image.size

    # async def resize(self,size:Union[int,tuple[int,int]]):
    #     if isinstance(size,int):
    #         # self.image.resize((size,int(self.image.size[1]*size/self.image.size[0])),Image.ANTIALIAS)
    #         self.image.resize((900,2100),Image.ANTIALIAS)
    #         print(self.image.size)
    #     else:
    #         self.image.resize(size,Image.ANTIALIAS)

    async def bg_setting(self,color:Union[str,tuple[int,int,int,int]]):
        image = Image.new(mode="RGBA",size=self.size,color=color)
        self.image = Image.blend(self.image,image,0.6)
        pass

    def save_to_io(self, **kwargs):
        bio = BytesIO()
        self.image.save(bio,"png",**kwargs)
        return bio

    def show(self):
        self.image.show()

    async def crop(self):
        pass

    async def paste(self,
                    image:Union[Image.Image,"ShowImage"],
                    pos):
        if isinstance(image, ShowImage):
            image = image.image
            
        image = image.convert("RGBA")
        self.image.paste(image,pos,image)

    async def text( self,
                    text:Union[str,int,float],
                    width:Union[float, Tuple[float, float]],
                    height:Union[float, Tuple[float, float]],
                    font:Optional[Any] = None,
                    color:Union[str, Tuple[int, int, int]] = 'white',
                    align:Literal['left', 'center', 'right'] = 'left'):

        if isinstance(text,(int,float)):
            text = str(text)  

        if align == "left":
            if isinstance(width,tuple):
                width = width[0]
            if isinstance(height, tuple):
                height = height[0]
            self.draw.text(xy=(width,height),text=text,fill=color,font=font)
        elif align in ['center', 'right']:
            W, H = self.draw.textsize(text, font)
            if align == 'center':
                w = width[0] + (width[1] - width[0] - W) / 2 if isinstance(width, tuple) else width
                h = height[0] + (height[1] - height[0] - H) / 2 if isinstance(height, tuple) else height
            else:
                if isinstance(width, tuple):
                    width = width[1]
                w = width - W
                h = height[0] if isinstance(height, tuple) else height
            self.draw.text(xy=(w, h),
                           text=text,
                           fill=color,
                           font=font)
        else:
            raise ValueError("对齐类型必须为\'left\', \'center\'或\'right\'")
    
    async def text_box( self):
        pass