import os
from app import create_app
from app.celery_start import start_scheduler
# Определяем текущую среду
env = os.getenv('FLASK_ENV', 'development')


# Создаем приложение
app = create_app(env)



if __name__ == "__main__":
    start_scheduler()
    app.run()
