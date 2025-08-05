# Alumni Networking Portal

A comprehensive web-based networking platform that connects alumni and current students. Built with Flask, this portal enables users to build professional networks, discover opportunities, and stay connected with their academic community.

![Alumni Portal](https://img.shields.io/badge/Flask-2.3.3-blue) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple) ![Python](https://img.shields.io/badge/Python-3.11-green)

## ✨ Features

### 🔐 User Authentication & Profiles
- Secure user registration and login system
- Detailed professional profiles with graduation info
- Role-based access (Alumni, Students, Admin)
- Password security with hashing

### 🔍 Advanced Search & Discovery
- Search alumni by department, company, or graduation year
- Filter results by location and professional interests
- Browse user profiles and connect with peers

### 💼 Job Board
- Post and browse job opportunities
- Detailed job descriptions with requirements
- Company and location information
- Easy application process

### 📅 Events Management
- Create and manage networking events
- Event details with date, location, and descriptions
- RSVP functionality for attendees
- Community calendar integration

### 💬 Messaging System
- Private messaging between users
- Real-time communication platform
- Message history and conversation management
- Professional networking facilitation

### 👑 Admin Dashboard
- User management and moderation tools
- Platform analytics and insights
- Content management capabilities
- System administration features

## 🚀 Live Demo

Visit the live application: [Alumni Portal](https://your-deployment-url.replit.app)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy with PostgreSQL support
- **Frontend**: Bootstrap 5 with dark theme
- **Authentication**: Werkzeug Security
- **Icons**: Feather Icons
- **Deployment**: Replit Deployments with Gunicorn

## 📋 Installation & Setup

### Prerequisites
- Python 3.11+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/alumni-networking-portal.git
   cd alumni-networking-portal
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy werkzeug gunicorn psycopg2-binary email-validator
   ```

3. **Set environment variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="your-database-url"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Deployment on Replit

1. Fork this repository to your Replit account
2. Click the "Deploy" button in your workspace
3. Choose "Autoscale" deployment type
4. Your app will be live at `yourapp.replit.app`

## 📁 Project Structure

```
alumni-networking-portal/
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Landing page
│   ├── register.html      # User registration
│   ├── login.html         # User login
│   ├── dashboard.html     # User dashboard
│   ├── profile.html       # User profiles
│   ├── search.html        # Alumni search
│   ├── jobs.html          # Job listings
│   ├── events.html        # Event listings
│   ├── messages.html      # Messaging system
│   └── admin.html         # Admin dashboard
├── static/                # Static assets
│   ├── css/style.css      # Custom styling
│   └── js/main.js         # JavaScript functionality
├── main.py               # Application entry point
├── app.py                # Flask app configuration
├── models.py             # Database models
├── auth.py               # Authentication routes
├── routes.py             # Main application routes
├── admin.py              # Admin functionality
├── utils.py              # Utility functions
└── README.md             # This file
```

## 🎯 Usage Guide

### For Students
1. **Register** with your academic email
2. **Complete your profile** with academic and career information
3. **Search for alumni** in your field of interest
4. **Apply to jobs** posted by alumni and companies
5. **Attend networking events** to build connections

### For Alumni
1. **Update your profile** with current professional information
2. **Post job opportunities** at your company
3. **Mentor students** through messaging
4. **Organize events** for your graduating class
5. **Give back** to your academic community

### For Administrators
1. **Monitor platform activity** through the admin dashboard
2. **Manage user accounts** and resolve issues
3. **Moderate content** to maintain professional standards
4. **Generate reports** on platform engagement

## 🔧 Configuration

### Environment Variables
- `SESSION_SECRET`: Secret key for session encryption
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Set to 'development' for debug mode

### Database Setup
The application automatically creates necessary tables on first run. No manual database setup required.

## 🎨 Customization

### Styling
- Built with Bootstrap 5 and Replit dark theme
- Custom CSS in `static/css/style.css`
- Responsive design for all device sizes

### Features
- Modular code structure for easy feature additions
- Well-documented functions and routes
- Beginner-friendly codebase with comments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions
- **Documentation**: Comprehensive code comments and documentation

## 🙏 Acknowledgments

- Bootstrap team for the excellent CSS framework
- Feather Icons for beautiful iconography
- Flask community for the amazing web framework
- Replit for providing deployment platform

---

**Built with ❤️ for connecting academic communities**

*Start building your professional network today!*
