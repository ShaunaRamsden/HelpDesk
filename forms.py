from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

class RegistrationForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    surname = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')

    def validate(self, extra_validators=None):
        # Normalize username to lowercase for case-insensitive handling
        if self.username.data:
            self.username.data = self.username.data.lower()
        return super().validate(extra_validators)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate(self, extra_validators=None):
        # Normalize username to lowercase for case-insensitive login
        if self.username.data:
            self.username.data = self.username.data.lower()
        return super().validate(extra_validators)

class TicketForm(FlaskForm):
    department = SelectField('Department', choices=[
        ('IT Support', 'IT Support'),
        ('Human Resources', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Operations', 'Operations'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Customer Service', 'Customer Service'),
        ('Facilities', 'Facilities')
    ], validators=[DataRequired()])
    
    subject = StringField('Subject', validators=[DataRequired(), Length(max=150)])
    
    priority = SelectField('Priority', choices=[
        ('1 - Critical', '1 - Critical'),
        ('2 - High', '2 - High'),
        ('3 - Medium', '3 - Medium'),
        ('4 - Low', '4 - Low'),
        ('5 - Planning', '5 - Planning')
    ], validators=[DataRequired()])
    
    request_type = SelectField('Request Type', choices=[
        ('Bug Report', 'Bug Report'),
        ('Feature Request', 'Feature Request'),
        ('Technical Issue', 'Technical Issue'),
        ('Account Issue', 'Account Issue'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    
    other_request_type = StringField('If "Other", please specify', validators=[Optional()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit Ticket')

class AdminTicketStatusForm(FlaskForm): 
    status = SelectField('Status', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed') 
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')

class AdminEditUserRoleForm(FlaskForm):
    role = SelectField('User Role', choices=[
        ('Regular', 'Regular'),
        ('Admin', 'Admin')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Role')
