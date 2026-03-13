from flask import Flask
from flask_migrate import Migrate
from models import db
from config import config
from routes.itineraries_blueprint import itineraries_bp

def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates')

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(itineraries_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

# For development server
if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
