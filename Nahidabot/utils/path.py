from pathlib import Path

BASE_PATH = Path().cwd() / "Nahidabot"
RESOURCE_PATH = BASE_PATH / "database"

VERION_FILE = Path("config/version.toml")
VERSION_PATH = BASE_PATH / VERION_FILE

DB_PATH = RESOURCE_PATH / "db.sqlite3"  # 数据库路径
STATIC_PATH = RESOURCE_PATH / "static"  # 静态资源
GRAPHIC_PATH = STATIC_PATH / "graphic"  # 图片资源
FONT_PATH = STATIC_PATH / "font"

GRAPHIC_PATH.mkdir(parents=True, exist_ok=True)

AKASHA_STORE_URL = "https://cdn.jsdelivr.net/gh/JiaranYa/Akashastore@master/"
NAHIDABOT_URL = "https://cdn.jsdelivr.net/gh/JiaranYa/Nahidabot@master/"
GITHUB_URL = "https://github.com/JiaranYa/Nahidabot.git"
