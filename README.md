# Nahidabot
---

## 自我介绍
这里是纳西妲！基于虚空知识制作的小机器人，一个圣遗物及伤害自定义定量评分系统，基于Nonebot框架开发

## 版本更新
[历史更新](/docs/HISTORY.md)
#### v2.1.0a

- 更新角色面板卡片显示
- 更新角色设置卡片显示
- 允许更改角色设置
- 修改账号绑定逻辑
- 补全文档
- 加入更新检测命令
- 新增
  - 角色：甘雨、神子、钟离、班尼特
- 修复一个评分bug，导致充能计算有误
- 修复一个评分bug，导致充能属性被严重低估
- 增加刷新命令（避免经常爬ENKA的资源）
## TODO List

 - [ ] 针对角色不同培养方式，加入流派选择的选项
 - [ ] 卡片美化

## 评分说明
  [评分文档](/docs/install.md)

## 安装方法
  [安装文档](/docs/install.md)

## 指令集
  **绑定 [uid]：绑定原神账号**
  
  一个QQ号原则上只绑定一个uid，换绑只需要重新输入这个命令就可以，换绑后，原uid的记录会被保留
  **更新面板：更新展柜上的角色信息**

  **nhd [角色名]：查询角色面板**
  
  **set [角色名]：更改角色设置**

  [序号1]-[更改值1] 空格 [序号2]-[更改值2]...

  例：W0-200 S1-0

## 开源致谢

- 数据来源：[Enka.network](https://enka.network/)
- 游戏资源：[GitHub - mrwan200/enkanetwork.py-data: Repository for fetch data from GenshinData to use EnkaNetwork.py python library.](https://github.com/mrwan200/enkanetwork.py-data)
- [悠哉字体 / Yozai Font](https://github.com/lxgw/yozai-font)
- [975 圆体 / 975 Maru](https://github.com/lxgw/975maru)
- 图片CDN：[GitHub - jsdelivr/jsdelivr: A free, fast, and reliable Open Source CDN for npm, GitHub, Javascript, and ESM](https://github.com/jsdelivr/jsdelivr)
- QQ协议及框架：[Nonebot2-跨平台 Python 异步机器人框架 ](https://github.com/nonebot/nonebot2)
- 部分源码、资源及功能参考：[小派蒙|LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon)