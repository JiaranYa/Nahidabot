from typing import Optional

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
from ..role_model import RoleModel


class Bennett(RoleModel):
    name = "班尼特"
