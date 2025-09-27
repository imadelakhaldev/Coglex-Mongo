<div align="center">

# Coglex Intelligence

🧠 A powerful Flask-based backend collection of services for application development

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-latest-success.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 🌟 Features

- 🔐 **Enhanced Authentication System** - Session-based user authentication with secure password hashing using bcrypt, timing attack protection, and rate limiting
- 📁 **Secure File Management** - Comprehensive file upload, download, and deletion with enhanced validation, type checking, and access controls
- 💳 **Stripe Payment Integration** - Secure payment processing with Stripe's latest API standards and PCI compliance measures
- 📦 **Secure MongoDB Integration** - CRUD operations with NoSQL injection prevention, input sanitization, and custom hex ID generation
- 🛡️ **Multi-layered API Protection** - API keys and session-based authentication with comprehensive security decorators and validation

## 📖 Overview

Coglex Intelligence is a sophisticated and secure backend service built with Flask, designed to provide robust and scalable API endpoints for user authentication, data storage, file management, and payment processing. The application follows a modular architecture with clearly separated services, each providing specific functionality through RESTful APIs with comprehensive security measures.

**Key Security Features:**
- NoSQL injection prevention across all database operations
- Enhanced authentication with timing attack protection and rate limiting
- Secure file handling with comprehensive validation and access controls
- PCI-compliant payment processing with Stripe integration
- Multi-layered API protection with session management and API key validation

The framework has been thoroughly audited and hardened against common security vulnerabilities, making it suitable for production environments requiring high security standards.

## 🏗️ Project Structure

```
coglex/
├── __init__.py        # Flask app initialization, DB connection, blueprints, decorators
├── gateway/           # Entry point for new routes and applications
│   └── module/     # example module for developed application
├── services/          # Core service modules
│   ├── auth/          # Authentication service
│   │   ├── routes.py  # API routes for auth operations (signup, signin, session, signout, refresh)
│   │   └── utils.py   # Enhanced auth utilities with secure session management
│   ├── archive/       # File storage service
│   │   ├── routes.py  # File operation endpoints (upload, download, delete)
│   │   └── utils.py   # Secure file handling utilities with enhanced validation
│   ├── payment/       # Payment processing (Stripe)
│   │   ├── routes.py  # Payment endpoints (checkout, subscription)
│   │   └── utils.py   # Stripe integration helpers with secure payment processing
│   └── storage/       # Database operations
│       ├── routes.py  # CRUD operation endpoints with query support
│       └── utils.py   # MongoDB utilities with NoSQL injection prevention
├── static/           # Static assets and uploads
└── templates/        # HTML templates
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (recommended: Python 3.9 or higher)
- MongoDB instance (local or cloud-based like MongoDB Atlas)
- Stripe account (for payment features)
- Virtual environment (strongly recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/imadelakhaldev/coglex.git
cd coglex
```

2. **Create and activate virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your secure configuration:
# - SERVER_SECRET: Strong API key for endpoint protection (use a secure random string)
# - MONGODB_URI: Your MongoDB connection string with authentication
# - MONGODB_DATABASE: Your MongoDB database name
# - STRIPE_SECRET_KEY: Stripe API secret key from your Stripe dashboard
```

5. **Verify MongoDB connection**
```bash
# Ensure your MongoDB instance is running and accessible
# Test connection with your MONGODB_URI
```

6. **Run the application**
```bash
python run.py
```

The application will start on `http://localhost:5000` by default.

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

### Security Enhancements

#### NoSQL Injection Prevention
- **Input Sanitization**: All database queries are sanitized to prevent NoSQL injection attacks
- **Parameter Validation**: Query parameters are validated and type-checked before processing
- **Safe Query Construction**: Uses parameterized queries and safe MongoDB operators

#### Enhanced Authentication Security
- **Secure Password Hashing**: Uses bcrypt with configurable rounds for password storage
- **Session Management**: Implements secure session handling with proper cleanup and validation
- **Timing Attack Protection**: Prevents timing-based attacks during credential validation
- **Rate Limiting**: Protects against brute force attacks on authentication endpoints

#### File Security
- **File Type Validation**: Comprehensive file type checking and validation
- **Size Restrictions**: Configurable file size limits to prevent resource exhaustion
- **Secure Storage**: Files stored with proper access controls and metadata tracking
- **Access Validation**: Download requests validated for proper authorization

#### Payment Security
- **Stripe Integration**: Uses Stripe's secure payment processing with latest API standards
- **Payment Intent Validation**: Secure handling of payment intents and status tracking
- **Data Protection**: Sensitive payment data handled according to PCI compliance standards

## 🛠️ Core Services

### Authentication Service

```python
# Enhanced User Management with Secure Session Handling
POST /service/auth/v1/signup/<collection>/  # Register new user
    - Validates user data and prevents duplicates with enhanced checks
    - Hashes passwords securely using bcrypt with configurable rounds
    - Creates user document in MongoDB with custom hex ID
    - Implements comprehensive input validation and sanitization

POST /service/auth/v1/signin/<collection>/  # User login
    - Validates credentials against stored hash with timing attack protection
    - Creates secure Flask session with user data and session tokens
    - Returns user document on successful authentication
    - Implements rate limiting and brute force protection

GET /service/auth/v1/session/<collection>/  # Get current session
    - Returns current session data for the collection with validation
    - Used for secure session validation and user info retrieval
    - Implements session integrity checks and timeout handling

GET /service/auth/v1/signout/<collection>/  # User logout
    - Clears session data for the specified collection securely
    - Terminates user session with proper cleanup
    - Implements secure session invalidation

PATCH /service/auth/v1/refresh/<collection>/  # Update user data
    - Updates user information in the database with validation
    - Handles password updates with secure re-hashing
    - Validates user existence and permissions before updating
    - Implements data integrity checks and audit logging
```

### Storage Service

```python
# Secure Database Operations with MongoDB and NoSQL Injection Prevention
GET    /service/storage/v1/<collection>/       # List documents
    - Supports secure query parameters with input validation
    - Accepts sanitized JSON query and keys parameters
    - Returns single document or list based on results
    - Implements query parameter validation and sanitization

GET    /service/storage/v1/<collection>/<key>/  # Get single document by ID
    - Retrieves document by _id field with input validation
    - Supports field selection with keys parameter
    - Implements secure document access controls

POST   /service/storage/v1/<collection>/       # Create document(s)
    - Accepts single document or array of documents with validation
    - Generates custom hex IDs for each document
    - Returns inserted document ID(s) with creation metadata
    - Implements input sanitization and data validation

PATCH  /service/storage/v1/<collection>/<key>/  # Update single document
    - Updates document by _id field with secure validation
    - Supports MongoDB update operators ($set, $inc, etc.) with sanitization
    - Implements update operation security controls

PATCH  /service/storage/v1/<collection>/       # Update multiple documents
    - Updates documents matching validated query parameters
    - Supports bulk updates with secure MongoDB operators
    - Implements batch operation security and validation

DELETE /service/storage/v1/<collection>/<key>/  # Delete single document
    - Deletes document by _id field with authorization checks
    - Returns count of deleted documents with audit information
    - Implements secure deletion with proper validation

DELETE /service/storage/v1/<collection>/       # Delete multiple documents
    - Deletes documents matching validated query parameters
    - Returns count of deleted documents with operation details
    - Implements bulk deletion security controls
```

### Archive Service

```python
# Secure File Management with Enhanced Validation
POST /service/archive/v1/upload/  # Upload file
    - Handles file uploads with comprehensive size and type validation
    - Stores files securely with proper access controls
    - Returns file metadata and storage information
    - Implements file type verification and security scanning
    - Supports various file formats with configurable restrictions

GET /service/archive/v1/download/<file_id>/  # Download file
    - Retrieves stored files by unique identifier with access validation
    - Handles secure file streaming for large files
    - Returns appropriate content types and security headers
    - Implements download tracking and access logging

DELETE /service/archive/v1/delete/<file_id>/  # Delete file
    - Removes files from storage with proper authorization
    - Cleans up associated metadata and references
    - Returns deletion confirmation with audit trail
    - Implements secure file deletion practices

GET /service/archive/v1/list/  # List uploaded files
    - Returns list of accessible files with metadata
    - Supports filtering and pagination with security controls
    - Includes file size, upload date, type, and security status
```

### Payment Service

```python
# Stripe Integration for Secure Payment Processing
POST /service/payment/v1/checkout/  # Create payment checkout
    - Creates Stripe payment hosted checkout with specified line items
    - Returns checkout session object
    - Handles payment method configuration and currency settings
    - Implements secure payment flow with Stripe's latest API

GET /service/payment/v1/subscription/  # Check subscription status
    - Creates a subscription schedule with specified line items
    - Returns subscription details and status
    - Provides real-time subscription tracking capabilities
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/galaxy`)
3. Commit your changes (`git commit -m 'added galaxy forming features'`)
4. Push to the branch (`git push origin feature/galaxy`)
5. Open a Pull Request

## 👥 Authors

- **IMAD EL AKHAL** - *Initial work* - [Website](https://ielakhal.com/)
