from copy import deepcopy
from datetime import datetime
from pathlib import Path

from nonebot.adapters.onebot.v11 import MessageSegment

from Nahidabot.utils.classmodel import DMG, BuffInfo, Relic, Role
from Nahidabot.utils.file import load_img, load_json
from Nahidabot.utils.path import STATIC_PATH
from Nahidabot.utils.rating import rarity_rating

from .panel_model import FontManager, ShowImage

bg_color_map = {
    "Fire": "#ba8c83",
    "Elec": "#9876ad",
    "Water": "#84a1c6",
    "Grass": "#2d8e34",
    "Wind": "#52b0b1",
    "Rock": "#bb9f4b",
    "Ice": "#46a8ba",
}
prop_map = load_json(STATIC_PATH / "property.json")

materials_file = Path("others")
gacha_file = Path("avatarimg")
icon_file = Path("icon")
weapon_file = Path("weapon")
artifacts_file = Path("artifacts")
talent_file = Path("talent")
conste_file = Path("constellation")
others_file = Path("others")
fm = FontManager()


async def draw_role_info(role_info: Role, uid: str, time: datetime):
    """角色面板卡片"""
    img = ShowImage(await load_img(materials_file / f"bg_{role_info.info.element}.png"))
    # 增益列表
    if buff_info := role_info.buff_list:
        buff_img = await draw_buff_pic(buff_info)
        await img.stretch((730, 1377), buff_img.height + 667, "height")
        await img.paste(buff_img, (42, 1820))
    # 伤害列表
    if dmg_info := role_info.dmg_list:
        dmg_img = await draw_dmg_pic(dmg_info)
        await img.stretch((730, 1377), dmg_img.height + 667, "height")
        await img.paste(dmg_img, (42, 1820))

    # 立绘
    chara_img = await load_img(
        gacha_file / f"UI_Gacha_AvatarImg_{role_info.info.abbr}.png"
    )
    if chara_img.height >= 630:
        chara_img = chara_img.resize((chara_img.width * 630 // chara_img.height, 630))
    else:
        chara_img = chara_img.resize(
            (chara_img.width, chara_img.height * 630 // chara_img.height)
        )
    await img.paste(chara_img, (770 - chara_img.width // 2, 20))
    await img.paste(await load_img(materials_file / "底遮罩.png"), (0, 0))
    # 地区
    if role_info.info.region:
        await img.paste(
            await load_img(
                materials_file / f"{role_info.info.region}.png", size=(108, 108)
            ),
            (25, 25),
        )

    await img.text(f"UID{uid}", 160, 100, fm.get("number.ttf", 48))
    await img.text(role_info.name, 45, 150, fm.get("优设标题黑.ttf", 72))
    name_length = img.text_length(role_info.name, fm.get("优设标题黑.ttf", 72))

    level_mask = await load_img(materials_file / "等级遮罩.png")
    await img.paste(level_mask, (45 + name_length + 25, 172))
    await img.text(
        f"LV{role_info.info.level}",
        (40 + name_length + 25, 40 + name_length + 25 + 171),
        (172, 172 + 52),
        fm.get("number.ttf", 48),
        "#0e2944",
        "center",
    )

    # 属性值
    await img.text("生命值", 59, 267, fm.get("hywh.ttf", 34))
    await img.text(
        f"{int(role_info.fight_prop.hp_base)}",
        450
        - img.text_length(
            f"+{int(role_info.fight_prop.hp_extra)}", fm.get("number.ttf", 34)
        )
        - 5,
        269,
        fm.get("number.ttf", 34),
        align="right",
    )
    await img.text(
        f"+{int(role_info.fight_prop.hp_extra)}",
        450,
        269,
        fm.get("number.ttf", 34),
        "#59c538",
        "right",
    )

    await img.text("攻击力", 59, 324, fm.get("hywh.ttf", 34))
    await img.text(
        f"{int(role_info.fight_prop.atk_base)}",
        450
        - img.text_length(
            f"+{int(role_info.fight_prop.atk_extra)}", fm.get("number.ttf", 34)
        )
        - 5,
        326,
        fm.get("number.ttf", 34),
        align="right",
    )
    await img.text(
        f"+{int(role_info.fight_prop.atk_extra)}",
        450,
        326,
        fm.get("number.ttf", 34),
        "#59c538",
        "right",
    )

    await img.text("防御力", 59, 382, fm.get("hywh.ttf", 34))
    await img.text(
        f"{int(role_info.fight_prop.defend)}",
        450
        - img.text_length(
            f"+{int(role_info.fight_prop.def_extra)}", fm.get("number.ttf", 34)
        )
        - 5,
        384,
        fm.get("number.ttf", 34),
        align="right",
    )
    await img.text(
        f"+{int(role_info.fight_prop.def_extra)}",
        450,
        384,
        fm.get("number.ttf", 34),
        "#59c538",
        "right",
    )

    await img.text("暴击率", 59, 441, fm.get("hywh.ttf", 34))
    await img.text(
        f"{round(role_info.fight_prop.crit_rate * 100, 1)}%",
        450,
        443,
        fm.get("number.ttf", 34),
        align="right",
    )

    await img.text("暴击伤害", 59, 498, fm.get("hywh.ttf", 34))
    await img.text(
        f"{round(role_info.fight_prop.crit_dmg * 100, 1)}%",
        450,
        500,
        fm.get("number.ttf", 34),
        align="right",
    )

    await img.text("元素精通", 59, 556, fm.get("hywh.ttf", 34))
    await img.text(
        str(int(role_info.fight_prop.elemental_mastery)),
        450,
        558,
        fm.get("number.ttf", 34),
        align="right",
    )

    await img.text("元素充能效率", 59, 615, fm.get("hywh.ttf", 34))
    await img.text(
        f"{round(role_info.fight_prop.recharge * 100, 1)}%",
        450,
        617,
        fm.get("number.ttf", 34),
        align="right",
    )

    add_hurt = prop_map[f"FIGHT_PROP_{(role_info.info.element).upper()}_ADD_HURT"]
    if role_info.artifacts and role_info.artifacts.goblet:
        if "ADD_HURT" in role_info.artifacts.goblet.main_stat.name:
            add_hurt = prop_map[role_info.artifacts.goblet.main_stat.name]

    await img.text(
        add_hurt,
        59,
        674,
        fm.get("hywh.ttf", 34),
    )
    await img.text(
        f"{round(role_info.fight_prop.get_elem_dmg(add_hurt) * 100, 1)}%",
        450,
        676,
        fm.get("number.ttf", 34),
        align="right",
    )

    # 天赋
    base_icon = await load_img(
        materials_file / f"icon_{role_info.info.element}.png", mode="RGBA"
    )
    base_icon_grey = await load_img(materials_file / "icon_off.png", mode="RGBA")

    for i, sk in enumerate(["A", "E", "Q"]):
        await img.paste(base_icon.resize((132, 142)), (551 + i * 176, 633))
        await img.text(
            str(role_info.info.get_skill(sk)),
            (517 + 176 * i, 559 + 176 * i),
            690,
            fm.get("number.ttf", 34),
            "#0e2944",
            "center",
        )
        await img.paste(
            await load_img(
                talent_file / f"{role_info.info.skill_icon[i]}",
                size=(57, 57),
                mode="RGBA",
            ),
            (588 + i * 176, 679),
        )

    # 命座
    lock = await load_img(materials_file / "锁.png", mode="RGBA", size=(45, 45))
    # t = 0
    for i in range(6):
        if i < role_info.info.constellation:
            await img.paste(base_icon.resize((83, 90)), (510 + i * 84, 805))
            con_icon = await load_img(
                conste_file / f"UI_Talent_{role_info.info.abbr}_{i+1}.png",
                size=(45, 45),
                mode="RGBA",
            )
            await img.paste(con_icon, (529 + i * 84, 828))
        else:
            await img.paste(base_icon_grey.resize((83, 90)), (510 + i * 84, 805))
            await img.paste(lock, (530 + i * 84, 828))

    # 武器
    weapon_bg = await load_img(
        materials_file / f"star{role_info.weapon.rank}.png", size=(150, 150)
    )
    await img.paste(weapon_bg, (59, 757))
    weapon_icon = await load_img(
        weapon_file / f"{role_info.weapon.icon}.png", size=(150, 150), mode="RGBA"
    )
    await img.paste(weapon_icon, (59, 757))
    await img.text(role_info.weapon.name, 254, 759, fm.get("hywh.ttf", 34))

    for i in range(role_info.weapon.rank):
        await img.text(
            "★", 254 + i * 30, 798, color="yellow", font=fm.get("HKFY.ttf", 30)
        )
    await img.text(
        f"LV{role_info.weapon.level}",
        (254, 254 + 98),
        (834, 864),
        fm.get("number.ttf", 27),
        "#0e2944",
        "center",
    )
    await img.text(f"精炼{role_info.weapon.affix}阶", 254, 879, fm.get("hywh.ttf", 34))

    # 圣遗物评分
    # score_pro = total_score / (average * 5) * 100
    relic_set: dict[str, int] = role_info.artifacts.get_item()
    score_total = role_info.scores.get_score()
    total_rank, color = rarity_rating(score_total, "total")
    # rank_icon = await load_img(ENKA_RES / f'评分{total_rank[0]}.png', mode='RGBA')
    await img.text(
        round(score_total, 1),
        (150, 250),
        (940, 1060),
        align="center",
        font=fm.get("number.ttf", 60),
    )
    await img.text(
        total_rank,
        (150, 250),
        (1140, 1240),
        color=color,
        align="center",
        font=fm.get("number.ttf", 80),
    )

    i = 0
    for key, value in relic_set.items():
        if value >= 2:
            await img.text(key, 50, 1270 + i * 44, font=fm.get("Yozai-Bold.ttf", 24))
            await img.text(value, 350, 1270 + i * 44, font=fm.get("Yozai-Bold.ttf", 24))
            i += 1

    # 圣遗物
    for i, item in enumerate(["flower", "plume", "sands", "goblet", "circlet"]):
        w = 42 + 338 * ((i + 1) % 3)
        h = 937 + 437 * int((i + 1) / 3)
        artifact: Relic = role_info.artifacts.get_item(item)
        artifact_bg = await load_img(
            materials_file / f"star{artifact.rank}.png", size=(93, 93)
        )
        await img.paste(artifact_bg, (216 + w, 70 + h))
        a_icon = await load_img(
            artifacts_file / artifact.icon, size=(93, 93), mode="RGBA"
        )
        await img.paste(a_icon, (217 + w, 70 + h))
        await img.text(artifact.name, 22 + w, 24 + h, fm.get("hywh.ttf", 36))
        score = round(role_info.scores.get_score(item), 1)
        # value, score = GenshinTools.artifact_score(info.prop, artifact, effective)
        # total_score += value
        rank, color = rarity_rating(score)
        await img.text(
            f"{rank}-{score}", 22 + w, 66 + h, fm.get("number.ttf", 28), color=color
        )
        await img.paste(level_mask.resize((98, 30)), (21 + w, 97 + h))
        await img.text(
            f"+{artifact.level}",
            (21 + w, 21 + w + 98),
            99 + h,
            fm.get("number.ttf", 27),
            "black",
            "center",
        )
        await img.text(artifact.main_stat.name, 21 + w, 134 + h, fm.get("hywh.ttf", 25))
        await img.text(
            artifact.main_stat.prop,
            21 + w,
            168 + h,
            font=fm.get("number.ttf", 48),
        )
        for j, stat in enumerate(artifact.sub_stat_list):
            text = stat.name.replace("百分比", "") if "百分比" in stat.name else stat.name
            await img.text(
                text,
                21 + w,
                230 + h + 50 * j,
                color="white",
                font=fm.get("hywh.ttf", 25),
            )

            await img.text(
                stat.prop,
                307 + w,
                230 + h + 50 * j,
                color="white",
                font=fm.get("number.ttf", 25),
                align="right",
            )

    # 落款
    await img.text(
        f'更新于{time.strftime("%m-%d %H:%M")}',
        (0, 1080),
        (img.height - 123, img.height - 80),
        fm.get("优设标题黑.ttf", 33),
        "#afafaf",
        "center",
    )
    await img.text(
        "Created by Nahidabot | Powered by LittlePaimon",
        (0, 1080),
        (img.height - 80, img.height - 40),
        fm.get("优设标题黑.ttf", 33),
        "white",
        "center",
    )

    return MessageSegment.image(img.save_to_io())


async def draw_dmg_pic(dmg_list: list[DMG]) -> ShowImage:
    """
    绘制伤害图片
    @paramsdmg: 伤害列表
    @return: 伤害图片
    """
    height = 120 * len(dmg_list)
    img = ShowImage(size=(1002, height), color=(0, 0, 0, 0), mode="RGBA")
    await img.draw_rounded_rectangle(
        (0, 0, img.width, img.height), 10, (14, 41, 68, 115)
    )

    await img.draw_line((60, 0), (60, 120), (255, 255, 255, 75), 2)
    await img.draw_line((600, 0), (600, 120), (255, 255, 255, 75), 2)
    await img.text(
        0, (0, 60), (0, 120), fm.get("hywh.ttf", 30), color="white", align="center"
    )
    await img.text(
        dmg_list[0].name,
        (60, 600),
        (0, 120),
        fm.get("hywh.ttf", 30),
        color="white",
        align="center",
    )
    await img.text(
        dmg_list[0].weight,
        (600, 1000),
        (0, 120),
        fm.get("hywh.ttf", 30),
        color="white",
        align="center",
    )

    for i, dmg in enumerate(dmg_list[1:], 1):
        if dmg.weight == 0:
            continue
        await img.draw_line((0, 120 * i), (1002, 120 * i), (255, 255, 255, 75), 2)
        await img.draw_line((60, 120 * i), (60, 120 * (i + 1)), (255, 255, 255, 75), 2)
        await img.text(
            i,
            (0, 60),
            (120 * i, 120 * (i + 1)),
            fm.get("hywh.ttf", 30),
            color="white",
            align="center",
        )
        await img.draw_line(
            (60, 60 + 120 * i), (1002, 60 + 120 * i), (255, 255, 255, 75), 2
        )

        await img.draw_line((150, 120 * i), (150, 60 + 120 * i), (255, 255, 255, 75), 2)
        await img.draw_line((900, 120 * i), (900, 60 + 120 * i), (255, 255, 255, 75), 2)

        await img.text(
            dmg.source,
            (60, 150),
            (120 * i, 60 + 120 * i),
            fm.get("hywh.ttf", 30),
            color="white",
            align="center",
        )
        await img.text(
            dmg.name,
            (150, 900),
            (120 * i, 60 + 120 * i),
            fm.get("hywh.ttf", 30),
            color="white",
            align="center",
        )
        await img.text(
            dmg.weight,
            (900, 1002),
            (120 * i, 60 + 120 * i),
            fm.get("hywh.ttf", 30),
            color="white",
            align="center",
        )

        await img.draw_line(
            (600, 60 + 120 * i), (600, 120 * (i + 1)), (255, 255, 255, 75), 2
        )
        await img.text(
            dmg.dsc,
            (60, 600),
            (60 + 120 * i, 120 * (i + 1)),
            fm.get("hywh.ttf", 30),
            color="white",
            align="center",
        )
        await img.text(
            f"{dmg.exp_value} ({dmg.crit_value})",
            (600, 1002),
            (60 + 120 * i, 120 * (i + 1)),
            fm.get("hywh.ttf", 30),
            color="white",
            align="center",
        )

    return img


async def draw_buff_pic(buff_list: list[BuffInfo]) -> ShowImage:
    """
    绘制增益图片
    :param dmg: 增益列表
    :return: 增益图片
    """
    height = 120 * len(buff_list)
    img = ShowImage(size=(1002, height), color=(0, 0, 0, 0), mode="RGBA")
    await img.draw_rounded_rectangle(
        (0, 0, img.width, img.height), 10, (14, 41, 68, 115)
    )

    i = 0
    for buff in buff_list:
        if buff.buff:
            await img.draw_line(
                (60, 60 + 120 * i), (1002, 60 + 120 * i), (255, 255, 255, 75), 2
            )
            await img.draw_line(
                (60, 120 * i), (60, 120 * (i + 1)), (255, 255, 255, 75), 2
            )
            await img.text(
                i + 1,
                (0, 60),
                (120 * i, 120 * (i + 1)),
                fm.get("hywh.ttf", 30),
                color="white",
                align="center",
            )
            await img.draw_line(
                (250, 120 * i), (250, 60 + 120 * i), (255, 255, 255, 75), 2
            )
            await img.draw_line(
                (850, 120 * i), (850, 60 + 120 * i), (255, 255, 255, 75), 2
            )
            await img.text(
                buff.source,
                (60, 250),
                (120 * i, 60 + 120 * i),
                fm.get("hywh.ttf", 30),
                color="white",
                align="center",
            )
            await img.text(
                buff.name,
                (250, 850),
                (120 * i, 60 + 120 * i),
                fm.get("hywh.ttf", 30),
                color="white",
                align="center",
            )

            await img.text(
                buff.setting.state,
                (850, 1002),
                (120 * i, 60 + 120 * i),
                fm.get("Yozai-Bold.ttf", 30),
                color="white",
                align="center",
            )

            await img.text(
                buff.buff.dsc,
                (60, 1002),
                (60 + 120 * i, 120 * (i + 1)),
                fm.get("hywh.ttf", 30),
                color="white",
                align="center",
            )

            await img.draw_line(
                (0, 120 * (i + 1)),
                (1002, 120 * (i + 1)),
                (255, 255, 255, 75),
                2,
            )
            i += 1

    return img


async def draw_setting_info(
    role_info: Role,
    uid: str,
):
    """角色设置卡片"""
    img = ShowImage(await load_img(materials_file / "bg.png"))
    icon_img = await load_img(
        icon_file / f"UI_AvatarIcon_{role_info.info.abbr}.png", (150, 150)
    )
    await img.paste(icon_img, (300, 30))
    # await img.paste(await load_img(materials_file / f"star{role_info.info.}.png"), (0, 0))
    await img.text(role_info.name, 600, 40, fm.get("HKFY.ttf", 84), "black")
    await img.text(f"uid:{uid}", 600, 140, fm.get("number.ttf", 24), "black")
    orange_title = ShowImage(await load_img(materials_file / "orange_card.png"))
    orange_line = ShowImage(await load_img(materials_file / "orange.png"))
    orange_body = ShowImage(await load_img(materials_file / "orange_board.png"))

    buff_img = await draw_setting_pic(role_info.buff_list)
    dmg_img = await draw_weight_pic(role_info.dmg_list)
    h1 = buff_img.height
    h2 = dmg_img.height
    if h1 + h2 + 400 > img.height:
        await img.stretch((730, 1377), h1 + h2 + 400, "height")

    # 增益列表
    await img.paste(orange_title, (40, 200))
    await img.paste(orange_line, (40, 200))
    await img.text("增益设置", (50, 220), 204, fm.get("HKFY.ttf", 40), align="center")

    await img.paste(buff_img, (42, 270))

    body1 = deepcopy(orange_body)
    await body1.stretch((5, body1.width - 5), orange_line.width - 10, "width")
    await body1.stretch((5, body1.height - 5), buff_img.height - 5, "height")
    await img.paste(body1, (40, 270))

    # 伤害列表
    await img.paste(orange_title, (40, 300 + h1))
    await img.paste(orange_line, (40, 300 + h1))
    await img.text("权重设置", (50, 220), 304 + h1, fm.get("HKFY.ttf", 40), align="center")

    # await img.stretch((730, 1377), dmg_img.height + 667, "height")
    await img.paste(dmg_img, (42, 370 + h1))

    body2 = deepcopy(orange_body)
    await body2.stretch((5, body2.width - 5), orange_line.width - 10, "width")
    await body2.stretch((5, body2.height - 5), dmg_img.height - 5, "height")
    await img.paste(body2, (40, 370 + h1))

    return MessageSegment.image(img.save_to_io())


async def draw_weight_pic(dmg_list: list[DMG]) -> ShowImage:
    """
    绘制权重设置图片
    @params
        dmg_list: 权重列表
    @return: 权重设置图片
    """
    height = 120 * len(dmg_list)
    img = ShowImage(size=(1002, height - 60), color=(0, 0, 0, 0), mode="RGBA")

    await img.draw_line((90, 0), (90, 60), (0, 0, 0, 100), 2)
    await img.draw_line((800, 0), (800, 60), (0, 0, 0, 100), 2)
    await img.text(
        "D0", (0, 90), (0, 60), fm.get("hywh.ttf", 30), color="black", align="center"
    )
    await img.text(
        dmg_list[0].name,
        (90, 800),
        (0, 60),
        fm.get("hywh.ttf", 30),
        color="black",
        align="center",
    )
    await img.text(
        dmg_list[0].weight,
        (800, 1000),
        (0, 60),
        fm.get("hywh.ttf", 30),
        color="black",
        align="center",
    )

    for i, dmg in enumerate(dmg_list[1:], 1):
        await img.draw_line((0, 120 * i - 60), (1002, 120 * i - 60), (0, 0, 0, 100), 2)
        await img.draw_line((90, 120 * i - 60), (90, 120 * i + 60), (0, 0, 0, 100), 2)
        await img.text(
            f"D{i}",
            (15, 90),
            120 * i - 16,
            fm.get("hywh.ttf", 30),
            color="black",
            align="center",
        )
        await img.draw_line((90, 120 * i), (800, 120 * i), (0, 0, 0, 100), 2)
        await img.draw_line((180, 120 * i - 60), (180, 120 * i), (0, 0, 0, 100), 2)
        await img.draw_line((800, 120 * i - 60), (800, 120 * i + 60), (0, 0, 0, 100), 2)

        await img.text(
            dmg.source,
            (90, 180),
            (120 * i - 60, 120 * i),
            fm.get("hywh.ttf", 30),
            color="black",
            align="center",
        )
        await img.text(
            dmg.name,
            (180, 800),
            (120 * i - 60, 120 * i),
            fm.get("hywh.ttf", 30),
            color="black",
            align="center",
        )
        await img.text(
            dmg.weight,
            (800, 1002),
            (120 * i - 60, 120 * i + 60),
            fm.get("hywh.ttf", 36),
            color="black",
            align="center",
        )

        await img.text(
            dmg.dsc,
            (90, 800),
            (120 * i, 120 * i + 60),
            fm.get("hywh.ttf", 30),
            color="black",
            align="center",
        )

    return img


async def draw_setting_pic(buff_list: list[BuffInfo]) -> ShowImage:
    """
    绘制设置图片
    @params
        buff_list: 增益列表
    @return: 设置图片
    """
    height = 180 * len(buff_list)
    img = ShowImage(size=(1002, height), color=(0, 0, 0, 0), mode="RGBA")

    i = 0
    for buff in buff_list:
        await img.draw_line((90, 60 + 180 * i), (1002, 60 + 180 * i), (0, 0, 0, 100), 2)
        await img.draw_line((90, 180 * i), (90, 180 * (i + 1)), (0, 0, 0, 100), 2)
        await img.text(
            f"W{i + 1}",
            (15, 90),
            76 + 180 * i,
            fm.get("hywh.ttf", 28),
            color="black",
        )
        await img.draw_line((300, 180 * i), (300, 60 + 180 * i), (0, 0, 0, 100), 2)
        await img.draw_line((850, 180 * i), (850, 60 + 180 * i), (0, 0, 0, 100), 2)
        await img.text(
            buff.source,
            (90, 300),
            (180 * i, 60 + 180 * i),
            fm.get("hywh.ttf", 28),
            color="black",
            align="center",
        )
        await img.text(
            buff.name,
            (300, 850),
            (180 * i, 60 + 180 * i),
            fm.get("hywh.ttf", 30),
            color="black",
            align="center",
        )

        await img.text(
            buff.setting.state,
            (850, 1002),
            (180 * i, 60 + 180 * i),
            fm.get("Yozai-Bold.ttf", 30),
            color="black",
            align="center",
        )

        await img.text(
            buff.setting.dsc,
            (90, 1002),
            (60 + 180 * i, 180 * (i + 1)),
            fm.get("Yozai-Bold.ttf", 24),
            color="black",
            align="center",
        )

        await img.draw_line(
            (0, 180 * (i + 1)),
            (1002, 180 * (i + 1)),
            (0, 0, 0, 100),
            2,
        )
        i += 1

    return img
