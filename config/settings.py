import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('SERVER')}/{os.getenv('DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "sua_chave_muito_secreta"
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = False