from app.routers.start import start_bp

def register_routers(app):
    app.register_blueprint(start_bp, url_prefix="/start")
