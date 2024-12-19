from app.config.base import BaseConfig
from app.config.development import DevelopmentConfig
from app.config.testing import TestingConfig
from app.config.production import ProductionConfig

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
