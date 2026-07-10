import os

from pathlib import Path

from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
SRC_DIR = APP_DIR.parent
PROJECT_DIR = SRC_DIR.parent

DATA_DIR = PROJECT_DIR / "data"
DATABASE_FILE = DATA_DIR / "lubanovic.db"

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(str(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
