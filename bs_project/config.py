import os

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'development-secret'
    DEBUG = os.getenv("DEBUG") or False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE")
    JWT_TOKEN_LOCATION = os.getenv("JWT_TOKEN_LOCATION")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)