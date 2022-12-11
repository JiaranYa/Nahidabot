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
    PropInfo,
    Role,
    SkillMultiplier,
)

from ..dmg_model import reserve_setting
from .role_model import RoleModel


class Xingqiu(RoleModel):
    name = "行秋"

    def C2(self, buff_info: BuffInfo):
        """天青现虹"""
        setting = buff_info.setting

        if setting.label == "0":
            setting.state = "×"
        else:
            setting.state = "✓"
            buff_info.buff = Buff(
                dsc="剑雨攻击的敌人，水抗-15％，持续4秒",
                elem_type="hydro",
                resist_reduction=0.15,
            )

    def C4(self, buff_info: BuffInfo):
        """孤舟斩蛟"""
        setting = buff_info.setting

    def skill_E(self, buff_info: BuffInfo):
        """古华剑·画雨笼山"""

    def skill_Q(self, buff_info: BuffInfo):
        """古华剑·裁雨留虹"""

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
                        label=labels.get("天青现虹", "1"),
                    ),
                )
            )
            if self.talent.constellation >= 4 and is_self:
                output.append(
                    BuffInfo(
                        source=f"{self.name}-C4",
                        name="孤舟斩蛟",
                        setting=BuffSetting(
                            dsc="古华剑·裁雨留虹持续期间||⓪（×）：无增益；①（✓）：古华剑·画雨笼山倍率×0.5",
                            label=labels.get("孤舟斩蛟", "1"),
                        ),
                    )
                )
        return output

    async def buff(self, buff_list: list[BuffInfo]):

        for buff in buff_list:
            if buff.name == "天青现虹":
                self.C2(buff)
            if buff.name == "孤舟斩蛟":
                self.C4(buff)

        return buff_list
