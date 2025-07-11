README - Help Desk Ticket System
================================

Author: Shauna Ramsden
Course: Software Engineering & Agile (QAC020N227K)
Date: 11/07/2025

Description:
------------
The Help Desk Ticket System is a Flask-based web application that allows users to register, log in, and submit technical support tickets. Admin users have full access to view, edit, and delete all submitted tickets, while regular users can only manage their own.

This application demonstrates the use of the Flask web framework, SQLite database, secure user authentication, and a styled user interface using HTML, CSS, and Flask-WTF forms.

Features:
---------
- User Registration and Login
- Role-based Access Control (Admin vs Regular Users)
- Create, Edit, View, and Delete Support Tickets
- Flash messages for success and error feedback
- Password hashing for secure authentication
- Styled login and registration pages with background image

Technology Stack:
-----------------
- Python 3.x
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy (ORM)
- SQLite (Database)
- Jinja2 (Templating)
- HTML5 & CSS3

Project Structure:
------------------
HELPDESK_APP/
├── __pycache__/            # Python bytecode cache directory
├── .venv/                  # Python Virtual Environment directory
├── instance/               # Instance-specific files, typically not version controlled
│   └── helpdesk.db         # SQLite database file
├── static/                 # Directory for static assets (CSS, JavaScript, images)
│   ├── css/                # Subdirectory for CSS files
│   │   └── style.css       # Main stylesheet for the application
│   └── images/             # Subdirectory for image assets
├── templates/              # Directory for HTML Jinja2 templates
│   ├── base.html           # Base template for consistent page structure
│   ├── create_ticket.html  # Template for creating new tickets
│   ├── dashboard.html      # User dashboard template
│   ├── edit_ticket.html    # Template for editing existing tickets
│   ├── edit_user_role.html # Template for administrators to edit user roles
│   ├── login.html          # User login page template
│   ├── manage_tickets.html # Template for administrators to manage all tickets
│   ├── manage_users.html   # Template for administrators to manage users
│   ├── register.html       # User registration page template
│   └── view_tickets.html   # Template for viewing specific tickets or user's tickets
├── README.txt              # Project README file (text format)
├── requirements.txt        # Lists Python package dependencies for the project
├── .gitignore              # Git ignore file, specifies files/directories to exclude from version control
├── create_db.py            # Script to initialize and populate the database
├── extensions.py           # Defines and initializes Flask extensions (e.g., SQLAlchemy, Flask-Login)
├── forms.py                # Defines Flask-WTF forms for web input
├── main.py                 # Main application entry point, creates and runs the Flask app
├── models.py               # Defines database models (e.g., User, Ticket)
└── routes.py               # Defines URL routes and their corresponding view functions

Setup Instructions:
-------------------
1. Ensure Python 3.x is installed on your system.
2. Create and activate a virtual environment (optional but recommended):

   Windows:
   > python -m venv venv
   > venv\Scripts\activate

   macOS/Linux:
   $ python3 -m venv venv
   $ source venv/bin/activate

3. Install required packages:
   > pip install -r requirements.txt

4. Initialize the database:
   > python create_db.py

5. Run the application:
   > python main.py
   or
   > flask run

6. Visit the application in your browser at:
   http://localhost:5000

Admin Role Notes:
-----------------
By default, users are registered with the role "regular". To promote a user to admin, manually update the database or modify the registration logic.

Admin Credentials:
------------------
Username: Admin
Password: Password321!

Security:
---------
- Passwords are hashed using Werkzeug security functions.
- Routes are protected using Flask-Login decorators.
- Flash messages provide feedback on login, logout, and form submissions.

Credits:
--------
This project was developed as part of the Software Engineering & Agile module coursework.

