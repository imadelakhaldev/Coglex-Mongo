# Coglex Intelligence

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![MongoDB](https://img.shields.io/badge/mongodb-5.0+-brightgreen.svg)
![Stripe](https://img.shields.io/badge/stripe-payments-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A comprehensive, production-ready Flask microservices backend framework designed for secure web development. Coglex provides a modular architecture with built-in authentication, database operations, file management, and payment processing capabilities.

## 🚀 Features

- **🔐 Advanced Authentication System**: JWT-based authentication with session management and context-aware user access
- **📁 Secure File Management**: Complete file upload, download, and archival system with metadata tracking
- **💳 Stripe Payment Integration**: Full payment processing with checkout sessions and webhook handling
- **🗄️ MongoDB Integration**: Comprehensive CRUD operations with aggregation pipeline support
- **🛡️ Multi-layer API Protection**: Route-level security with API key and authentication decorators
- **🏗️ Microservices Architecture**: Modular service design with independent blueprints
- **⚡ Production Ready**: Waitress WSGI server for production deployment
- **🔧 Advanced Session Management**: Built-in Flask session integration with collection-based token storage

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Advanced Features](#advanced-features)
- [Security Features](#security-features)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 📁 Project Structure

```
coglex/
├── run.py                          # Application entry point with development/production server
├── config.py                       # Global configuration and environment variables
├── utils.py                        # Utility functions (JWT, password hashing, colored output)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── coglex/
│   ├── __init__.py                 # Flask app initialization and decorators
│   ├── services/
│   │   ├── auth/
│   │   │   ├── routes.py           # Authentication endpoints
│   │   │   └── utils.py            # Authentication utilities
│   │   ├── storage/
│   │   │   ├── routes.py           # Database CRUD endpoints
│   │   │   └── utils.py            # MongoDB operations
│   │   ├── archive/
│   │   │   ├── routes.py           # File management endpoints
│   │   │   └── utils.py            # File operations and metadata
│   │   └── payment/
│   │       ├── routes.py           # Stripe payment endpoints
│   │       └── utils.py            # Payment processing utilities
│   ├── static/                     # Static files and assets
│   └── templates/                  # Jinja2 templates
```

## 🔧 Prerequisites

- **Python 3.8+**
- **MongoDB 5.0+**
- **Stripe Account** (for payment processing)
- **Virtual Environment**
- **SMTP Server** (for email functionality)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/imadelakhaldev/coglex.git
   cd coglex
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application:**
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

# MongoDB Configuration
MONGODB_URI=mongodb://username:password@localhost:27017/database

# SMTP Configuration
SMTP_PASSWORD=your-smtp-password

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### Server Configuration

The application supports both development and production modes:

- **Development**: Set `SERVER_DEBUG = True` in `config.py`
- **Production**: Set `SERVER_DEBUG = False` for Waitress WSGI server

## 📚 API Documentation

All endpoints require the `X-API-Key` header with your server secret key.

### Authentication Service (`/service/auth/v1/`)

#### User Registration
```http
POST /service/auth/v1/signup
Content-Type: application/json
X-API-Key: your-server-secret

{
  "_key": "user@example.com",
  "_password": "secure_password",
  "document": {
    "name": "John Doe",
    "role": "user"
  }
}
```

#### User Authentication
```http
POST /service/auth/v1/signin
Content-Type: application/json
X-API-Key: your-server-secret

{
  "_key": "user@example.com",
  "_password": "secure_password",
  "query": {
    "active": true
  }
}
```

#### User Profile Retrieval
```http
GET /service/auth/v1/{user_key}
X-API-Key: your-server-secret
```

#### User Profile Update
```http
PATCH /service/auth/v1/{user_key}
Content-Type: application/json
X-API-Key: your-server-secret

{
  "document": {
    "$set": {
      "name": "Updated Name"
    }
  }
}
```

#### User Signout
```http
GET /service/auth/v1/signout
X-API-Key: your-server-secret
```

### Storage Service (`/service/storage/v1/`)

#### Find Documents
```http
GET /service/storage/v1/{collection}
X-API-Key: your-server-secret
```

#### Find Single Document
```http
GET /service/storage/v1/{collection}/{document_id}
X-API-Key: your-server-secret
```

#### Insert Documents
```http
POST /service/storage/v1/{collection}
Content-Type: application/json
X-API-Key: your-server-secret

{
  "documents": [
    {
      "title": "Document Title",
      "content": "Document content"
    }
  ]
}
```

#### Update Documents
```http
PATCH /service/storage/v1/{collection}/{document_id}
Content-Type: application/json
X-API-Key: your-server-secret

{
  "document": {
    "$set": {
      "title": "Updated Title"
    }
  }
}
```

#### Delete Documents
```http
DELETE /service/storage/v1/{collection}/{document_id}
X-API-Key: your-server-secret
```

#### Aggregation Pipeline
```http
POST /service/storage/v1/{collection}/aggregate
Content-Type: application/json
X-API-Key: your-server-secret

{
  "pipeline": [
    {"$match": {"status": "active"}},
    {"$group": {"_id": "$category", "count": {"$sum": 1}}}
  ]
}
```

### Archive Service (`/service/archive/v1/`)

#### List Files
```http
GET /service/archive/v1/
X-API-Key: your-server-secret
```

#### Upload File
```http
POST /service/archive/v1/
Content-Type: multipart/form-data
X-API-Key: your-server-secret

file: [binary file data]
```

#### Download File
```http
GET /service/archive/v1/{file_id}
X-API-Key: your-server-secret
```

#### Delete File
```http
DELETE /service/archive/v1/{file_id}
X-API-Key: your-server-secret
```

### Payment Service (`/service/payment/v1/`)

#### Create Checkout Session
```http
POST /service/payment/v1/
Content-Type: application/json
X-API-Key: your-server-secret

{
  "mode": "payment",
  "success_url": "https://example.com/success",
  "cancel_url": "https://example.com/cancel",
  "email": "customer@example.com",
  "linedata": [
    {
      "price_data": {
        "currency": "usd",
        "product_data": {
          "name": "Product Name"
        },
        "unit_amount": 2000
      },
      "quantity": 1
    }
  ],
  "metadata": {
    "order_id": "12345"
  }
}
```

## 🔥 Advanced Features

### Session Management

Coglex provides built-in Flask session integration for token storage:

```python
# Check if user session exists for a specific collection
if session.get(config.MONGODB_AUTH_COLLECTION):
    # User has an active session
    token = session.get(config.MONGODB_AUTH_COLLECTION)
```

### Authentication Context

Access the authenticated user model in any protected route:

```python
from flask import g
from coglex import authenticated

@app.route('/protected-route')
@authenticated()
def protected_route():
    # Access current authenticated user
    current_user = g.authentication
    return jsonify({
        'user_id': current_user['_id'],
        'user_key': current_user['_key']
    })
```

### Token-Based Authentication

The framework supports both header-based and session-based authentication:

1. **Header Authentication**: Include `Authorization: Bearer <token>` header
2. **Session Authentication**: Automatic token retrieval from Flask session
3. **Dual Fallback**: Headers take precedence, falls back to session if header is missing

### Custom Decorators

#### `@protected()` Decorator
Protects routes with API key authentication:

```python
from coglex import protected

@app.route('/api/endpoint')
@protected()  # Uses default server secret
def secure_endpoint():
    return jsonify({'message': 'Secure data'})

@app.route('/api/custom')
@protected(secret='custom-secret')  # Custom secret
def custom_secure_endpoint():
    return jsonify({'message': 'Custom secure data'})
```

#### `@authenticated()` Decorator
Protects routes with user authentication:

```python
from coglex import authenticated

@app.route('/user/profile')
@authenticated()  # Uses default auth collection
def user_profile():
    user = g.authentication
    return jsonify(user)

@app.route('/admin/panel')
@authenticated(collection='_ADMINS')  # Custom collection
def admin_panel():
    admin = g.authentication
    return jsonify(admin)
```

### Database Operations

#### Advanced Queries with Filters
```python
from coglex.services.storage.utils import _find

# Find with complex query
users = _find('_USERS', {
    'active': True,
    'role': {'$in': ['admin', 'moderator']},
    'created_at': {'$gte': datetime(2024, 1, 1)}
})

# Find with field projection
users = _find('_USERS', {'active': True}, {'password': 0, 'secret': 0})
```

#### Aggregation Pipelines
```python
from coglex.services.storage.utils import _aggregate

# Complex aggregation
pipeline = [
    {'$match': {'status': 'active'}},
    {'$group': {
        '_id': '$department',
        'count': {'$sum': 1},
        'avg_salary': {'$avg': '$salary'}
    }},
    {'$sort': {'count': -1}}
]

results = _aggregate('employees', pipeline)
```

### File Management

#### Secure File Upload with Validation
```python
from coglex.services.archive.utils import _upload
from werkzeug.datastructures import FileStorage

# File upload with automatic security checks
file_id = _upload(file_object)  # Returns file ID or None if invalid
```

#### File Metadata Tracking
All uploaded files include comprehensive metadata:
- Original filename (secured)
- File path on server
- File size in bytes
- MIME type detection
- Upload timestamp

## 🛡️ Security Features

### Authentication & Authorization
- **JWT Token Security**: HS256 algorithm with configurable expiration
- **Password Hashing**: bcrypt with automatic salt generation
- **Session Management**: Secure Flask session integration
- **Multi-level Authentication**: API key + user authentication

### Data Protection
- **Input Sanitization**: Secure filename handling for uploads
- **Query Injection Prevention**: Parameterized MongoDB queries
- **File Type Validation**: MIME type detection and validation
- **Size Limits**: Configurable file upload size restrictions

### API Security
- **Rate Limiting Ready**: Framework supports rate limiting implementation
- **CORS Configuration**: Configurable cross-origin resource sharing
- **Header Validation**: Required API key validation on all endpoints
- **Error Handling**: Secure error responses without information leakage

### Payment Security
- **PCI Compliance**: Stripe integration for secure payment processing
- **Webhook Verification**: Signature validation for Stripe webhooks
- **Metadata Encryption**: Secure handling of payment metadata

## 🔧 Development

### Running in Development Mode

```bash
# Set debug mode in config.py
SERVER_DEBUG = True

# Run the application
python run.py
```

### Code Quality

```bash
# Install linting tools
pip install pylint black

# Format code
black .

# Lint code
pylint coglex/
```

## 🚀 Deployment

### Production Deployment

1. **Set production configuration:**
   ```python
   # In config.py
   SERVER_DEBUG = False
   ```

2. **Use environment variables:**
   ```bash
   export SERVER_SECRET="your-production-secret"
   export MONGODB_URI="mongodb://production-server:27017/coglex"
   ```

3. **Run with Waitress:**
   ```bash
   python run.py
   ```

### Docker Deployment

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Website**: [https://imadelakhaldev.com/](https://imadelakhaldev.com/)
- **Issues**: Create an issue on GitHub
- **Email**: imadelakhaldev@gmail.com

## 📈 Version History

- **Genesis**: Initial release with core microservices architecture
- **Features**: Authentication, Storage, Archive, and Payment services
- **Security**: Multi-layer protection and JWT authentication
- **Production**: Waitress WSGI server integration

---

**Built with ❤️ by IMAD EL AKHAL**

*Coglex Intelligence - Empowering secure web development through modular microservices architecture.*
