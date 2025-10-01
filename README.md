# Coglex Intelligence

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.1-green.svg)
![MongoDB](https://img.shields.io/badge/mongodb-compatible-brightgreen.svg)
![Stripe](https://img.shields.io/badge/stripe-payments-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A comprehensive, secure backend framework built with Flask and MongoDB, providing microservices architecture for modern web applications. Coglex offers robust authentication, file management, payment processing, and database operations with enterprise-grade security features.

## 🚀 Features

- **🔐 Advanced Authentication System**: Secure user management with bcrypt password hashing, JWT tokens, session management, and timing attack protection
- **📁 Secure File Management**: Complete file upload/download system with type validation, size limits, and secure storage
- **💳 Stripe Payment Integration**: PCI-compliant payment processing with checkout sessions and secure payment intent handling
- **🗄️ MongoDB Integration**: Robust NoSQL database operations with injection prevention and data sanitization
- **🛡️ Multi-layer API Protection**: Comprehensive security with API key authentication, rate limiting, and input validation
- **⚡ Microservices Architecture**: Modular service design for scalability and maintainability

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🔍 Overview

Coglex Intelligence is a production-ready backend framework designed for modern web applications requiring secure, scalable, and maintainable architecture. Built with Flask and MongoDB, it provides a comprehensive suite of services including user authentication, file management, payment processing, and database operations.

### Key Architecture Components

- **Flask Application**: WSGI-compatible web framework with blueprint-based routing
- **MongoDB Integration**: NoSQL database with PyMongo for flexible data operations
- **Microservices Design**: Modular services for authentication, storage, archive, and payments
- **Security Layer**: Multi-tier protection with API keys, JWT tokens, and input validation
- **Production Ready**: Waitress WSGI server for production deployment

## 📁 Project Structure

```
coglex/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── .pylintrc                # Python linting configuration
├── README.md                # Project documentation
├── config.py                # Global configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── utils.py                 # Shared utility functions
└── coglex/                  # Main application package
    ├── __init__.py          # Flask app initialization & decorators
    ├── gateway/             # Gateway modules (extensible)
    ├── services/            # Microservices collection
    │   ├── auth/            # Authentication service
    │   │   ├── routes.py    # Auth API endpoints
    │   │   └── utils.py     # Auth business logic
    │   ├── storage/         # Database operations service
    │   │   ├── routes.py    # Storage API endpoints
    │   │   └── utils.py     # MongoDB CRUD operations
    │   ├── archive/         # File management service
    │   │   ├── routes.py    # File API endpoints
    │   │   └── utils.py     # File operations logic
    │   └── payment/         # Payment processing service
    │       ├── routes.py    # Payment API endpoints
    │       └── utils.py     # Stripe integration logic
    ├── static/              # Static files directory
    └── templates/           # Jinja2 templates directory
```

## 📋 Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or higher)
- **MongoDB** (local instance or MongoDB Atlas)
- **Stripe Account** (for payment processing)
- **Virtual Environment** (strongly recommended)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/imadelakhaldev/coglex.git
cd coglex
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration values
```

### 5. Verify MongoDB Connection
Ensure your MongoDB instance is running and accessible with the provided URI.

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Server Configuration
SERVER_SECRET=your-secure-random-string-here
SERVER_DEBUG=True

# MongoDB Configuration
MONGODB_URI=mongodb://username:password@localhost:27017/database

# SMTP Configuration (Optional)
SMTP_PASSWORD=your-smtp-password

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### Key Configuration Parameters

- **SERVER_SECRET**: Strong API key for authentication (secure random string)
- **MONGODB_URI**: MongoDB connection string with authentication
- **STRIPE_SECRET_KEY**: Secret key from your Stripe dashboard
- **SERVER_DEBUG**: Set to `False` in production

## 📚 API Documentation

### Authentication Service (`/service/auth/v1/`)

**User Registration**
- `POST /service/auth/v1/signup`
- Creates new user accounts with secure password hashing
- Requires: `_key`, `_password`, optional `document`

**User Authentication**
- `POST /service/auth/v1/signin`
- Authenticates users and returns JWT tokens
- Requires: `_key`, `_password`, optional `query`

**User Profile Retrieval**
- `GET /service/auth/v1/<_key>`
- Retrieves user profile information
- Requires: valid API key, optional `query`

**User Profile Update**
- `PATCH /service/auth/v1/<_key>`
- Updates user profile data
- Requires: `document`, optional `query`

### Storage Service (`/service/storage/v1/`)

**Document Operations**
- `GET /service/storage/v1/<collection>/<key>` - Retrieve single document
- `GET /service/storage/v1/<collection>` - Retrieve multiple documents
- `POST /service/storage/v1/<collection>` - Insert documents
- `PATCH /service/storage/v1/<collection>/<key>` - Update single document
- `PATCH /service/storage/v1/<collection>` - Update multiple documents
- `DELETE /service/storage/v1/<collection>/<key>` - Delete single document
- `DELETE /service/storage/v1/<collection>` - Delete multiple documents

**Aggregation Operations**
- `POST /service/storage/v1/<collection>/aggregate` - MongoDB aggregation pipeline

### Archive Service (`/service/archive/v1/`)

**File Management**
- `GET /service/archive/v1/` - List all uploaded files
- `POST /service/archive/v1/` - Upload files with validation
- `GET /service/archive/v1/<reference>` - Download files securely
- `DELETE /service/archive/v1/<reference>` - Delete files and metadata

### Payment Service (`/service/payment/v1/`)

**Stripe Integration**
- `POST /service/payment/v1/` - Create Stripe checkout sessions
- Supports both one-time payments and subscriptions
- Requires: `mode`, `success_url`, `cancel_url`, `email`, `linedata`

## 🛡️ Security Features

### Authentication & Authorization
- **bcrypt Password Hashing**: Secure password storage with configurable rounds
- **JWT Token Management**: Stateless authentication with expiration handling
- **API Key Protection**: Server-level API key validation for all endpoints
- **Session Security**: Secure session management with timeout handling
- **Timing Attack Protection**: Constant-time password comparison

### Data Protection
- **NoSQL Injection Prevention**: Input sanitization and query validation
- **Input Validation**: Comprehensive data validation and sanitization
- **File Security**: File type validation, size limits, and secure storage
- **Data Encryption**: Secure data transmission and storage practices

### API Security
- **Rate Limiting**: Protection against brute force attacks
- **CORS Configuration**: Cross-origin request security
- **Error Handling**: Secure error responses without information leakage
- **Audit Logging**: Comprehensive logging for security monitoring

### Payment Security
- **PCI Compliance**: Stripe integration for secure payment processing
- **Payment Intent Validation**: Secure payment flow with verification
- **Webhook Security**: Stripe webhook signature verification

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

## 🔧 Development

### Running in Development Mode
```bash
# Set debug mode in config.py or .env
SERVER_DEBUG=True
python run.py
```

### Code Quality
```bash
# Run linting
pylint coglex/

# Format code
black coglex/
```

### Testing
```bash
# Run tests (if test suite is available)
python -m pytest tests/
```

## 🚀 Deployment

### Production Configuration
1. Set `SERVER_DEBUG=False` in production
2. Use strong, unique `SERVER_SECRET`
3. Configure MongoDB with authentication
4. Set up SSL/TLS certificates
5. Use environment variables for sensitive data

### WSGI Deployment
The application uses Waitress WSGI server for production deployment:

```python
# Automatic production server when SERVER_DEBUG=False
python run.py
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include error handling
- Write secure code
- Test thoroughly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

## 🔄 Version History

- **Genesis**: Initial release with core microservices architecture
- Comprehensive authentication system
- Secure file management
- Stripe payment integration
- MongoDB operations with security enhancements

---

**Coglex Intelligence** - Secure, Scalable, Production-Ready Backend Framework
