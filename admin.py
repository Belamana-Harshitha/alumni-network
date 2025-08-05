"""
Admin panel routes and functionality
"""

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import User, Job, Event, Message
from auth import admin_required, get_current_user
import logging

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    # Get statistics
    total_users = len([user for user in User.get_all_users() if user.user_type != 'admin'])
    total_jobs = len(Job.get_all_jobs())
    total_events = len(Event.get_all_events())
    total_messages = len(list(messages.values()))
    
    # Get recent activity
    recent_users = sorted([user for user in User.get_all_users() 
                          if user.user_type != 'admin'], 
                         key=lambda x: x.created_at, reverse=True)[:5]
    recent_jobs = sorted(Job.get_all_jobs(), 
                        key=lambda x: x.created_at, reverse=True)[:5]
    recent_events = sorted(Event.get_all_events(), 
                          key=lambda x: x.created_at, reverse=True)[:5]
    
    from models import messages  # Import here to avoid circular import
    
    return render_template('admin.html',
                         stats={
                             'total_users': total_users,
                             'total_jobs': total_jobs,
                             'total_events': total_events,
                             'total_messages': total_messages
                         },
                         recent_users=recent_users,
                         recent_jobs=recent_jobs,
                         recent_events=recent_events)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Manage users"""
    users = [user for user in User.get_all_users() if user.user_type != 'admin']
    return render_template('admin.html', view='users', users=users)

@app.route('/admin/user/<user_id>/toggle_status')
@admin_required
def admin_toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_users'))
    
    if user.user_type == 'admin':
        flash('Cannot modify admin user', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_active = not user.is_active
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}', 'success')
    logging.info(f'Admin toggled user status: {user.username} -> {status}')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/jobs')
@admin_required
def admin_jobs():
    """Manage jobs"""
    jobs = Job.get_all_jobs()
    jobs.sort(key=lambda x: x.created_at, reverse=True)
    return render_template('admin.html', view='jobs', jobs=jobs)

@app.route('/admin/job/<job_id>/toggle_status')
@admin_required
def admin_toggle_job_status(job_id):
    """Toggle job active status"""
    job = Job.get_by_id(job_id)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('admin_jobs'))
    
    job.is_active = not job.is_active
    status = 'activated' if job.is_active else 'deactivated'
    flash(f'Job "{job.title}" has been {status}', 'success')
    logging.info(f'Admin toggled job status: {job.title} -> {status}')
    
    return redirect(url_for('admin_jobs'))

@app.route('/admin/events')
@admin_required
def admin_events():
    """Manage events"""
    events = Event.get_all_events()
    events.sort(key=lambda x: x.created_at, reverse=True)
    return render_template('admin.html', view='events', events=events)

@app.route('/admin/event/<event_id>/toggle_status')
@admin_required
def admin_toggle_event_status(event_id):
    """Toggle event active status"""
    event = Event.get_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin_events'))
    
    event.is_active = not event.is_active
    status = 'activated' if event.is_active else 'deactivated'
    flash(f'Event "{event.title}" has been {status}', 'success')
    logging.info(f'Admin toggled event status: {event.title} -> {status}')
    
    return redirect(url_for('admin_events'))

@app.route('/admin/messages')
@admin_required
def admin_messages():
    """View all messages"""
    from models import messages  # Import here to avoid circular import
    all_messages = list(messages.values())
    all_messages.sort(key=lambda x: x.created_at, reverse=True)
    return render_template('admin.html', view='messages', messages=all_messages)
