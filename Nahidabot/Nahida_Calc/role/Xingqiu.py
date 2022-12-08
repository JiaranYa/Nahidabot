from typing import Optional

import numpy as np

from Nahidabot.utils.classmodel import (
    DMG,
    Buff,
    BuffInfo,
    BuffSetting,
    DMGBonus,
    FightProp,
    FixValue,
    Multiplier,
    PropBuff,
    PropInfo,
    Role,
    SkillMultiplier,
)

from ..dmg_model import RoleModel, reserve_setting


class Xingqiu(RoleModel):
    name = "行秋"

    def C2(self):
        """"""
        return []

    pass

    async def setting(self, buff_list: list[BuffInfo], is_self: bool = True):
        output: list[BuffInfo] = []
        labels = reserve_setting(buff_list)

        if self.talent.constellation >= 2:
            output.append(
                BuffInfo(
                    source=f"{self.name}-C2",
                    name="天青现虹",
                    range="all",
                    setting=BuffSetting(
                        dsc="敌人受到剑雨攻击4s内||⓪（×）：无增益；①（✓）：水抗-15%",
                        label=labels.get("天青现虹", 1),
                    ),
                )
            )
            if self.talent.constellation >= 4 and is_self:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-C4",
                        name="孤舟斩蛟",
                        setting=BuffSetting(
                            dsc="元素爆发持续期间，E||⓪（×）：无增益；①（✓）：倍率×0.5",
                            label=labels.get("孤舟斩蛟", 1),
                        ),
                    )
                )
        return output

    async def buff(self, buff_list: list[BuffInfo], type: str):
        pass


async def Xing():
    pass


async def Xingqiu_buff():
    pass


async def Xingqiu_setting():
    pass
