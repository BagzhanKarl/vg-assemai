from app.routers.start import start_bp
from app.routers.main import main_bp
from app.routers.ui import ui_bp

def register_routers(app):
    app.register_blueprint(ui_bp)
    app.register_blueprint(start_bp, url_prefix="/start")
    app.register_blueprint(main_bp)
