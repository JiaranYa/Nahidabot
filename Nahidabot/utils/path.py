from pathlib import Path

BASE_PATH = Path().cwd() / "Nahidabot"
DATABASE_PATH = BASE_PATH / "database"

VERION_FILE = Path("config/version.toml")
VERSION_PATH = BASE_PATH / VERION_FILE

DB_PATH = DATABASE_PATH / "db.sqlite3"  # 数据库路径
STATIC_PATH = DATABASE_PATH / "static"  # 静态资源
RESOUCE_PATH = BASE_PATH / "resources"  # 大型资源
GRAPHIC_PATH = RESOUCE_PATH / "pics"  # 图片资源
FONT_PATH = RESOUCE_PATH / "fonts"


GRAPHIC_PATH.mkdir(parents=True, exist_ok=True)
FONT_PATH.mkdir(parents=True, exist_ok=True)
AKASHA_STORE_URL = "https://cdn.jsdelivr.net/gh/JiaranYa/Akashastore@master/"
NAHIDABOT_URL = "https://cdn.jsdelivr.net/gh/JiaranYa/Nahidabot@master/"
# GITHUB_URL = "https://github.com/JiaranYa/Nahidabot.git"
