import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "app")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "apppass")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "decanat")
    SESSION_PROTECTION = "strong"
