from flask  import Blueprint

start_bp = Blueprint('start', __name__)
@start_bp.route('/')
def index():
    return "Все установлено и работает!"