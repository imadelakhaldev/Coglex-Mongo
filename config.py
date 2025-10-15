"""
global configuration variables module
contains project-wide settings and constants used throughout the application
includes server, database, smtp and application-specific configurations
"""


# standard imports
import os

# python's built-in time scheduling and management
from datetime import timedelta

# pip install python-dotenv
# environment variable management
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()


# application details and configurations
# baic global settings
APP_IMPORT = __name__
APP_FOLDER = "coglex"
APP_STATIC = os.path.join(APP_FOLDER, "static")
APP_TEMPLATES = os.path.join(APP_FOLDER, "templates")
APP_UPLOAD = os.path.join(APP_FOLDER, "static", "documents")
APP_NAME = "Coglex"
APP_VERSION = "Genesis"
APP_TITLE = "Backend Collection for Web Development"
APP_COMPANY = "IMAD EL AKHAL"
APP_WEBSITE = "https://coglex.ma/"

# server configurations and session settings
BASE_URL = "http://127.0.0.1:5000"

# file uploads and storage settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
SEND_FILE_MAX_AGE = timedelta(days=365)

# server configurations and session settings
SERVER_SECRET = os.environ.get("SERVER_SECRET")
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
SERVER_DEBUG = True  # must be set to False in production, True for local testing and development
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
MONGODB_AUTH_COLLECTION = "_USERS"
MONGODB_ARCHIVE_COLLECTION = "_ARCHIVE"

# verification / one-time-password (otp) authentication configurations
VERIFICATION_LENGTH = 6
VERIFICATION_EXPIRY = timedelta(minutes=10)

# oauth provider credentials and configurations
OAUTH_EXPIRY = timedelta(minutes=10)
OAUTH_PROVIDERS = {
    "google": {
        "CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID"),
        "CLIENT_SECRET": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "AUTHORIZE_URL": "https://accounts.google.com/o/oauth2/v2/auth",
        "TOKEN_URL": "https://oauth2.googleapis.com/token",
        "INFO_URL": "https://www.googleapis.com/oauth2/v2/userinfo",
        "SCOPES": "openid email profile"
    },
    "facebook": {
        "CLIENT_ID": os.environ.get("FACEBOOK_CLIENT_ID"),
        "CLIENT_SECRET": os.environ.get("FACEBOOK_CLIENT_SECRET"),
        "AUTHORIZE_URL": "https://www.facebook.com/v18.0/dialog/oauth",
        "TOKEN_URL": "https://graph.facebook.com/v18.0/oauth/access_token",
        "INFO_URL": "https://graph.facebook.com/me?fields=id,name,email",
        "SCOPES": "email public_profile"
    }
}

# stripe payment api keys
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")

# google gemini api configurations
GENERATION_MODEL = "models/gemini-2.5-flash"
GENERATION_KEY = os.environ.get("GENERATION_KEY")


# custom gateway configurations
# basic settings and configurations
# MODULE_CONFIG = True
