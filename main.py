from flask import Flask
from extensions import db, login_manager # Assuming extensions.py defines db and login_manager
from models import User # Only User model needed for user_loader
from routes import main as main_blueprint # Import the blueprint from routes.py

# factory pattern function
def create_app():
    app = Flask(__name__)

    # set configuration variable
    app.config['SECRET_KEY'] = 'your_secret_key_here' # IMPORTANT: Change this to a strong, unique secret key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main_blueprint.login' # Specify the login view for Flask-Login
    login_manager.login_message_category = 'info' # Category for login required message

    # Register the blueprint
    app.register_blueprint(main_blueprint)

    return app

# User authentication loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user from the database given their user ID.
    This function is required by Flask-Login.
    """
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app = create_app()
    # Create database tables within the application context
    with app.app_context():
        db.create_all()
    app.run(debug=True) # Run the Flask application in debug mode
