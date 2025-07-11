from main import create_app
from extensions import db
from models import User, Ticket
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    print("Database and tables created successfully.")

    # Check if admin user already exists
    existing_admin = User.query.filter_by(username='Admin').first()
    
    if not existing_admin:
        admin_user = User(
            name= 'Admin',
            surname= 'Administrator',
            username='Admin',
            password_hash=generate_password_hash('Password321!'),
            role='Admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

