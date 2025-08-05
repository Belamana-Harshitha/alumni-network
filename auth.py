"""
Authentication routes and session management
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import User
import logging

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name', '').strip()
        graduation_year = request.form.get('graduation_year')
        department = request.form.get('department', '').strip()
        current_company = request.form.get('current_company', '').strip()
        location = request.form.get('location', '').strip()
        user_type = request.form.get('user_type', 'alumni')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif User.get_by_username(username):
            errors.append('Username already exists')
        
        if not email:
            errors.append('Email is required')
        elif User.get_by_email(email):
            errors.append('Email already exists')
        
        if not password:
            errors.append('Password is required')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if not full_name:
            errors.append('Full name is required')
        
        # Try to convert graduation year to integer
        if graduation_year:
            try:
                graduation_year = int(graduation_year)
                if graduation_year < 1950 or graduation_year > 2030:
                    errors.append('Please enter a valid graduation year')
            except ValueError:
                errors.append('Graduation year must be a number')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            user = User(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                graduation_year=graduation_year,
                department=department,
                current_company=current_company,
                location=location,
                user_type=user_type
            )
            
            flash('Registration successful! Please log in.', 'success')
            logging.info(f'New user registered: {username}')
            return redirect(url_for('login'))
            
        except Exception as e:
            logging.error(f'Registration error: {str(e)}')
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        # Find user
        user = User.get_by_username(username)
        
        if user and user.check_password(password) and user.is_active:
            # Set session
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            logging.info(f'User logged in: {username}')
            
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            logging.warning(f'Failed login attempt for username: {username}')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'Unknown')
    session.clear()
    flash('You have been logged out successfully', 'info')
    logging.info(f'User logged out: {username}')
    return redirect(url_for('index'))

def login_required(f):
    """Decorator to require login for protected routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        
        if session.get('user_type') != 'admin':
            flash('Admin privileges required', 'error')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get the current logged-in user"""
    if 'user_id' in session:
        return User.get_by_id(session['user_id'])
    return None
