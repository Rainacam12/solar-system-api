from flask import Flask


def create_app():
    app = Flask(__name__)

    from .routes import planet_bp
    app.register_blueprint(planet_bp)
    return app
