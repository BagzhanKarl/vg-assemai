from flask import Flask
from app.db.database import db
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

migrate = Migrate()
load_dotenv()

def create_app(env='development'):
    from app.config import config_map

    app = Flask(__name__)
    app.config.from_object(config_map[env])

    # Инициализация базы данных
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация роутеров
    from app.routers import register_routers
    register_routers(app)

    return app
