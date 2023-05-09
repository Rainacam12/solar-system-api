from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# give us access to db ops
db = SQLAlchemy()
migrate = Migrate()

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    # if we're not in our testing environment
    if not test_config: 
    # set up the database
        # development environment confirguration
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # gets the variable and its value from .env
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else: 
        # test environment configuration 
        # if there is a test config passed in,
        # this means we're trying to test the app,
        # confirgures the test settings
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # "which database am i looking at" = specify which database we're pointing to
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    # connect the db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import planet_bp, moon_bp
    app.register_blueprint(planet_bp)
    app.register_blueprint(moon_bp)
    

    # import so db can see the model
    from app.models.planet import Planet
    from app.models.moon import Moon
    return app
