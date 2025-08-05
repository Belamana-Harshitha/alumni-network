# Alumni Networking Portal

## Overview

A Flask-based web application that serves as a networking platform for alumni and students. The platform enables users to connect with each other, share job opportunities, organize events, and communicate through a built-in messaging system. The application features user authentication, role-based access control, and an admin panel for platform management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Flask**: Lightweight Python web framework chosen for rapid development and simplicity
- **Jinja2 Templates**: Server-side rendering for dynamic content generation
- **Session Management**: Flask sessions for user authentication state

### Data Storage
- **In-Memory Storage**: Currently uses Python dictionaries for MVP implementation
- **Data Models**: Four main entities - Users, Jobs, Events, and Messages
- **UUID-based IDs**: Ensures unique identification across all entities

### Authentication & Authorization
- **Password Hashing**: Werkzeug security for password encryption
- **Session-based Auth**: User sessions stored server-side
- **Role-based Access**: Three user types (alumni, student, admin) with different permissions
- **Decorator-based Protection**: `@login_required` and `@admin_required` decorators

### Frontend Architecture
- **Bootstrap 5**: Responsive UI framework with dark theme
- **Feather Icons**: Consistent iconography throughout the application
- **Progressive Enhancement**: JavaScript enhancements for better UX
- **Mobile-first Design**: Responsive layout for all device sizes

### Application Structure
- **Modular Routing**: Separated route handlers (main routes, auth, admin)
- **Template Inheritance**: Base template with consistent navigation and layout
- **Utility Functions**: Helper functions for data formatting and validation
- **Static Assets**: CSS and JavaScript files for custom styling and interactions

### Security Features
- **Input Validation**: Server-side validation for all user inputs
- **Password Requirements**: Minimum length and confirmation validation
- **Session Security**: Configurable secret key for session encryption
- **Admin Access Control**: Restricted admin functionality with proper authorization

## External Dependencies

### Core Dependencies
- **Flask**: Web application framework
- **Werkzeug**: WSGI utilities and security functions for password hashing

### Frontend Dependencies
- **Bootstrap 5**: CSS framework with Replit dark theme variant
- **Feather Icons**: SVG icon library loaded via CDN
- **JavaScript**: Vanilla JS for client-side enhancements

### Development Dependencies
- **Python Standard Library**: datetime, uuid, logging, os, re modules
- **Werkzeug ProxyFix**: For proper URL generation behind proxies

### Future Integration Points
- **Database**: Ready for migration from in-memory to persistent storage (PostgreSQL recommended)
- **Email Service**: Placeholder for notification and messaging features
- **File Upload**: Infrastructure for profile pictures and document sharing
- **Search Engine**: Can be enhanced with dedicated search capabilities