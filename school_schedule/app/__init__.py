from flask import Flask
from config import Config
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.schedule import schedule_bp
    from .routes.directories import directories_bp
    from .routes.backup import backup_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(directories_bp)
    app.register_blueprint(backup_bp)
    with app.app_context():
        from .models import models
        db.create_all()
        models.seed_data()
    return app
