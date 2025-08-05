import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask application
app = Flask(__name__)

# Set secret key for session management
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure proxy fix for proper URL generation
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Import routes after creating the app to avoid circular imports
from routes import *
from auth import *
from admin import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
