from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create a global SQLAlchemy instance
db = SQLAlchemy()
login_manager = LoginManager()
