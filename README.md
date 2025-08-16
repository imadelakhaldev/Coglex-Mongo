<div align="center">

# Coglex Intelligence

🧠 A powerful Flask-based backend collection of services for application development

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-latest-success.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 🌟 Features

- 🔐 **Robust Authentication System** - JWT-based user authentication with secure session management
- 📁 **File Management** - Secure file upload, download, and deletion with metadata tracking
- 💳 **Payment Integration** - Stripe payment processing for subscriptions and one-time payments
- 🔄 **Dynamic Function Execution** - Remote execution of Python functions with parameter validation
- 📦 **MongoDB Integration** - Comprehensive CRUD operations with PyMongo
- 🛡️ **API Protection** - Multi-layered security with API keys and JWT authentication

## 📖 Overview

Coglex Intelligence is a sophisticated backend service built with Flask, designed to provide secure and scalable API endpoints for user authentication, data storage, and file management. The application follows a modular architecture, with clearly separated services for authentication, storage, file management, and payment processing.

## 🏗️ Project Structure

```
coglex/
├── __init__.py        # Flask app initialization, DB connection, blueprints
├── gateway/           # Entry point for new routes and applications
├── services/          # Core service modules
│   ├── auth/          # Authentication service
│   │   ├── routes.py  # API routes for auth operations
│   │   └── utils.py   # Auth helper functions
│   ├── archive/       # File storage service
│   │   ├── routes.py  # File operation endpoints
│   │   └── utils.py   # File handling utilities
│   ├── execution/     # Function execution service
│   │   ├── routes.py  # Dynamic function endpoints
│   │   └── utils.py   # Execution helpers
│   ├── payment/       # Payment processing (Stripe)
│   │   ├── routes.py  # Payment endpoints
│   │   └── utils.py   # Stripe integration helpers
│   └── storage/       # Database operations
│       ├── routes.py  # CRUD operation endpoints
│       └── utils.py   # MongoDB utilities
├── static/           # Static assets and uploads
└── templates/        # HTML templates
```

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- MongoDB instance
- Stripe account (for payment features)
- SMTP server (for email notifications)

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
# - SMTP_PASSWORD: Email server password
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

#### JWT Authentication (`@authenticated` decorator)
- Implements stateless authentication using JSON Web Tokens
- Requires `Authorization: Bearer <token>` header
- Validates user session and permissions
- Ensures secure access to user-specific resources

## 🛠️ Core Services

### Authentication Service

```python
# User Management Endpoints
POST /service/auth/v1/signup/<collection>/  # Register new user
    - Validates user data
    - Hashes passwords securely
    - Creates user document in MongoDB

POST /service/auth/v1/signin/<collection>/  # User login
    - Validates credentials
    - Issues JWT token
    - Sets session data

GET /service/auth/v1/session/<collection>/  # Validate session
    - Verifies JWT token
    - Returns user session data

GET /service/auth/v1/signout/<collection>/  # User logout
    - Invalidates current session
    - Cleans up session data
```

### Storage Service

```python
# Database Operations
GET    /service/storage/v1/<collection>/       # List documents
    - Supports pagination
    - Implements filtering
    - Handles sorting

GET    /service/storage/v1/<collection>/<key>/  # Get single document
POST   /service/storage/v1/<collection>/       # Create document
PATCH  /service/storage/v1/<collection>/<key>/  # Update document
DELETE /service/storage/v1/<collection>/<key>/  # Delete document
```

### Archive Service

```python
# File Management
POST   /service/archive/v1/upload/<collection>/    # Upload file
    - Handles multipart/form-data
    - Validates file types
    - Stores metadata in MongoDB

GET    /service/archive/v1/download/<collection>/  # Download file
    - Streams file content
    - Validates permissions

DELETE /service/archive/v1/delete/<collection>/   # Delete file
    - Removes file and metadata
```

### Payment Service

```python
# Stripe Integration
POST /service/payment/v1/checkout/      # Process one-time payment
    - Creates Stripe Checkout session
    - Handles success/failure redirects

POST /service/payment/v1/subscription/  # Manage subscriptions
    - Creates/updates subscriptions
    - Handles billing cycles

POST /service/payment/v1/webhook/       # Handle Stripe events
    - Processes webhook notifications
    - Updates payment status
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

## 📚 Documentation

For detailed API documentation and examples, refer to our [Wiki](https://github.com/yourusername/coglex/wiki).

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write comprehensive docstrings
- Add unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **IMAD EL AKHAL** - *Initial work* - [Website](https://ielakhal.com/)

## 🙏 Acknowledgments

- Flask framework and its community
- MongoDB team for excellent documentation
- Stripe for robust payment integration
- All contributors who have helped shape this project
