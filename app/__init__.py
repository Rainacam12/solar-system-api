from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# give us access to db ops
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # set up the database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/solar_system_development'

    # connect the db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import planet_bp
    app.register_blueprint(planet_bp)

    # import so db can see the model
    from app.models.planet import Planet
    return app
