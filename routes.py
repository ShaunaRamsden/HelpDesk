from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime # Import datetime for created_at default

# Assuming these are defined in your project
from extensions import db
from models import User, Ticket
from forms import RegistrationForm, LoginForm, TicketForm, AdminTicketStatusForm, AdminEditUserRoleForm

# Define the blueprint
main = Blueprint('main_blueprint', __name__) # Renamed to avoid conflict with 'main' module name

# --- Routes associated with the 'main' blueprint ---

@main.route('/')
def index():
    """
    Redirects the root URL to the login page.
    """
    return redirect(url_for('main_blueprint.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
   
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main_blueprint.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)

        # Create new user with 'Regular' role by default
        user = User(name=form.name.data, surname=form.surname.data ,username=form.username.data, role='Regular')
        user.set_password(form.password.data)  # Hash the password
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main_blueprint.login'))

    # Flash individual validation errors (e.g., "Passwords must match")
    elif form.errors:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'danger')

    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    If a user is already authenticated, they are redirected to the dashboard.
    """
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main_blueprint.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Authenticate user
        if user and user.check_password(form.password.data):
            login_user(user) # Log the user in
            flash(f'Logged in successfully as {user.username}.', 'success')
            return redirect(url_for('main_blueprint.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    """
    Logs out the current user.
    Requires user to be logged in.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_blueprint.login'))

@main.route('/dashboard')
@login_required
def dashboard():
 
    if current_user.role == 'Admin':
        # Admins see global stats
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='Open').count()
        resolved_tickets = Ticket.query.filter_by(status='Resolved').count()

        recent_ticket = Ticket.query.order_by(Ticket.created_at.desc()).first()

    else:
        # Regular users see only their own stats
        total_tickets = Ticket.query.filter_by(user_id=current_user.id).count()
        open_tickets = Ticket.query.filter_by(user_id=current_user.id, status='Open').count()
        resolved_tickets = Ticket.query.filter_by(user_id=current_user.id, status='Resolved').count()

        recent_ticket = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).first()

    return render_template('dashboard.html',
                           total_tickets=total_tickets,
                           open_tickets=open_tickets,
                           resolved_tickets=resolved_tickets,
                           recent_ticket=recent_ticket)

@main.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    """
    Allows a logged-in user to create a new ticket.
    """
    form = TicketForm()
    if form.validate_on_submit():
        # Handle 'Other' request type
        other_request_type = form.other_request_type.data if form.request_type.data == 'Other' else None
        ticket = Ticket(
            department=form.department.data,
            subject=form.subject.data,
            priority=form.priority.data,
            request_type=form.request_type.data,
            other_request_type=other_request_type,
            description=form.description.data,
            user_id=current_user.id, # Assign the current user as the owner
            status='Open', # New tickets are always 'Open' by default
            created_at=datetime.utcnow() # Set creation timestamp
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been submitted!', 'success')
        return redirect(url_for('main_blueprint.view_tickets'))
    return render_template('create_ticket.html', form=form)

@main.route('/view_tickets')
@login_required
def view_tickets():
    """
    Displays all tickets submitted by the current user.
    """
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('view_tickets.html', tickets=tickets)

@main.route('/manage_tickets', methods=['GET'])
@login_required
def manage_tickets():
    """
    Admin-only route to view and manage all tickets.
    Admins can see all tickets and their current status.
    """
    if current_user.role != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    tickets = Ticket.query.all()
    # Create a dictionary of forms, one for each ticket, pre-populated with current status
    ticket_status_forms = {ticket.id: AdminTicketStatusForm(status=ticket.status) for ticket in tickets}

    return render_template('manage_tickets.html', tickets=tickets, ticket_status_forms=ticket_status_forms)

@main.route('/update_ticket_status/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    """
    Admin-only route to update the status of a specific ticket.
    """
    if current_user.role != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)
    form = AdminTicketStatusForm() # Form for status update

    if form.validate_on_submit():
        ticket.status = form.status.data
        db.session.commit()
        flash(f'Ticket {ticket.id} status updated to {ticket.status}.', 'success')
    else:
        # If validation fails, it might be due to CSRF token or invalid status choice
        flash('Failed to update ticket status. Please try again.', 'danger')

    return redirect(url_for('main_blueprint.manage_tickets'))

@main.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    """
    Allows the ticket owner or an Admin to edit ticket details.
    """
    ticket = Ticket.query.get_or_404(ticket_id)

    # Only the ticket owner or an Admin can edit the full ticket details
    if not (current_user.id == ticket.user_id or current_user.role == 'Admin'):
        flash('You do not have permission to edit this ticket.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    form = TicketForm(obj=ticket) # Pre-populate form with existing ticket data

    if form.validate_on_submit():
        form.populate_obj(ticket) # Populates ticket object with form data
        # Special handling for 'Other' request type
        if form.request_type.data == 'Other' and form.other_request_type.data:
            ticket.other_request_type = form.other_request_type.data
        elif form.request_type.data != 'Other':
            ticket.other_request_type = None # Clear if "Other" is no longer selected
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        # Redirect based on user role after update
        if current_user.role == 'Admin':
            return redirect(url_for('main_blueprint.manage_tickets'))
        else:
            return redirect(url_for('main_blueprint.view_tickets'))

    # Pre-populate 'Other' text field if 'Other' is the current request type on GET request
    if request.method == 'GET' and ticket.request_type == 'Other' and ticket.other_request_type:
        form.other_request_type.data = ticket.other_request_type

    return render_template('edit_ticket.html', form=form, ticket=ticket)

@main.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    """
    Admin-only route to delete a ticket.
    """
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    db.session.delete(ticket)
    db.session.commit()
    flash(f'Ticket {ticket.id} deleted successfully.', 'success')
    return redirect(url_for('main_blueprint.manage_tickets'))

@main.route('/manage_users')
@login_required
def manage_users():
    """
    Admin-only route to view and manage all users.
    """
    if current_user.role != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    users = User.query.all()
    return render_template('manage_users.html', users=users)

@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """
    Admin-only route to delete a user.
    Prevents an admin from deleting their own account.
    Also deletes all tickets associated with the user.
    """
    if current_user.role != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    # Prevent an admin from deleting their own account
    if current_user.id == user_id:
        flash('You cannot delete your own user account.', 'danger')
        return redirect(url_for('main_blueprint.manage_users'))

    user_to_delete = User.query.get_or_404(user_id)

    # Store username for flash message before deletion
    username = user_to_delete.username

    # Delete all tickets associated with the user first to avoid integrity errors
    Ticket.query.filter_by(user_id=user_to_delete.id).delete()
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'User "{username}" and associated tickets deleted successfully.', 'success')
    return redirect(url_for('main_blueprint.manage_users'))

@main.route('/edit_user_role/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user_role(user_id):
    """
    Admin-only route to edit a user's role.
    Prevents an admin from changing their own role from this page.
    """
    if current_user.role != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main_blueprint.dashboard'))

    user = User.query.get_or_404(user_id)

    # Prevent an admin from changing their own role (good practice)
    if current_user.id == user.id:
        flash("You cannot change your own role from this page. Please contact another admin if needed.", 'warning')
        return redirect(url_for('main_blueprint.manage_users'))

    form = AdminEditUserRoleForm(obj=user) # Pre-populate form with current role

    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash(f'Role for user "{user.username}" updated to "{user.role}".', 'success')
        return redirect(url_for('main_blueprint.manage_users'))

    return render_template('edit_user_role.html', form=form, user=user)


@main.route('/view_ticket/<int:ticket_id>')  # If your blueprint is 'main'
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    # Access control
    if current_user.role != 'Admin' and ticket.user_id != current_user.id:
        flash("You don't have permission to view this ticket.", "danger")
        return redirect(url_for('main.view_tickets'))
    return render_template('view_ticket.html', ticket=ticket)