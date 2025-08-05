"""
Data models for the Alumni Networking Portal
Using in-memory storage for MVP implementation
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# In-memory storage dictionaries
users = {}
jobs = {}
events = {}
messages = {}

class User:
    """User model for alumni and students"""
    
    def __init__(self, username, email, password, full_name, graduation_year=None, 
                 department=None, current_company=None, location=None, user_type='alumni'):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.full_name = full_name
        self.graduation_year = graduation_year
        self.department = department
        self.current_company = current_company
        self.location = location
        self.user_type = user_type  # 'alumni', 'student', 'admin'
        self.created_at = datetime.now()
        self.is_active = True
        
        # Store in global users dictionary
        users[self.id] = self
    
    def check_password(self, password):
        """Check if provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary for easy template rendering"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'graduation_year': self.graduation_year,
            'department': self.department,
            'current_company': self.current_company,
            'location': self.location,
            'user_type': self.user_type,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    @staticmethod
    def get_by_username(username):
        """Find user by username"""
        for user in users.values():
            if user.username == username:
                return user
        return None
    
    @staticmethod
    def get_by_email(email):
        """Find user by email"""
        for user in users.values():
            if user.email == email:
                return user
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Find user by ID"""
        return users.get(user_id)
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        return list(users.values())

class Job:
    """Job posting model"""
    
    def __init__(self, title, description, company, location, posted_by_id, 
                 job_type='full-time', salary_range=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.company = company
        self.location = location
        self.posted_by_id = posted_by_id
        self.job_type = job_type
        self.salary_range = salary_range
        self.created_at = datetime.now()
        self.is_active = True
        
        # Store in global jobs dictionary
        jobs[self.id] = self
    
    def to_dict(self):
        """Convert job object to dictionary"""
        posted_by = User.get_by_id(self.posted_by_id)
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'location': self.location,
            'posted_by': posted_by.full_name if posted_by else 'Unknown',
            'posted_by_id': self.posted_by_id,
            'job_type': self.job_type,
            'salary_range': self.salary_range,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    @staticmethod
    def get_all_jobs():
        """Get all active jobs"""
        return [job for job in jobs.values() if job.is_active]
    
    @staticmethod
    def get_by_id(job_id):
        """Find job by ID"""
        return jobs.get(job_id)

class Event:
    """Event model for alumni gatherings and networking events"""
    
    def __init__(self, title, description, date, location, organized_by_id):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.organized_by_id = organized_by_id
        self.created_at = datetime.now()
        self.is_active = True
        
        # Store in global events dictionary
        events[self.id] = self
    
    def to_dict(self):
        """Convert event object to dictionary"""
        organized_by = User.get_by_id(self.organized_by_id)
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'location': self.location,
            'organized_by': organized_by.full_name if organized_by else 'Unknown',
            'organized_by_id': self.organized_by_id,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    @staticmethod
    def get_all_events():
        """Get all active events"""
        return [event for event in events.values() if event.is_active]
    
    @staticmethod
    def get_by_id(event_id):
        """Find event by ID"""
        return events.get(event_id)

class Message:
    """Message model for user communication"""
    
    def __init__(self, sender_id, receiver_id, subject, content):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.subject = subject
        self.content = content
        self.created_at = datetime.now()
        self.is_read = False
        
        # Store in global messages dictionary
        messages[self.id] = self
    
    def to_dict(self):
        """Convert message object to dictionary"""
        sender = User.get_by_id(self.sender_id)
        receiver = User.get_by_id(self.receiver_id)
        return {
            'id': self.id,
            'sender': sender.full_name if sender else 'Unknown',
            'sender_id': self.sender_id,
            'receiver': receiver.full_name if receiver else 'Unknown',
            'receiver_id': self.receiver_id,
            'subject': self.subject,
            'content': self.content,
            'created_at': self.created_at,
            'is_read': self.is_read
        }
    
    @staticmethod
    def get_user_messages(user_id):
        """Get all messages for a specific user (sent and received)"""
        user_messages = []
        for message in messages.values():
            if message.sender_id == user_id or message.receiver_id == user_id:
                user_messages.append(message)
        return sorted(user_messages, key=lambda x: x.created_at, reverse=True)
    
    @staticmethod
    def get_by_id(message_id):
        """Find message by ID"""
        return messages.get(message_id)

# Initialize with admin user
def init_data():
    """Initialize the application with an admin user"""
    if not users:  # Only create if no users exist
        admin = User(
            username='admin',
            email='admin@alumni.edu',
            password='admin123',
            full_name='System Administrator',
            user_type='admin'
        )
        print(f"Admin user created with ID: {admin.id}")

# Call initialization
init_data()
