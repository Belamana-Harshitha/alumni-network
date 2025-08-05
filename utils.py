"""
Utility functions for the Alumni Networking Portal
"""

from datetime import datetime
import re

def format_date(date_obj):
    """Format date for display"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%B %d, %Y at %I:%M %p')
    elif hasattr(date_obj, 'strftime'):  # date object
        return date_obj.strftime('%B %d, %Y')
    return str(date_obj)

def format_date_short(date_obj):
    """Format date in short format"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%m/%d/%Y')
    elif hasattr(date_obj, 'strftime'):  # date object
        return date_obj.strftime('%m/%d/%Y')
    return str(date_obj)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def truncate_text(text, max_length=100):
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'

def get_graduation_years():
    """Get list of graduation years for dropdown"""
    current_year = datetime.now().year
    return list(range(current_year + 5, 1950, -1))  # Future years to 1950

def get_departments():
    """Get list of common departments"""
    return [
        'Computer Science',
        'Engineering',
        'Business Administration',
        'Liberal Arts',
        'Medicine',
        'Law',
        'Education',
        'Psychology',
        'Biology',
        'Chemistry',
        'Physics',
        'Mathematics',
        'Economics',
        'Political Science',
        'History',
        'English',
        'Art',
        'Music',
        'Other'
    ]

def get_job_types():
    """Get list of job types"""
    return [
        'full-time',
        'part-time',
        'contract',
        'internship',
        'freelance',
        'remote'
    ]

# Add utility functions to Jinja2 global context
from app import app

@app.template_global()
def format_date_filter(date_obj):
    return format_date(date_obj)

@app.template_global()
def format_date_short_filter(date_obj):
    return format_date_short(date_obj)

@app.template_global()
def truncate_text_filter(text, max_length=100):
    return truncate_text(text, max_length)
