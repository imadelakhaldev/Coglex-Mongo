"""
global configuration variables module
contains project-wide settings and constants used throughout the application
includes server, database, smtp and application-specific configurations
"""


# python's built-in time scheduling and management
from datetime import timedelta

# operating system interactions
import os

# pip install python-dotenv
# environment variable management
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()


# application details and configurations
APP_IMPORT = __name__
APP_FOLDER = "coglex"
APP_STATIC = os.path.join(APP_FOLDER, "static")
APP_TEMPLATES = os.path.join(APP_FOLDER, "templates")
APP_UPLOAD = os.path.join(APP_FOLDER, "static", "documents")
APP_NAME = "Tranzlate"
APP_VERSION = "Genesis"
APP_TITLE = "AI-Powered Document Translation"
APP_COMPANY = "DIGISOFTWORKS LTD"
APP_WEBSITE = "https://tranzlate.ma/"

# server configurations and session settings
BASE_URL = "http://127.0.0.1:5000"

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
MONGODB_AUTH_COLLECTION = "USERS"

# stripe payment api keys
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")


# gemini translation model generation credintials
GENERATION_MODEL_KEY = os.environ.get("GENERATION_MODEL_KEY")
GENERATION_MODEL_NAME = "gemini-2.0-flash"
GENERATION_MODEL_SYSTEM = """
You are an AI translation engine, your task is to translate the user's content from source language to target language according to the provided instructions.


**Parameters and Settings**

*   **Source Language:** `{ source }`
*   **Target Language:** `{ target }`


**Primary Rules:**

1.  **Language Identification:** Correctly identify source and target languages, whether they are provided as ISO codes (e.g., `en`, `fr`), English names (e.g., `French`, `Arabic`), or native names (e.g., `Français`, `العربية`).
2.  **Format Detection:** Automatically detect if the input is `JSON` (from unstructured.io) or `SRT` (transcription).
3.  **Output Result:** Your response must be **only** the final translated text in the correct format, with no conversational text.


**Format-Specific Instructions:**

**1. If JSON Input:**
*   **Goal:** Convert to a single Markdown document.
*   **Action:** Translate the provided texts, and map elements to their appropriate markdown equivalent.

**2. If SRT Input:**
*   **Goal:** Translate the subtitles in place.
*   **Action:** Translate **only** the dialogue lines.
*   **Crucial:** **DO NOT** alter the line numbers or timestamps, preserve the exact SRT structure.
"""
