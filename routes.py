"""
Main application routes
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import User, Job, Event, Message
from auth import login_required, get_current_user
from datetime import datetime
import logging

@app.route('/')
def index():
    """Home page"""
    # Get recent jobs and events for display
    recent_jobs = Job.get_all_jobs()[:3]  # Show 3 most recent jobs
    recent_events = Event.get_all_events()[:3]  # Show 3 most recent events
    
    return render_template('index.html', 
                         recent_jobs=recent_jobs, 
                         recent_events=recent_events)

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    # Get user's recent activity
    user_jobs = [job for job in Job.get_all_jobs() if job.posted_by_id == current_user.id]
    user_events = [event for event in Event.get_all_events() if event.organized_by_id == current_user.id]
    user_messages = Message.get_user_messages(current_user.id)[:5]  # Recent 5 messages
    
    return render_template('dashboard.html',
                         user=current_user,
                         user_jobs=user_jobs,
                         user_events=user_events,
                         user_messages=user_messages)

@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    """View user profile"""
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('search'))
    
    current_user = get_current_user()
    is_own_profile = current_user and current_user.id == user_id
    
    return render_template('profile.html', user=user, is_own_profile=is_own_profile)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Update profile information
        current_user.full_name = request.form.get('full_name', '').strip()
        current_user.department = request.form.get('department', '').strip()
        current_user.current_company = request.form.get('current_company', '').strip()
        current_user.location = request.form.get('location', '').strip()
        
        # Handle graduation year
        graduation_year = request.form.get('graduation_year')
        if graduation_year:
            try:
                current_user.graduation_year = int(graduation_year)
            except ValueError:
                flash('Invalid graduation year', 'error')
                return render_template('edit_profile.html', user=current_user)
        
        flash('Profile updated successfully!', 'success')
        logging.info(f'Profile updated for user: {current_user.username}')
        return redirect(url_for('profile', user_id=current_user.id))
    
    return render_template('edit_profile.html', user=current_user)

@app.route('/search')
@login_required
def search():
    """Search and filter alumni"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    # Get search parameters
    query = request.args.get('q', '').strip()
    department = request.args.get('department', '').strip()
    company = request.args.get('company', '').strip()
    graduation_year = request.args.get('graduation_year', '').strip()
    
    # Get all users except current user
    all_users = [user for user in User.get_all_users() 
                 if user.id != current_user.id and user.is_active]
    
    # Apply filters
    filtered_users = all_users
    
    if query:
        filtered_users = [user for user in filtered_users 
                         if query.lower() in user.full_name.lower() or
                            query.lower() in (user.username or '').lower()]
    
    if department:
        filtered_users = [user for user in filtered_users 
                         if user.department and department.lower() in user.department.lower()]
    
    if company:
        filtered_users = [user for user in filtered_users 
                         if user.current_company and company.lower() in user.current_company.lower()]
    
    if graduation_year:
        try:
            year = int(graduation_year)
            filtered_users = [user for user in filtered_users 
                             if user.graduation_year == year]
        except ValueError:
            pass
    
    # Get unique departments and companies for filter dropdowns
    departments = list(set([user.department for user in all_users 
                           if user.department]))
    companies = list(set([user.current_company for user in all_users 
                         if user.current_company]))
    
    return render_template('search.html',
                         users=filtered_users,
                         departments=sorted(departments),
                         companies=sorted(companies),
                         search_params={
                             'q': query,
                             'department': department,
                             'company': company,
                             'graduation_year': graduation_year
                         })

@app.route('/jobs')
@login_required
def jobs():
    """Job listings page"""
    all_jobs = Job.get_all_jobs()
    # Sort by creation date (newest first)
    all_jobs.sort(key=lambda x: x.created_at, reverse=True)
    
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    """Post a new job"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        company = request.form.get('company', '').strip()
        location = request.form.get('location', '').strip()
        job_type = request.form.get('job_type', 'full-time')
        salary_range = request.form.get('salary_range', '').strip()
        
        # Validation
        if not all([title, description, company, location]):
            flash('Please fill in all required fields', 'error')
            return render_template('post_job.html')
        
        # Create new job
        job = Job(
            title=title,
            description=description,
            company=company,
            location=location,
            posted_by_id=current_user.id,
            job_type=job_type,
            salary_range=salary_range if salary_range else None
        )
        
        flash('Job posted successfully!', 'success')
        logging.info(f'New job posted by {current_user.username}: {title}')
        return redirect(url_for('jobs'))
    
    return render_template('post_job.html')

@app.route('/events')
@login_required
def events():
    """Events listing page"""
    all_events = Event.get_all_events()
    # Sort by date (upcoming first, then by creation date)
    all_events.sort(key=lambda x: (x.date, x.created_at))
    
    return render_template('events.html', events=all_events)

@app.route('/post_event', methods=['GET', 'POST'])
@login_required
def post_event():
    """Post a new event"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        date_str = request.form.get('date', '').strip()
        location = request.form.get('location', '').strip()
        
        # Validation
        if not all([title, description, date_str, location]):
            flash('Please fill in all required fields', 'error')
            return render_template('post_event.html')
        
        # Parse date
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'error')
            return render_template('post_event.html')
        
        # Create new event
        event = Event(
            title=title,
            description=description,
            date=event_date,
            location=location,
            organized_by_id=current_user.id
        )
        
        flash('Event posted successfully!', 'success')
        logging.info(f'New event posted by {current_user.username}: {title}')
        return redirect(url_for('events'))
    
    return render_template('post_event.html')

@app.route('/messages')
@login_required
def messages():
    """Messages page"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    user_messages = Message.get_user_messages(current_user.id)
    
    return render_template('messages.html', messages=user_messages)

@app.route('/send_message/<recipient_id>', methods=['GET', 'POST'])
@login_required
def send_message(recipient_id):
    """Send a message to another user"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    recipient = User.get_by_id(recipient_id)
    if not recipient:
        flash('Recipient not found', 'error')
        return redirect(url_for('search'))
    
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()
        
        if not subject or not content:
            flash('Subject and message content are required', 'error')
            return render_template('messages.html', recipient=recipient)
        
        # Create new message
        message = Message(
            sender_id=current_user.id,
            receiver_id=recipient_id,
            subject=subject,
            content=content
        )
        
        flash(f'Message sent to {recipient.full_name}!', 'success')
        logging.info(f'Message sent from {current_user.username} to {recipient.username}')
        return redirect(url_for('messages'))
    
    return render_template('messages.html', recipient=recipient)

@app.route('/message/<message_id>')
@login_required
def view_message(message_id):
    """View a specific message"""
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    message = Message.get_by_id(message_id)
    if not message:
        flash('Message not found', 'error')
        return redirect(url_for('messages'))
    
    # Check if user has permission to view this message
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        flash('You do not have permission to view this message', 'error')
        return redirect(url_for('messages'))
    
    # Mark as read if user is the receiver
    if message.receiver_id == current_user.id:
        message.is_read = True
    
    return render_template('messages.html', view_message=message)
