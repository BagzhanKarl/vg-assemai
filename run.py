import os
from app import create_app

# Определяем текущую среду
env = os.getenv('FLASK_ENV', 'development')


# Создаем приложение
app = create_app(env)

@app.route('/check')
def check_work():
    return 'Hello, World!'

if __name__ == "__main__":

    app.run()
