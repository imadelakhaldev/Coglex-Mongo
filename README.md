<div align="center">

# Coglex Intelligence

🧠 A powerful Flask-based backend collection of services for application development

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-latest-success.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 🌟 Features

- 🔐 **Robust Authentication System** - Session-based user authentication with secure password hashing using bcrypt
- 📁 **File Management** - Secure file upload, download, and deletion with temporary storage and metadata tracking
- 💳 **Payment Integration** - Stripe payment processing for subscriptions and one-time payments with webhook support
- 🔄 **Dynamic Function Execution** - Remote execution of Python functions with parameter validation and error handling
- 📦 **MongoDB Integration** - Comprehensive CRUD operations with PyMongo and custom hex ID generation
- 🛡️ **API Protection** - Multi-layered security with API keys and session-based authentication decorators

## 📖 Overview

Coglex Intelligence is a sophisticated backend service built with Flask, designed to provide secure and scalable API endpoints for user authentication, data storage, file management, payment processing, and dynamic function execution. The application follows a modular architecture with clearly separated services, each providing specific functionality through RESTful APIs.

## 🏗️ Project Structure

```
coglex/
├── __init__.py        # Flask app initialization, DB connection, blueprints, decorators
├── gateway/           # Entry point for new routes and applications
│   └── tranzlate/     # Gateway module for Tranzlate application
├── services/          # Core service modules
│   ├── auth/          # Authentication service
│   │   ├── routes.py  # API routes for auth operations (signup, signin, session, signout, refresh)
│   │   └── utils.py   # Auth helper functions (_signup, _signin, _signout, _refresh)
│   ├── archive/       # File storage service
│   │   ├── routes.py  # File operation endpoints (upload, download, delete)
│   │   └── utils.py   # File handling utilities with temporary storage
│   ├── execution/     # Function execution service
│   │   ├── routes.py  # Dynamic function execution endpoints
│   │   └── utils.py   # Function execution helpers with inspection
│   ├── payment/       # Payment processing (Stripe)
│   │   ├── routes.py  # Payment endpoints (checkout, subscription)
│   │   └── utils.py   # Stripe integration helpers with webhook verification
│   └── storage/       # Database operations
│       ├── routes.py  # CRUD operation endpoints with query support
│       └── utils.py   # MongoDB utilities with custom hex ID generation
├── static/           # Static assets and uploads
└── templates/        # HTML templates
```

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- MongoDB instance
- Stripe account (for payment features)
- Virtual environment (recommended)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/coglex.git
cd coglex
```

2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration:
# - SERVER_SECRET: Your API key for endpoint protection
# - MONGODB_URI: Your MongoDB connection string
# - MONGODB_DATABASE: Your MongoDB database name
# - STRIPE_SECRET_KEY: Stripe API secret key
```

5. Run the application
```bash
python run.py
```

## 🔒 Security Implementation

### API Protection

#### API Key Authentication (`@protected` decorator)
- Requires `X-API-Key` header in requests
- Validates against `SERVER_SECRET` in configuration
- Provides first-level security for all service endpoints

#### Session Authentication (`@authenticated` decorator)
- Implements session-based authentication using Flask sessions
- Validates user credentials against stored password hashes
- Re-authenticates users on each request for enhanced security
- Ensures secure access to user-specific resources

## 🛠️ Core Services

### Authentication Service

```python
# User Management Endpoints
POST /service/auth/v1/signup/<collection>/  # Register new user
    - Validates user data and prevents duplicates
    - Hashes passwords securely using bcrypt
    - Creates user document in MongoDB with custom hex ID

POST /service/auth/v1/signin/<collection>/  # User login
    - Validates credentials against stored hash
    - Creates Flask session with user data
    - Returns user document on successful authentication

GET /service/auth/v1/session/<collection>/  # Get current session
    - Returns current session data for the collection
    - Used for session validation and user info retrieval

GET /service/auth/v1/signout/<collection>/  # User logout
    - Clears session data for the specified collection
    - Terminates user session securely

PATCH /service/auth/v1/refresh/<collection>/  # Update user data
    - Updates user information in the database
    - Handles password updates with re-hashing
    - Validates user existence before updating
```

### Storage Service

```python
# Database Operations with MongoDB
GET    /service/storage/v1/<collection>/       # List documents
    - Supports query parameters for filtering
    - Accepts JSON query and keys parameters
    - Returns single document or list based on results

GET    /service/storage/v1/<collection>/<key>/  # Get single document by ID
    - Retrieves document by _id field
    - Supports field selection with keys parameter

POST   /service/storage/v1/<collection>/       # Create document(s)
    - Accepts single document or array of documents
    - Generates custom hex IDs for each document
    - Returns inserted document ID(s)

PATCH  /service/storage/v1/<collection>/<key>/  # Update single document
    - Updates document by _id field
    - Supports MongoDB update operators ($set, $inc, etc.)

PATCH  /service/storage/v1/<collection>/       # Update multiple documents
    - Updates documents matching query parameters
    - Supports bulk updates with MongoDB operators

DELETE /service/storage/v1/<collection>/<key>/  # Delete single document
    - Deletes document by _id field
    - Returns count of deleted documents

DELETE /service/storage/v1/<collection>/       # Delete multiple documents
    - Deletes documents matching query parameters
    - Returns count of deleted documents
```

### Archive Service

```python
# File Management and Temporary Storage
POST /service/archive/v1/upload/  # Upload file
    - Handles file uploads with size validation
    - Stores files temporarily in the system
    - Returns file metadata and storage information
    - Supports various file types and formats

GET /service/archive/v1/download/<file_id>/  # Download file
    - Retrieves stored files by unique identifier
    - Handles file streaming for large files
    - Returns appropriate content types and headers

DELETE /service/archive/v1/delete/<file_id>/  # Delete file
    - Removes files from temporary storage
    - Cleans up associated metadata
    - Returns deletion confirmation

GET /service/archive/v1/list/  # List uploaded files
    - Returns list of available files with metadata
    - Supports filtering and pagination
    - Includes file size, upload date, and type information
```

### Execution Service

```python
# Dynamic Function Execution
POST /service/execution/v1/execute/  # Execute Python code dynamically
    - Accepts Python code as string in request body
    - Executes code in isolated environment with error handling
    - Returns execution results or error messages
    - Supports both synchronous execution and result capture
    - Implements security measures for safe code execution
```

### Payment Service

```python
# Stripe Integration with Webhook Support
POST /service/payment/v1/create-payment-intent/  # Create payment intent
    - Creates Stripe payment intent with specified amount
    - Returns client secret for frontend payment processing
    - Handles payment method configuration

POST /service/payment/v1/webhook/  # Stripe webhook handler
    - Processes Stripe webhook events securely
    - Validates webhook signatures for security
    - Handles payment status updates and notifications
    - Supports various Stripe event types

GET /service/payment/v1/payment-status/<payment_intent_id>/  # Check payment status
    - Retrieves current status of payment intent
    - Returns payment details and confirmation status
```

## 🔌 Event System

### Signal Handlers

The application uses Flask signals for extensible event handling:

```python
from coglex.utils import stripe_webhook_received

@stripe_webhook_received.connect
def handle_payment(sender, **kwargs):
    payload = sender
    # Custom payment processing logic
    # - Update order status
    # - Send confirmation emails
    # - Trigger fulfillment
```

## 🧪 Testing

### API Testing

Import the provided collections for comprehensive API testing:

```bash
# Using Insomnia
insomnia import insomnia.yaml

# Using Postman
postman import insomnia.har
```

The collections include pre-configured requests for all endpoints with:
- Request headers setup
- Body templates
- Environment variables
- Authentication flows

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Authors

- **IMAD EL AKHAL** - *Initial work* - [Website](https://ielakhal.com/)
