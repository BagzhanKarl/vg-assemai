import os
from app import create_app

print(f"FLASK_ENV: {os.getenv('FLASK_DEBUG')}")
# Определяем текущую среду
env = os.getenv('FLASK_ENV', 'development')

# Создаем приложение
app = create_app(env)

if __name__ == "__main__":
    app.run()
