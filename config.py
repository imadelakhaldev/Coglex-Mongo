"""
global configuration variables module
contains project-wide settings and constants used throughout the application
includes server, database, smtp and application-specific configurations
"""


# python's built-in time scheduling and management
from datetime import timedelta

# operating system interactions
import os

# environment variable management
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()


# application details and configurations
APP_IMPORT = __name__
APP_FOLDER = "coglex"
APP_STATIC = os.path.join(APP_FOLDER, "static")
APP_TEMPLATES = os.path.join(APP_FOLDER, "templates")
APP_UPLOAD = os.path.join(APP_FOLDER, "static", "uploads")
APP_NAME = "Coglex Intelligence"
APP_VERSION = "Genesis"
APP_TITLE = "Artificial Intelligence Completion"
APP_COMPANY = "DIGISOFTWORKS LTD"
APP_WEBSITE = "https://digisoftworks.com/"

# server configurations and session settings
BASE_URL = "https://coglex.com/"

# file uploads and storage settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
SEND_FILE_MAX_AGE = timedelta(days=365)

# server configurations and session settings
SERVER_SECRET = os.environ.get("SERVER_SECRET")
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
SERVER_DEBUG = True
SERVER_SESSION_LIFETIME = timedelta(days=8)

# smtp mailing server credentials
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USE_TLS = True
SMTP_USERNAME = "system@coglex.com"
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

# mongodb, database client configurations
MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_DATABASE = APP_FOLDER
MONGODB_HEX_LENGTH = 12

# stripe payment api keys
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
