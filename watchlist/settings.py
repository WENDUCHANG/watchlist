import os,sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SQLITE_PREFIX = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'


class BaseConfig:  # 创建配置基类
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')


class DevelopmentConfig(BaseConfig):  # 开发配置
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX + str(BASE_DIR / 'data-dev.db')


class TestingConfig(BaseConfig):  # 测试配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):  # 生产配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLITE_PREFIX + str(BASE_DIR / 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}