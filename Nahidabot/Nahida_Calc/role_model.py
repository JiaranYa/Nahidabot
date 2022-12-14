from nonebot.utils import run_sync

from Nahidabot.database.models import PropList, RoleBasicInfo
from Nahidabot.utils.classmodel import DMG, BuffInfo, Role, RoleInfo

from .dmg_model import DMGCalc, reserve_setting, reserve_weight
from .relics import artifacts, artifacts_setting

# from .role import role_buff, role_dmg
from .weapon import weapon_buff, weapon_setting


class RoleModel(Role):
    """角色计算模型"""

    prebuff: list[BuffInfo] = []
    """圣遗物面板增益"""

    @run_sync
    def get_recharge(self):
        """充能（用于圣遗物计算）"""
        calc = DMGCalc(self.fight_prop, self.info.level) + self.prebuff
        return calc.recharge

    propbuff: list[BuffInfo] = []
    """面板型增益"""
    transbuff: list[BuffInfo] = []
    """转移型增益"""
    dmgbuff: list[BuffInfo] = []
    """伤害型增益"""

    async def update_from_database(self, user_qq, uid):
        """从数据库更新"""

        basicinfo: RoleInfo
        (basicinfo,) = await RoleBasicInfo.filter(name=self.name).values_list(
            "info", flat=True
        )
        self.scaling_table = basicinfo.scaling_table

        (roleinfo,) = await PropList.filter(
            user_qq=str(user_qq), uid=uid, role_name=self.name
        ).all()
        self.info = roleinfo.info  # type: ignore
        self.fight_prop = roleinfo.property  # type: ignore
        self.weapon = roleinfo.weapon  # type: ignore
        self.artifacts = roleinfo.artifacts  # type: ignore
        self.party_member = roleinfo.party_member  # type: ignore
        self.buff_list = roleinfo.buff_info  # type: ignore
        self.dmg_list = roleinfo.dmg_info  # type: ignore

    @property
    def calculator(self):
        """战斗实时面板"""
        return (
            DMGCalc(self.fight_prop, self.info.level)
            + self.prebuff
            + self.propbuff
            + self.transbuff
        )

    @property
    def valid_prop(self) -> list[str]:
        """有效属性"""
        return []

    @run_sync
    def setting(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益设置"""
        output: list[BuffInfo] = []
        labels = reserve_setting(buff_list)

        return output

    @run_sync
    def buff(self, buff_list: list[BuffInfo]) -> list[BuffInfo]:
        """增益列表"""
        return buff_list

    @run_sync
    def weight(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害权重"""
        output: list[DMG] = []
        weights = reserve_weight(dmg_list)

        return output

    @run_sync
    def dmg(self, dmg_list: list[DMG]) -> list[DMG]:
        """伤害列表"""
        return dmg_list

    async def get_setting(self):
        """获取自身增益设定"""
        buff_list = self.buff_list.copy()
        self.buff_list = []
        self.buff_list.extend(await self.setting(buff_list))
        self.buff_list.extend(await weapon_setting(self.weapon, self.info, buff_list))
        self.buff_list.extend(
            await artifacts_setting(self.artifacts, buff_list, self.name)
        )

    async def get_buff(self, mode: str):
        """获取自身增益"""
        # 命座、天赋和技能增益
        input_buff: list[BuffInfo] = []
        for buff in self.buff_list:
            if buff.buff_type == mode:
                input_buff.append(buff)
        # 自身增益
        await self.buff(input_buff)
        # 武器增益
        await weapon_buff(input_buff, self.info, self.calculator)
        # 圣遗物增益
        await artifacts(input_buff, self.info, self.calculator)

        if mode == "propbuff":
            self.propbuff.extend(input_buff)
        elif mode == "transbuff":
            self.transbuff.extend(input_buff)
        else:
            self.dmgbuff.extend(input_buff)

        output_buff: list[BuffInfo] = []
        for buff in input_buff:
            if buff.buff_range != "self":
                output_buff.append(buff)
        return output_buff

    async def save_buff(self):
        """保存增益"""
        output: list[BuffInfo] = []
        output.extend(self.propbuff)
        output.extend(self.transbuff)
        output.extend(self.dmgbuff)
        return output

    async def get_partner(self):
        """获取队友"""
        return self.party_member

    async def load_buff(self, input_buff: list[BuffInfo], mode: str):
        """获取外部增益"""
        buffs = []
        for buff in input_buff:
            if self.name not in buff.source:
                buffs.append(buff)

        if mode == "prebuff":
            self.prebuff.extend(buffs)
        elif mode == "propbuff":
            self.propbuff.extend(buffs)
        elif mode == "transbuff":
            self.transbuff.extend(buffs)
        else:
            self.dmgbuff.extend(buffs)

    async def get_dmg(self):
        """获取伤害列表"""
        self.dmg_list = await self.weight(self.dmg_list)
        return await self.dmg(self.dmg_list)
