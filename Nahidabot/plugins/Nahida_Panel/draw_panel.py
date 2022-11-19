from PIL import Image
from pathlib import Path
from .panel_model import ShowImage
from typing import Union
from asyncio import run
from nonebot.adapters.onebot.v11 import MessageSegment
from Nahidabot.utils.file import load_img, load_json
from Nahidabot.utils.font import Font
from Nahidabot.utils.classmodel import Role, Relic, Relicset
from Nahidabot.utils.path import STATIC_PATH
from Nahidabot.database import PropList
from Nahidabot.utils.rating import rarity_rating
bg_color_map = {
    "Fire":"#ba8c83",
    "Elec":"#9876ad",
    "Water":"#84a1c6",
    "Grass":"#2d8e34",
    "Wind":"#52b0b1",
    "Rock":"#bb9f4b",
    "Ice":"#46a8ba",
}
prop_map = run(load_json(STATIC_PATH/"property.json"))

background_file = "background/overlay.jpg"
gacha_file = Path("Avatarfig")
weapon_file = Path("weapon")
artifacts_file = Path("artifacts")
talent_file = Path("talent")
conste_file = Path("constellation")
others_file = Path("others")

async def draw_role_info(info_data:PropList):
    prop_map = await load_json(STATIC_PATH/"property.json")

    role = Role(name=info_data.role_name,
                talent=info_data.talent,  # type: ignore
                fight_prop=info_data.property,  # type: ignore
                weapon=info_data.weapon,  # type: ignore
                artifacts=info_data.artifacts)  # type: ignore
    img = ShowImage(image=(await load_img(background_file)).transpose(Image.ROTATE_270).resize((800,2100)))
    
    if not role.talent or not role.fight_prop or not role.weapon:
        return None

    await img.bg_setting(bg_color_map[role.talent.element])
    # 立绘
    gacha = await load_img(gacha_file/"_".join(["UI","Gacha","AvatarIcon",role.talent.abbr+".png"]))
    await img.paste(image=gacha.resize((int(gacha.size[0]*600/gacha.size[1]),600)),pos=(0,0))
    # 信息
    await img.text( role.name,
                    width=(400,800),height=(0,100),
                    align="right",
                    font=Font().get(font="HKFY",size=80))
    await img.text( f"uid:{info_data.uid}",
                    width=(400,800),height=90,
                    align="right",
                    font=Font().get(font="Yozai",size=20))  
    await img.text( f"Lv{role.talent.level}",
                    width=(500,650),height=120,
                    align="center",
                    font=Font().get(font="Yozai",size=40)) 
    await img.text( f"C{role.talent.constellation}",
                    width=(650,800),height=120,
                    align="center",
                    font=Font().get(font="Yozai",size=40))  
    
    # 面板
    propcase = ShowImage(size=(300,320),color="#0001")

    await propcase.text("生命值",
                        width=(0,150),height=(0,40),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{int(role.fight_prop.hp)}",
                        width=(150,300),height=(0,40),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await propcase.text("攻击力",
                        width=(0,150),height=(40,80),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{int(role.fight_prop.atk)}",
                        width=(150,300),height=(40,80),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await propcase.text("防御力",
                        width=(0,150),height=(80,120),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{int(role.fight_prop.defend)}",
                        width=(150,300),height=(80,120),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await propcase.text("元素精通",
                        width=(0,150),height=(120,160),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{int(role.fight_prop.elemental_mastery)}",
                        width=(150,300),height=(120,160),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await propcase.text("暴击率",
                        width=(0,150),height=(160,200),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{round(role.fight_prop.crit_rate*100,1)}%",
                        width=(150,300),height=(160,200),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await propcase.text("暴击伤害",
                        width=(0,150),height=(200,240),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{round(role.fight_prop.crit_dmg*100,1)}%",
                        width=(150,300),height=(200,240),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await propcase.text("元素充能效率",
                        width=(0,150),height=(240,280),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{round(role.fight_prop.recharge*100,1)}%",
                        width=(150,300),height=(240,280),
                        align="right",
                        font=Font().get(font="Yozai",size=25)) 

    add_hurt = prop_map[f"FIGHT_PROP_{(role.talent.element).upper()}_ADD_HURT"]
    if role.artifacts and role.artifacts.goblet:
        if "ADD_HURT" in role.artifacts.goblet.main_stat.name:
            add_hurt = prop_map[role.artifacts.goblet.main_stat.name]
    
    await propcase.text(add_hurt,
                        width=(0,150),height=(280,320),
                        align="left",
                        font=Font().get(font="Yozai",size=25))
    await propcase.text(f"{round(role.fight_prop.get_elem_dmg(add_hurt)*100,1)}%",
                        width=(150,300),height=(280,320),
                        align="right",
                        font=Font().get(font="Yozai",size=25))

    await img.paste(image=propcase,pos=(400,180))
    
    # 武器
    weapon_case = ShowImage(size=(250,120),color="#0001")
    weapon_icon = await load_img(weapon_file / (role.weapon.icon+".png"),size=(100,100))
    await weapon_case.paste(weapon_icon,pos=(0,0))
    await weapon_case.text( f"{role.weapon.name}",
                            width=(100,250),height=10,
                            align="center",
                            font=Font().get(font="Yozai",size=20))
    await weapon_case.text( f"LV{role.weapon.level}",
                            width=(100,200),height=80,
                            align="center",
                            font=Font().get(font="Yozai",size=20))                                
    await weapon_case.text( f"R{role.weapon.affix}",
                            width=(200,250),height=80,
                            align="center",
                            font=Font().get(font="Yozai",size=20))
    await img.paste(image=weapon_case,pos=(50,630))
    
    # 天赋和命座
    active_icon = others_file/ f"{(role.talent.element).lower()}_on.png"
    inactive_icon = others_file/ "off.png"
    skill_case = ShowImage(size=(400,240),color="#0001")

    for i,l in enumerate(["skill_A","skill_E","skill_Q"]):
        await skill_case.paste( await load_img(active_icon,size=(120,120)),
                                pos=(10+i*130,0)) 
        await skill_case.paste( await load_img(talent_file/role.talent.skill_icon[i],size=(80,80)),
                                pos=(30+i*130,20))
        await skill_case.text(  role.talent.dict()[l],
                                width=(52+i*135,80+i*135),height=120,
                                font=Font().get("Yozai",size=20),
                                align="center")

    conste_flag = [True if i < role.talent.constellation else False for i in range(6)]
    for i in range(6):
        if conste_flag[i]:
            await skill_case.paste(await load_img(active_icon,size=(80,80)),pos=(10+i*60,160))
        else:
            await skill_case.paste(await load_img(inactive_icon,size=(80,80)),pos=(10+i*60,160))
        await skill_case.paste(await load_img(conste_file/f"UI_Talent_{role.talent.abbr}_{str(i+1)}.png",size=(40,40)),pos=(30+i*60,180))

        await img.paste(image=skill_case,pos=(350,510))
    
    # 圣遗物
    if items:= role.artifacts:
        for i,item in enumerate([items,items.flower,items.plume,items.sands,items.goblet,items.circlet]):
            if item:
                await img.paste(await get_relic_case(item),
                                pos=(20+(i%3)*260,800+int(i/3)*260))

    return MessageSegment.image(img.save_to_io())

# 圣遗物小模块
async def get_relic_case(item:Union[Relic,Relicset]):
    box = ShowImage(size=(250,250),color="#0001")
    if isinstance(item,Relicset):
        await box.text( rarity_rating(item.total_score),
                        width=(0,250),height=0,
                        font=Font().get("Yozai",size=80),
                        align="center")
        await box.text( item.total_score,
                        width=(0,250),height=100,
                        font=Font().get("Yozai",size=40),
                        align="center")

        count=0
        for key,value in item.set_info.items():
            if value>=2:
                await box.text( key,
                                width=(0,200),height=180+count*30,
                                font=Font().get("Yozai",size=20),
                                align="left")
                await box.text( 4 if value>=4 else 2,
                                width=(200,250),height=180+count*30,
                                font=Font().get("Yozai",size=20),
                                align="right")
                count += 1
        if count == 0:
            await box.text( "无套装加成",
                            width=(0,250),height=200,
                            font=Font().get("Yozai",size=20),
                            align="center")
    else:
        await box.paste(await load_img(artifacts_file / item.icon,size=(80,80)),
                        pos=(0,0))
        await box.text( item.name,
                        width=100,height=10,
                        font=Font().get("Yozai",size=20))

        await box.text( rarity_rating(item.score),
                        width=80,height=40,
                        font=Font().get("Yozai",size=30))
        await box.text( item.score if item.score else 0,
                        width=(180,250),height=40,
                        font=Font().get("Yozai",size=25),
                        align="center")

        await box.text( prop_map[item.main_stat.name],
                        width=(0,150),height=80,
                        font=Font().get("Yozai",size=24),
                        align="left")
        await box.text( item.main_stat.prop,
                        width=(150,250),height=80,
                        font=Font().get("Yozai",size=24),
                        align="right")  

        for i,sub in enumerate(item.sub_stat_list):
            await box.text( prop_map[sub.name],
                            width=(0,150),height=120+i*30,
                            font=Font().get("Yozai",size=20),
                            align="left")
            await box.text( sub.prop,
                            width=(150,250),height=120+i*30,
                            font=Font().get("Yozai",size=20),
                            align="right")  
    return box
