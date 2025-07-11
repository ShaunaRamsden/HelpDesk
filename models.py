from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users' # Explicitly define table name for ForeignKey reference

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)         
    surname = db.Column(db.String(100), nullable=False)    
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Regular') # 'Regular' or 'Admin'

    tickets = db.relationship('Ticket', backref='owner', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, **kwargs):
        super().__init__(**kwargs)
        self.username = username.lower()  # force lowercase

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Ticket(db.Model):
    __tablename__ = 'tickets' # Explicitly define table name for ForeignKey reference

    id = db.Column(db.Integer, primary_key=True)  
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Open')
    department = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    request_type = db.Column(db.String(100), nullable=False)
    other_request_type = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)



    def __repr__(self):
        return f'<Ticket {self.id} - {self.subject}>'