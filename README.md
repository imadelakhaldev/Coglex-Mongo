# Coglex Intelligence

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1+-green.svg)
![MongoDB](https://img.shields.io/badge/mongodb-5.0+-brightgreen.svg)
![Stripe](https://img.shields.io/badge/stripe-payments-purple.svg)
![Google-Gemini](https://img.shields.io/badge/google-gemini-ai-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Coglex is a comprehensive, production-ready Flask microservices backend framework designed for secure web development. It provides modular services for authentication, data storage, file archival, payments, and AI content generation via Google Gemini, with consistent security, error handling, and configuration management.

## 🚀 Features

- **🔐 Authentication**: JWT-based authentication with session management, OAuth integration (Google, Facebook), and OTP verification
- **🗄️ Storage**: MongoDB CRUD operations with aggregation pipeline support and safe query handling
- **📁 Archive**: Secure file upload, download, deletion, and metadata tracking with file type detection
- **💳 Payments**: Stripe Checkout integration with support for one-time and subscription payments
- **🧠 AI Generation**: Google Gemini integration for text generation, file uploads, and multimodal content
- **🛡️ Security**: API key protection, user authentication decorators, input validation, and secure error handling
- **🏗️ Microservices**: Modular blueprint architecture with consistent patterns across services
- **⚡ Production Ready**: Waitress WSGI server support with environment-driven configuration
- **🔧 Utilities**: Password hashing, JWT token management, colored terminal output, and token counting

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Authentication & Protection](#authentication--protection)
- [API Documentation](#api-documentation)
- [Utility Functions](#utility-functions)
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
├── .gitignore                      # Git ignore patterns
├── .pylintrc                       # Pylint configuration
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
│   │   ├── payment/
│   │   │   ├── routes.py           # Stripe payment endpoints
│   │   │   └── utils.py            # Payment processing utilities
│   │   └── generation/
│   │       ├── routes.py           # Google Gemini endpoints
│   │       └── utils.py            # Gemini utilities
│   ├── gateway/                    # Gateway modules (placeholder for future expansion)
│   ├── static/
│   │   └── documents/              # File upload directory
│   └── templates/                  # Jinja2 templates
```

## 🔧 Prerequisites

- **Python 3.8+**
- **MongoDB 5.0+**
- **Stripe Account** (for payment processing)
- **Google AI API Key** (for Gemini generation)
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

# Google Gemini Configuration
GENERATION_KEY=your-google-ai-api-key

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
```

### Application Configuration (config.py)

Key configuration parameters:

- **Server Settings**:
  - `BASE_URL`: Base server URL (default: `http://127.0.0.1:5000`)
  - `SERVER_HOST`: Server host (default: `0.0.0.0`)
  - `SERVER_PORT`: Server port (default: `5000`)
  - `SERVER_DEBUG`: Development mode flag

- **File Upload Settings**:
  - `MAX_CONTENT_LENGTH`: Max upload size (16 MB)
  - `APP_UPLOAD`: Upload directory (`coglex/static/documents`)
  - `SEND_FILE_MAX_AGE_DEFAULT`: Static file cache TTL

- **Database Settings**:
  - `MONGODB_DATABASE`: Database name (default: `coglex`)
  - `MONGODB_AUTH_COLLECTION`: Users collection (default: `_USERS`)
  - `MONGODB_ARCHIVE_COLLECTION`: Files collection (default: `_ARCHIVE`)

- **AI Generation Settings**:
  - `GENERATION_MODEL`: Default Gemini model (`models/gemini-2.5-flash`)
  - `GENERATION_KEY`: Gemini API key

- **Authentication Settings**:
  - `VERIFICATION_LENGTH`: OTP length (6 digits)
  - `VERIFICATION_EXPIRY`: OTP expiry time (10 minutes)
  - `SERVER_SESSION_LIFETIME`: Session duration (8 days)

## 🔐 Authentication & Protection

The framework provides two main decorators for endpoint protection:

### @protected Decorator
Verifies API key authentication:
```python
@protected(secret: str = config.SERVER_SECRET)
```
- Requires `X-API-Key` header with server secret
- Optional custom secret parameter

### @authenticated Decorator
Validates user session or JWT token:
```python
@authenticated(collection: str = config.MONGODB_AUTH_COLLECTION)
```
- Checks for JWT token in Authorization header or session
- Provides `g.authentication` with user data
- Optional custom collection parameter

### Usage Example
```python
@app.route('/protected-endpoint')
@protected()
@authenticated()
def secure_endpoint():
    user_data = g.authentication
    return {"message": "Access granted", "user": user_data}
```

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
    "role": "user",
    "active": true
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
Authorization: Bearer jwt-token
```

#### User Profile Update
```http
PATCH /service/auth/v1/{user_key}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "document": {
    "$set": {
      "name": "Updated Name"
    }
  }
}
```

#### OAuth Authentication
```http
POST /service/auth/v1/oauth
Content-Type: application/json
X-API-Key: your-server-secret

{
  "provider": "google",
  "code": "authorization_code",
  "redirect_uri": "http://localhost:3000/callback"
}
```

#### OTP Generation
```http
POST /service/auth/v1/passgen
Content-Type: application/json
X-API-Key: your-server-secret

{
  "_key": "user@example.com"
}
```

#### OTP Verification
```http
POST /service/auth/v1/passver
Content-Type: application/json
X-API-Key: your-server-secret

{
  "_key": "user@example.com",
  "_password": "123456"
}
```

### Storage Service (`/service/storage/v1/`)

#### Find Documents
```http
GET /service/storage/v1/{collection}?query={}&projection={}&sort={}&limit=10&skip=0
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

#### Find Single Document
```http
GET /service/storage/v1/{collection}/{document_id}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

#### Insert Document
```http
POST /service/storage/v1/{collection}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "document": {
    "name": "Sample Document",
    "content": "Document content"
  }
}
```

#### Update Document
```http
PATCH /service/storage/v1/{collection}/{document_id}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "document": {
    "$set": {
      "name": "Updated Document"
    }
  }
}
```

#### Delete Document
```http
DELETE /service/storage/v1/{collection}/{document_id}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

#### Aggregation Pipeline
```http
POST /service/storage/v1/{collection}/aggregate
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

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
GET /service/archive/v1/list
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

#### Upload File
```http
POST /service/archive/v1/upload
Content-Type: multipart/form-data
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

file: [binary file data]
```

#### Download File
```http
GET /service/archive/v1/download/{file_id}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

#### Delete File
```http
DELETE /service/archive/v1/destroy/{file_id}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

### Payment Service (`/service/payment/v1/`)

#### Create Checkout Session
```http
POST /service/payment/v1/checkout
Content-Type: application/json
X-API-Key: your-server-secret

{
  "mode": "payment",
  "success_url": "https://example.com/success",
  "cancel_url": "https://example.com/cancel",
  "customer_email": "customer@example.com",
  "line_items": [
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
  ]
}
```

#### Webhook Verification
```http
POST /service/payment/v1/verify
Content-Type: application/json
X-API-Key: your-server-secret

{
  "payload": "webhook_payload",
  "signature": "stripe_signature"
}
```

### Generation Service (`/service/generation/v1/`)

#### Upload File for AI Processing
```http
POST /service/generation/v1/file
Content-Type: multipart/form-data
X-API-Key: your-server-secret

file: [binary file data]
key: optional-google-ai-api-key
```

Response:
```json
{
  "fileData": {
    "fileUri": "ai://file/...",
    "mimeType": "image/png"
  }
}
```

#### Generate Content (Converse)
```http
POST /service/generation/v1/converse
Content-Type: application/json
X-API-Key: your-server-secret

{
  "contents": [
    {
      "role": "user",
      "parts": [
        {"text": "Describe this image in one sentence."},
        {"file_data": {"mime_type": "image/png", "file_uri": "ai://file/..."}}
      ]
    }
  ],
  "system": "You are a helpful assistant.",
  "tools": [
    {
      "name": "getWeather",
      "description": "Get current weather.",
      "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
      }
    }
  ],
  "model": "models/gemini-2.5-flash",
  "key": "optional-google-ai-api-key"
}
```

Response:
```json
[
  {"text": "It looks like a sunset over the ocean."}
]
```

## 🛠️ Utility Functions

The framework includes several utility functions in `utils.py`:

### Password Management
```python
from utils import phash, pcheck

# Hash a password
hashed = phash("my_password")

# Verify a password
is_valid = pcheck("my_password", hashed)
```

### JWT Token Management
```python
from utils import jwtenc, jwtdec
from datetime import datetime, timedelta

# Encode JWT token
token = jwtenc({"user_id": "123"}, datetime.now() + timedelta(hours=1))

# Decode JWT token
payload = jwtdec(token)
```

### Colored Terminal Output
```python
from utils import sprint

# Print colored text
sprint("RED", "Error message")
sprint("GREEN", "Success message")
sprint("BLUE", "Info message")
```

### Token Counting for AI
```python
from utils import tokenize

# Count tokens for Gemini API
token_count = tokenize(["Hello world", "How are you?"])
```

## 🔒 Security Features

- **API Key Protection**: All endpoints protected with server secret
- **JWT Authentication**: Secure token-based user authentication
- **Password Hashing**: bcrypt with salt for password security
- **Input Validation**: Comprehensive request validation
- **File Type Detection**: Secure file upload with type verification
- **Session Management**: Flask session integration with MongoDB
- **OAuth Integration**: Secure third-party authentication
- **CORS Support**: Configurable cross-origin resource sharing
- **Error Handling**: Secure error responses without sensitive data exposure

## 🚀 Development

### Running in Development Mode
```bash
# Set debug mode in config.py
SERVER_DEBUG = True

# Run the application
python run.py
```

### Code Quality
The project includes:
- **Pylint configuration** (`.pylintrc`) with custom rules
- **Git ignore patterns** (`.gitignore`) for Python projects
- **Environment template** (`.env.example`) for easy setup

### Adding New Services
1. Create service directory in `coglex/services/`
2. Add `routes.py` with Flask Blueprint
3. Add `utils.py` with service logic
4. Register blueprint in `coglex/__init__.py`

## 🚀 Deployment

### Production Deployment
```bash
# Set production mode in config.py
SERVER_DEBUG = False

# Run with Waitress WSGI server
python run.py
```

### Environment Setup
1. Set all required environment variables
2. Configure MongoDB connection
3. Set up SMTP server for emails
4. Configure Stripe webhooks
5. Set up Google AI API access

### Docker Deployment (Optional)
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

## 📋 Dependencies

### Core Dependencies
- **Flask 3.1.2**: Web framework
- **PyMongo 4.15.3**: MongoDB driver
- **Stripe 13.0.1**: Payment processing
- **google-genai 1.43.0**: Google Gemini AI
- **PyJWT 2.10.1**: JWT token handling
- **bcrypt 5.0.0**: Password hashing
- **Waitress 3.0.2**: WSGI server

### Additional Dependencies
- **python-dotenv**: Environment variable management
- **python-magic**: File type detection
- **colorama**: Terminal colored output
- **requests**: HTTP client library
- **Werkzeug**: WSGI utilities

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

- **Genesis**: Core microservices architecture (Auth, Storage, Archive, Payment)
- **AI Generation**: Added Google Gemini service (File upload, Converse)
- **Security**: Multi-layer protection and JWT authentication
- **Production**: Waitress WSGI server integration

---

**Built with ❤️ by IMAD EL AKHAL**

*Coglex Intelligence — secure web development with modular microservices and AI.*
