from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
SRC_DIR = APP_DIR.parent
PROJECT_DIR = SRC_DIR.parent

DATA_DIR = PROJECT_DIR / "data"
DATABASE_FILE = DATA_DIR / "lubanovic.db"
