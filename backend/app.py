from flask import Flask
from backend.config import Config
from backend.extensions import db, login_manager, cors
from backend.models import User
from backend.auth_routes import auth_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs("backend/instance", exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    cors.init_app(
        app,
        supports_credentials=True,
        origins=["http://localhost:5500"]
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
