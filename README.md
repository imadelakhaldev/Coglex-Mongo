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

**Generate OAuth Authorization URL:**
```http
POST /service/auth/v1/oauth
Content-Type: application/json
X-API-Key: your-server-secret

{
  "provider": "google",
  "redirect": "http://localhost:3000/callback"
}
```

Response:
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&scope=...&state=...",
  "state": "jwt_state_token"
}
```

**Handle OAuth Callback:**
```http
POST /service/auth/v1/ocall
Content-Type: application/json
X-API-Key: your-server-secret

{
  "provider": "google",
  "redirect": "http://localhost:3000/callback",
  "state": "jwt_state_token_from_authorization",
  "code": "authorization_code_from_provider"
}
```

Response:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "identifier": "google_user_id_123",
  "provider": "google"
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

Response:
```json
{
  "otp_token": "jwt_token_containing_otp",
  "expires_in": 600
}
```

#### OTP Verification
```http
POST /service/auth/v1/passver
Content-Type: application/json
X-API-Key: your-server-secret

{
  "_key": "user@example.com",
  "_password": "123456",
  "token": "jwt_token_from_passgen"
}
```

Response:
```json
{
  "valid": true,
  "message": "OTP verified successfully"
}
```

### Storage Service (`/service/storage/v1/`)

#### Find Multiple Documents
```http
GET /service/storage/v1/{collection}?query={}&keys={}&sort={}&limit=10&skip=0
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

Query Parameters:
- `query`: JSON-encoded MongoDB query filter (optional)
- `keys`: JSON-encoded projection object (optional)
- `sort`: JSON-encoded sort specification (optional)
- `limit`: Maximum number of documents to return (optional)
- `skip`: Number of documents to skip (optional)

Example:
```http
GET /service/storage/v1/products?query={"category":"electronics"}&keys={"name":1,"price":1}&sort={"price":-1}&limit=5
```

#### Find Single Document
```http
GET /service/storage/v1/{collection}/{document_id}?keys={}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

Query Parameters:
- `keys`: JSON-encoded projection object (optional)

#### Insert Multiple Documents
```http
POST /service/storage/v1/{collection}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "documents": [
    {
      "name": "Product 1",
      "price": 29.99,
      "category": "electronics"
    },
    {
      "name": "Product 2", 
      "price": 49.99,
      "category": "books"
    }
  ]
}
```

#### Update Single Document
```http
PATCH /service/storage/v1/{collection}/{document_id}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "document": {
    "$set": {
      "name": "Updated Product Name",
      "last_modified": "2024-01-15T10:30:00Z"
    },
    "$inc": {
      "view_count": 1
    }
  }
}
```

#### Update Multiple Documents
```http
PATCH /service/storage/v1/{collection}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "document": {
    "$set": {
      "status": "archived"
    }
  },
  "query": {
    "created_date": {
      "$lt": "2023-01-01T00:00:00Z"
    }
  }
}
```

#### Delete Single Document
```http
DELETE /service/storage/v1/{collection}/{document_id}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

#### Delete Multiple Documents
```http
DELETE /service/storage/v1/{collection}
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "query": {
    "status": "inactive",
    "last_login": {
      "$lt": "2023-01-01T00:00:00Z"
    }
  }
}
```

#### Aggregation Pipeline
```http
POST /service/storage/v1/{collection}/aggregate
Content-Type: application/json
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

{
  "pipeline": [
    {
      "$match": {
        "status": "active",
        "created_date": {
          "$gte": "2024-01-01T00:00:00Z"
        }
      }
    },
    {
      "$group": {
        "_id": "$category",
        "count": {"$sum": 1},
        "total_value": {"$sum": "$price"},
        "avg_price": {"$avg": "$price"}
      }
    },
    {
      "$sort": {
        "count": -1
      }
    },
    {
      "$limit": 10
    }
  ]
}
```

Response:
```json
[
  {
    "_id": "electronics",
    "count": 25,
    "total_value": 1250.75,
    "avg_price": 50.03
  },
  {
    "_id": "books", 
    "count": 18,
    "total_value": 540.50,
    "avg_price": 30.03
  }
]
```

### Archive Service (`/service/archive/v1/`)

#### List Files
```http
GET /service/archive/v1/?query={}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

Query Parameters:
- `query`: JSON-encoded MongoDB query filter (optional)

Example:
```http
GET /service/archive/v1/?query={"mimetype":"image/png","size":{"$lt":1048576}}
```

Response:
```json
[
  {
    "_id": "file_id_123",
    "filename": "document.pdf",
    "mimetype": "application/pdf",
    "size": 2048576,
    "uploaded_at": "2024-01-15T10:30:00Z",
    "metadata": {
      "uploader": "user@example.com",
      "description": "Important document"
    }
  }
]
```

#### Upload File
```http
POST /service/archive/v1/
Content-Type: multipart/form-data
X-API-Key: your-server-secret
Authorization: Bearer jwt-token

file: [binary file data]
metadata: {"description": "User uploaded file", "category": "documents"}
```

Response:
```json
{
  "_id": "file_id_123",
  "filename": "uploaded_document.pdf",
  "mimetype": "application/pdf",
  "size": 2048576,
  "filepath": "/path/to/stored/file",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "metadata": {
    "description": "User uploaded file",
    "category": "documents"
  }
}
```

#### Download File
```http
GET /service/archive/v1/{file_reference}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

Response: Binary file download with appropriate headers:
- `Content-Disposition: attachment; filename="original_filename.ext"`
- `Content-Type: detected/mime-type`

#### Delete File
```http
DELETE /service/archive/v1/{file_reference}
X-API-Key: your-server-secret
Authorization: Bearer jwt-token
```

Response:
```json
{
  "deleted": true,
  "file_id": "file_id_123",
  "message": "File deleted successfully"
}
```

### Payment Service (`/service/payment/v1/`)

#### Create Checkout Session
```http
POST /service/payment/v1/checkout
Content-Type: application/json
X-API-Key: your-server-secret

{
  "mode": "payment",
  "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://example.com/cancel",
  "email": "customer@example.com",
  "linedata": [
    {
      "price_data": {
        "currency": "usd",
        "product_data": {
          "name": "Premium Subscription",
          "description": "Monthly premium access",
          "images": ["https://example.com/product-image.jpg"]
        },
        "unit_amount": 2999
      },
      "quantity": 1
    },
    {
      "price": "price_1234567890",
      "quantity": 2
    }
  ],
  "metadata": {
    "user_id": "user_123",
    "order_id": "order_456",
    "source": "web_app"
  }
}
```

**For Subscription Mode:**
```http
POST /service/payment/v1/checkout
Content-Type: application/json
X-API-Key: your-server-secret

{
  "mode": "subscription",
  "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://example.com/cancel",
  "email": "customer@example.com",
  "linedata": [
    {
      "price": "price_recurring_monthly_2999",
      "quantity": 1
    }
  ],
  "metadata": {
    "user_id": "user_123",
    "plan": "premium_monthly"
  }
}
```

Response:
```json
{
  "id": "cs_test_1234567890",
  "url": "https://checkout.stripe.com/pay/cs_test_1234567890#fidkdWxOYHwnPyd1blpxYHZxWjA0S...",
  "payment_status": "unpaid",
  "customer_email": "customer@example.com",
  "mode": "payment",
  "metadata": {
    "user_id": "user_123",
    "order_id": "order_456"
  }
}
```

### Generation Service (`/service/generation/v1/`)

#### Upload File for AI Processing
```http
POST /service/generation/v1/file
Content-Type: multipart/form-data
X-API-Key: your-server-secret

file: [binary file data - images, documents, audio, video]
key: optional-google-ai-api-key
```

**Supported File Types:**
- **Images**: PNG, JPEG, GIF, WebP, BMP, ICO
- **Documents**: PDF, TXT, HTML, CSS, JavaScript, Python, etc.
- **Audio**: WAV, MP3, AIFF, AAC, OGG, FLAC
- **Video**: MP4, MOV, AVI, FLV, MPG, WebM, WMV, 3GPP

Response:
```json
{
  "fileData": {
    "fileUri": "https://generativelanguage.googleapis.com/v1beta/files/abc123def456",
    "mimeType": "image/png",
    "name": "files/abc123def456",
    "displayName": "uploaded_image.png",
    "sizeBytes": "1048576",
    "createTime": "2024-01-15T10:30:00.123456Z",
    "updateTime": "2024-01-15T10:30:00.123456Z",
    "expirationTime": "2024-01-17T10:30:00.123456Z",
    "sha256Hash": "abcd1234...",
    "uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123def456"
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
        {
          "text": "Analyze this image and describe what you see in detail."
        },
        {
          "fileData": {
            "mimeType": "image/png",
            "fileUri": "https://generativelanguage.googleapis.com/v1beta/files/abc123def456"
          }
        }
      ]
    }
  ],
  "systemInstruction": {
    "parts": [
      {
        "text": "You are an expert image analyst. Provide detailed, accurate descriptions of images including objects, people, settings, colors, and any text visible in the image."
      }
    ]
  },
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "getWeatherInfo",
          "description": "Get current weather information for a specific location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and country, e.g. 'New York, USA'"
              },
              "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
              }
            },
            "required": ["location"]
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.7,
    "topK": 40,
    "topP": 0.95,
    "maxOutputTokens": 2048,
    "stopSequences": ["END"]
  },
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH", 
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ],
  "model": "models/gemini-2.0-flash-exp",
  "key": "optional-google-ai-api-key"
}
```

**Simple Text Generation:**
```http
POST /service/generation/v1/converse
Content-Type: application/json
X-API-Key: your-server-secret

{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Write a short story about a robot learning to paint."
        }
      ]
    }
  ]
}
```

**Multi-turn Conversation:**
```http
POST /service/generation/v1/converse
Content-Type: application/json
X-API-Key: your-server-secret

{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "What is the capital of France?"
        }
      ]
    },
    {
      "role": "model",
      "parts": [
        {
          "text": "The capital of France is Paris."
        }
      ]
    },
    {
      "role": "user", 
      "parts": [
        {
          "text": "What is its population?"
        }
      ]
    }
  ]
}
```

Response:
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "The image shows a beautiful sunset over a calm ocean. The sky is painted in vibrant shades of orange, pink, and purple, with wispy clouds scattered across the horizon. In the foreground, there's a silhouette of a person standing on what appears to be a wooden pier or dock, creating a peaceful and contemplative scene."
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0,
      "safetyRatings": [
        {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "probability": "NEGLIGIBLE"
        },
        {
          "category": "HARM_CATEGORY_HATE_SPEECH",
          "probability": "NEGLIGIBLE"
        }
      ]
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 15,
    "candidatesTokenCount": 67,
    "totalTokenCount": 82
  }
}
```

## 🛠️ Utility Functions

The framework includes several utility functions in `utils.py`:

### Password Management
```python
from utils import phash, pcheck

# Hash a password with bcrypt and salt
hashed_password = phash("my_secure_password")
print(hashed_password)  # $2b$12$abcd1234...

# Verify a password against its hash
is_valid = pcheck("my_secure_password", hashed_password)
print(is_valid)  # True

# Invalid password check
is_invalid = pcheck("wrong_password", hashed_password)
print(is_invalid)  # False
```

### JWT Token Management
```python
from utils import jwtenc, jwtdec
from datetime import timedelta

# Encode JWT token with expiration
user_data = {"user_id": "123", "email": "user@example.com", "role": "admin"}
token = jwtenc(user_data, expiration=timedelta(hours=24))
print(token)  # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# Encode JWT token without expiration (permanent until server secret changes)
permanent_token = jwtenc({"api_key": "special_access"})

# Decode JWT token
decoded_data = jwtdec(token)
print(decoded_data)  # {"user_id": "123", "email": "user@example.com", "role": "admin"}

# Handle expired or invalid tokens
invalid_data = jwtdec("invalid.jwt.token")
print(invalid_data)  # None

# Custom secret key
custom_token = jwtenc({"data": "sensitive"}, key="custom_secret_key")
custom_decoded = jwtdec(custom_token, key="custom_secret_key")
```

### Colored Terminal Output
```python
from utils import sprint

# Available colors: RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, WHITE, BLACK
sprint("RED", "❌ Error: Database connection failed")
sprint("GREEN", "✅ Success: User authenticated successfully")
sprint("BLUE", "ℹ️ Info: Processing request...")
sprint("YELLOW", "⚠️ Warning: Rate limit approaching")
sprint("MAGENTA", "🔧 Debug: Variable value = 42")
sprint("CYAN", "📡 Network: Sending API request")

# Example usage in error handling
try:
    # Some operation
    result = perform_operation()
    sprint("GREEN", f"Operation completed: {result}")
except Exception as e:
    sprint("RED", f"Operation failed: {str(e)}")
```

### Token Counting for AI (Google Gemini)
```python
from utils import tokenize
from google.genai import types

# Count tokens for simple text
text_content = ["Hello world", "How are you today?", "This is a test message."]
token_count = tokenize(text_content)
print(f"Token count: {token_count}")  # Token count: 12

# Count tokens for complex content with files
complex_content = [
    "Analyze this image:",
    types.Content(
        role="user",
        parts=[
            types.Part.from_text("What do you see in this image?"),
            types.Part.from_uri("https://example.com/image.jpg", mime_type="image/jpeg")
        ]
    )
]
complex_token_count = tokenize(complex_content)

# Count tokens with custom model and API key
custom_count = tokenize(
    contents=["Custom content to analyze"],
    model="models/gemini-1.5-pro",
    key="your_custom_api_key"
)

# Example usage for cost estimation
def estimate_cost(content_list, cost_per_1k_tokens=0.002):
    tokens = tokenize(content_list)
    estimated_cost = (tokens / 1000) * cost_per_1k_tokens
    sprint("BLUE", f"Estimated tokens: {tokens}")
    sprint("YELLOW", f"Estimated cost: ${estimated_cost:.4f}")
    return tokens, estimated_cost
```

### Advanced Utility Examples

**Combining Utilities for Authentication Flow:**
```python
from utils import phash, pcheck, jwtenc, jwtdec, sprint
from datetime import timedelta

def register_user(email, password):
    """Complete user registration with password hashing and token generation."""
    try:
        # Hash the password
        hashed_password = phash(password)
        
        # Store user in database (pseudo-code)
        user_data = {
            "email": email,
            "password": hashed_password,
            "created_at": datetime.now(),
            "active": True
        }
        # db.users.insert_one(user_data)
        
        # Generate JWT token for immediate login
        token_payload = {"email": email, "user_id": "generated_id"}
        auth_token = jwtenc(token_payload, expiration=timedelta(days=7))
        
        sprint("GREEN", f"✅ User {email} registered successfully")
        return {"token": auth_token, "user": user_data}
        
    except Exception as e:
        sprint("RED", f"❌ Registration failed: {str(e)}")
        return None

def authenticate_user(email, password):
    """Authenticate user with password verification and token generation."""
    try:
        # Retrieve user from database (pseudo-code)
        # user = db.users.find_one({"email": email})
        user = {"email": email, "password": "$2b$12$stored_hash..."}
        
        if not user:
            sprint("YELLOW", f"⚠️ User {email} not found")
            return None
            
        # Verify password
        if not pcheck(password, user["password"]):
            sprint("RED", f"❌ Invalid password for {email}")
            return None
            
        # Generate new session token
        token_payload = {"email": email, "user_id": user.get("_id")}
        session_token = jwtenc(token_payload, expiration=timedelta(hours=8))
        
        sprint("GREEN", f"✅ User {email} authenticated successfully")
        return {"token": session_token, "user": user}
        
    except Exception as e:
        sprint("RED", f"❌ Authentication failed: {str(e)}")
        return None
```

**AI Content Processing with Token Management:**
```python
from utils import tokenize, sprint

def process_ai_content(content_list, max_tokens=8000):
    """Process AI content with token limit checking."""
    try:
        # Count tokens before processing
        token_count = tokenize(content_list)
        
        if token_count > max_tokens:
            sprint("YELLOW", f"⚠️ Content exceeds token limit: {token_count}/{max_tokens}")
            return None
            
        sprint("BLUE", f"📊 Processing {token_count} tokens")
        
        # Process with AI service (pseudo-code)
        # result = ai_service.generate(content_list)
        
        sprint("GREEN", f"✅ AI processing completed")
        return {"tokens_used": token_count, "result": "generated_content"}
        
    except Exception as e:
        sprint("RED", f"❌ AI processing failed: {str(e)}")
        return None
```

## 🔒 Security Features

Coglex Intelligence implements multiple layers of security to protect your application and user data:

### 1. API Key Protection
- **Server Secret**: All JWT tokens are signed with `SERVER_SECRET` from environment variables
- **Key Rotation**: Change `SERVER_SECRET` to invalidate all existing tokens
- **Environment Isolation**: Secrets are never hardcoded, always loaded from `.env` files

```python
# Example: Secure API key management
import os
from config import SERVER_SECRET

# Never do this (hardcoded secrets)
# SECRET = "my-secret-key-123"

# Always do this (environment variables)
SECRET = os.getenv('SERVER_SECRET') or SERVER_SECRET
```

### 2. JWT Token Security
- **Signed Tokens**: All JWTs use HMAC-SHA256 signing algorithm
- **Expiration Control**: Configurable token lifetimes via `SERVER_SESSION_LIFETIME`
- **Payload Validation**: Automatic token validation in protected routes
- **Secure Headers**: Tokens transmitted via Authorization Bearer headers

```python
# Token security example
from utils import jwtenc, jwtdec
from datetime import timedelta

# Generate secure token with expiration
user_token = jwtenc(
    payload={"user_id": "123", "role": "user"},
    expiration=timedelta(hours=8)  # Auto-expires after 8 hours
)

# Validate token (returns None if invalid/expired)
decoded = jwtdec(user_token)
if decoded is None:
    # Token is invalid, expired, or tampered with
    return {"error": "Invalid authentication"}, 401
```

### 3. Password Security
- **bcrypt Hashing**: Industry-standard password hashing with salt
- **Automatic Salting**: Each password gets a unique salt
- **Configurable Rounds**: bcrypt work factor for computational cost
- **No Plain Text**: Passwords never stored in plain text

```python
from utils import phash, pcheck

# Secure password handling
def secure_password_flow(plain_password):
    # Hash with automatic salt generation
    hashed = phash(plain_password)  # $2b$12$randomsalt...
    
    # Store hashed password (never plain text)
    user_data = {
        "email": "user@example.com",
        "password": hashed,  # Secure hash
        "created_at": datetime.now()
    }
    
    # Later verification
    is_valid = pcheck(plain_password, hashed)
    return is_valid
```

### 4. Input Validation & Sanitization
- **Request Validation**: All endpoints validate required parameters
- **Type Checking**: Automatic type validation for request data
- **SQL Injection Prevention**: MongoDB queries use parameterized operations
- **XSS Protection**: Input sanitization for user-generated content

```python
# Example: Secure database operations
from coglex.services.storage.utils import find_one

# Secure query (parameterized)
user = find_one(
    collection="users",
    query={"email": user_email},  # Safe parameter binding
    projection={"password": 0}    # Exclude sensitive fields
)

# Never do this (vulnerable to injection)
# query = f"SELECT * FROM users WHERE email = '{user_email}'"
```

### 5. File Upload Security
- **MIME Type Validation**: Strict file type checking
- **File Size Limits**: Configurable upload size restrictions
- **Virus Scanning**: Integration ready for antivirus scanning
- **Secure Storage**: Files stored with unique identifiers

```python
# Secure file upload example
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'text/plain', 'application/json',
    'audio/mpeg', 'audio/wav', 'video/mp4', 'video/webm'
}

def validate_file_upload(file_data, mime_type):
    # MIME type validation
    if mime_type not in ALLOWED_MIME_TYPES:
        return False, "File type not allowed"
    
    # File size validation (10MB limit)
    if len(file_data) > 10 * 1024 * 1024:
        return False, "File too large"
    
    # Additional security checks
    # - Magic number validation
    # - Virus scanning integration
    # - Content analysis
    
    return True, "File is safe"
```

### 6. Session Management
- **Secure Sessions**: JWT-based stateless sessions
- **Session Timeout**: Automatic expiration via `SERVER_SESSION_LIFETIME`
- **Session Invalidation**: Logout functionality clears client tokens
- **Concurrent Sessions**: Multiple device support with individual tokens

```python
# Session management example
from config import SERVER_SESSION_LIFETIME
from datetime import timedelta

# Create session with configured lifetime
session_token = jwtenc(
    payload={"user_id": user_id, "session_id": generate_session_id()},
    expiration=timedelta(minutes=SERVER_SESSION_LIFETIME)
)

# Session validation middleware
@protected()
def protected_endpoint():
    # Automatic session validation
    # Token must be valid and not expired
    current_user = request.current_user  # Populated by @protected
    return {"user": current_user}
```

### 7. OAuth Security
- **State Parameter**: CSRF protection for OAuth flows
- **Secure Redirects**: Validated redirect URLs
- **Token Exchange**: Secure authorization code flow
- **Scope Limitation**: Minimal required permissions

```python
# OAuth security implementation
def generate_oauth_url(provider, redirect_uri):
    # Generate cryptographically secure state parameter
    state = secrets.token_urlsafe(32)
    
    # Store state for validation (in production, use Redis/database)
    oauth_states[state] = {
        "created_at": datetime.now(),
        "redirect_uri": redirect_uri,
        "provider": provider
    }
    
    # Build secure authorization URL
    auth_url = f"{PROVIDER_AUTH_URL}?client_id={CLIENT_ID}&state={state}&..."
    return auth_url, state

def validate_oauth_callback(state, code):
    # Validate state parameter (CSRF protection)
    if state not in oauth_states:
        raise SecurityError("Invalid OAuth state")
    
    # Check state expiration (prevent replay attacks)
    state_data = oauth_states[state]
    if datetime.now() - state_data["created_at"] > timedelta(minutes=10):
        raise SecurityError("OAuth state expired")
    
    # Exchange code for token securely
    # ... secure token exchange logic
```

### 8. CORS Configuration
- **Origin Validation**: Configurable allowed origins
- **Method Restrictions**: Limited HTTP methods per endpoint
- **Header Control**: Secure header management
- **Credential Handling**: Secure cookie and authentication handling

```python
# CORS security configuration
from flask_cors import CORS

# Secure CORS setup
CORS(app, 
    origins=["https://yourdomain.com", "https://app.yourdomain.com"],
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
    max_age=3600  # Cache preflight for 1 hour
)
```

### 9. Error Handling Security
- **Information Disclosure Prevention**: Generic error messages in production
- **Detailed Logging**: Comprehensive error logging for debugging
- **Rate Limiting Ready**: Structure supports rate limiting implementation
- **Graceful Degradation**: Secure fallbacks for service failures

```python
# Secure error handling
def secure_error_handler(error):
    # Log detailed error for developers
    sprint("RED", f"Error: {str(error)} | User: {request.user_id} | IP: {request.remote_addr}")
    
    # Return generic message to client (prevent information disclosure)
    if app.config.get('DEBUG'):
        return {"error": str(error)}, 500
    else:
        return {"error": "Internal server error"}, 500
```

### 10. Database Security
- **Connection Security**: Encrypted MongoDB connections
- **Authentication**: Database user authentication
- **Query Parameterization**: Prevents NoSQL injection
- **Field Projection**: Sensitive data exclusion from responses

```python
# Secure database operations
def secure_user_lookup(user_id):
    # Safe query with projection (exclude sensitive fields)
    user = find_one(
        collection="users",
        query={"_id": ObjectId(user_id)},
        projection={
            "password": 0,      # Never return password hash
            "reset_token": 0,   # Exclude reset tokens
            "internal_notes": 0 # Exclude internal data
        }
    )
    return user
```

### Security Best Practices

1. **Environment Variables**: Always use `.env` files for secrets
2. **HTTPS Only**: Deploy with SSL/TLS certificates
3. **Regular Updates**: Keep dependencies updated
4. **Security Headers**: Implement security headers (CSP, HSTS, etc.)
5. **Monitoring**: Log security events and monitor for anomalies
6. **Backup Security**: Encrypt backups and secure storage
7. **Access Control**: Implement role-based access control (RBAC)
8. **Audit Trails**: Log all sensitive operations

### Security Checklist

- [ ] All secrets in environment variables
- [ ] HTTPS enabled in production
- [ ] Database connections encrypted
- [ ] File upload validation implemented
- [ ] Rate limiting configured
- [ ] Security headers added
- [ ] Error handling sanitized
- [ ] Logging and monitoring active
- [ ] Regular security updates scheduled
- [ ] Backup encryption enabled

## 🚀 Development & Deployment

### Development Environment

#### Running in Debug Mode
```bash
# Set debug mode in config.py or environment
export SERVER_DEBUG=true

# Run the development server
python run.py

# Server will start with:
# - Hot reloading enabled
# - Detailed error messages
# - Debug logging
# - Flask development server
```

#### Development Configuration
```python
# config.py - Development settings
SERVER_DEBUG = True
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Development Tools Integration

**VS Code Configuration** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreter": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintPath": "./venv/bin/pylint",
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

**PyLint Configuration** (`.pylintrc`):
```ini
[MASTER]
load-plugins=pylint_flask

[MESSAGES CONTROL]
disable=missing-docstring,too-few-public-methods

[FORMAT]
max-line-length=100
```

### Production Deployment

#### Production Configuration
```python
# config.py - Production settings
SERVER_DEBUG = False
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# Use production WSGI server (Waitress)
# Configured automatically in run.py
```

#### Environment Setup for Production
```bash
# 1. Create production environment file
cp .env.example .env.production

# 2. Configure production variables
nano .env.production

# Required production variables:
SERVER_SECRET=your-super-secure-secret-key-here
MONGODB_URI=mongodb://username:password@host:port/database
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
GENERATION_KEY=your-google-ai-api-key
SMTP_PASSWORD=your-smtp-password

# 3. Set production environment
export FLASK_ENV=production
export SERVER_DEBUG=false
```

#### Production Deployment Options

**1. Traditional Server Deployment:**
```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
source .env.production

# Run with production server (Waitress)
python run.py

# Or run directly with Waitress
waitress-serve --host=0.0.0.0 --port=8000 run:app
```

**2. Docker Deployment:**

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "run.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  coglex:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SERVER_DEBUG=false
      - SERVER_HOST=0.0.0.0
      - SERVER_PORT=8000
    env_file:
      - .env.production
    depends_on:
      - mongodb
    restart: unless-stopped

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - coglex
    restart: unless-stopped

volumes:
  mongodb_data:
```

**3. Cloud Platform Deployment:**

**Heroku:**
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SERVER_SECRET=your-secret
heroku config:set MONGODB_URI=your-mongodb-uri
heroku config:set STRIPE_SECRET_KEY=your-stripe-key
# ... set all required variables

# Deploy
git push heroku main
```

Create `Procfile`:
```
web: python run.py
```

**AWS EC2:**
```bash
# 1. Launch EC2 instance (Ubuntu 20.04 LTS)
# 2. Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# 4. Clone repository
git clone https://github.com/yourusername/coglex.git
cd coglex

# 5. Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configure environment
cp .env.example .env
nano .env  # Add your configuration

# 7. Setup systemd service
sudo nano /etc/systemd/system/coglex.service
```

Systemd service file (`/etc/systemd/system/coglex.service`):
```ini
[Unit]
Description=Coglex Intelligence API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/coglex
Environment=PATH=/home/ubuntu/coglex/venv/bin
ExecStart=/home/ubuntu/coglex/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Google Cloud Platform:**
```yaml
# app.yaml for Google App Engine
runtime: python39

env_variables:
  SERVER_SECRET: "your-secret"
  MONGODB_URI: "your-mongodb-uri"
  # ... other variables

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

### Performance Optimization

#### Database Optimization
```python
# MongoDB indexing for better performance
from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]

# Create indexes for common queries
db.users.create_index([("email", ASCENDING)], unique=True)
db.users.create_index([("created_at", DESCENDING)])
db.files.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
db.payments.create_index([("user_id", ASCENDING), ("status", ASCENDING)])

# Compound indexes for complex queries
db.documents.create_index([
    ("user_id", ASCENDING),
    ("category", ASCENDING),
    ("created_at", DESCENDING)
])
```

#### Caching Strategy
```python
# Redis caching implementation (optional)
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator

# Usage example
@cache_result(expiration=600)  # Cache for 10 minutes
def get_user_profile(user_id):
    return find_one("users", {"_id": ObjectId(user_id)})
```

#### Load Balancing with Nginx
```nginx
# nginx.conf
upstream coglex_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://coglex_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static file serving
    location /static/ {
        alias /path/to/static/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Monitoring & Logging

#### Application Monitoring
```python
# Enhanced logging configuration
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not app.debug:
        # Production logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/coglex.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Coglex Intelligence startup')

# Usage in run.py
setup_logging(app)
```

#### Health Check Endpoint
```python
# Add to main application
@app.route('/health')
def health_check():
    """Health check endpoint for load balancers."""
    try:
        # Check database connection
        db_status = check_database_connection()
        
        # Check external services
        stripe_status = check_stripe_connection()
        ai_status = check_ai_service()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": db_status,
                "stripe": stripe_status,
                "ai_service": ai_status
            }
        }, 200
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, 503
```

### Backup & Recovery

#### Database Backup Strategy
```bash
#!/bin/bash
# backup.sh - MongoDB backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mongodb"
DB_NAME="your_database_name"

# Create backup directory
mkdir -p $BACKUP_DIR

# Perform backup
mongodump --uri="$MONGODB_URI" --db=$DB_NAME --out=$BACKUP_DIR/$DATE

# Compress backup
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz -C $BACKUP_DIR $DATE

# Remove uncompressed backup
rm -rf $BACKUP_DIR/$DATE

# Keep only last 30 days of backups
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.tar.gz"
```

#### Automated Backup with Cron
```bash
# Add to crontab (crontab -e)
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1

# Weekly full backup at 3 AM on Sundays
0 3 * * 0 /path/to/full_backup.sh >> /var/log/backup.log 2>&1
```

### Scaling Considerations

#### Horizontal Scaling
- **Stateless Design**: JWT-based authentication enables horizontal scaling
- **Database Sharding**: MongoDB supports automatic sharding for large datasets
- **Load Balancing**: Multiple application instances behind load balancer
- **Microservice Architecture**: Each service can be scaled independently

#### Vertical Scaling
- **Memory Optimization**: Tune MongoDB memory usage
- **CPU Optimization**: Use multiprocessing for CPU-intensive tasks
- **Storage Optimization**: SSD storage for better I/O performance

#### Auto-scaling Configuration
```yaml
# Kubernetes auto-scaling example
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: coglex-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: coglex-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
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

## 📋 Dependencies

### Core Dependencies
```
Flask==3.1.2              # Web framework
PyMongo==4.15.3           # MongoDB driver
Stripe==13.0.1            # Payment processing
google-genai==1.43.0      # Google Gemini AI SDK
PyJWT==2.10.1             # JWT token handling
bcrypt==5.0.0             # Password hashing
Waitress==3.0.2           # Production WSGI server
```

### Additional Dependencies
```
python-dotenv==1.0.0      # Environment variable management
python-magic==0.4.27      # File type detection
colorama==0.4.6           # Terminal colored output
requests==2.31.0          # HTTP client library
Werkzeug==3.0.1           # WSGI utilities
flask-cors==4.0.0         # Cross-Origin Resource Sharing
click==8.1.7              # Command line interface
itsdangerous==2.1.2       # Cryptographic signing
Jinja2==3.1.2             # Template engine
MarkupSafe==2.1.3         # String handling
blinker==1.6.3            # Signal support
certifi==2023.7.22        # SSL certificates
charset-normalizer==3.3.0 # Character encoding
idna==3.4                 # Internationalized domain names
urllib3==2.0.6            # HTTP library
```

### Development Dependencies (Optional)
```
pylint==3.0.3             # Code linting
black==23.12.1            # Code formatting
pytest==7.4.3            # Testing framework
pytest-cov==4.1.0        # Coverage reporting
flake8==6.1.0             # Style guide enforcement
mypy==1.8.0               # Static type checking
pre-commit==3.6.0        # Git hooks framework
bandit==1.7.5             # Security linting
```

### Installation Commands
```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pylint black pytest pytest-cov flake8 mypy pre-commit bandit

# Install with specific versions (recommended for production)
pip install Flask==3.1.2 PyMongo==4.15.3 google-genai==1.43.0

# Upgrade all dependencies
pip install --upgrade -r requirements.txt

# Install in editable mode for development
pip install -e .
```

### Dependency Management Best Practices

**Virtual Environment Setup:**
```bash
# Create virtual environment
python -m venv coglex-env

# Activate virtual environment
# On macOS/Linux:
source coglex-env/bin/activate
# On Windows:
coglex-env\Scripts\activate

# Install dependencies in virtual environment
pip install -r requirements.txt

# Generate requirements file with exact versions
pip freeze > requirements.txt

# Generate requirements file without system packages
pip list --format=freeze --local > requirements.txt
```

**Security and Updates:**
```bash
# Check for security vulnerabilities
pip audit

# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages (use with caution in production)
pip install --upgrade $(pip list --outdated --format=freeze | cut -d'=' -f1)

# Check for known security issues
bandit -r coglex/

# Scan for dependency vulnerabilities
safety check
```

**Docker Dependencies:**
```dockerfile
# Multi-stage build for optimized production images
FROM python:3.9-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

# Production stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Add local packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000
CMD ["python", "run.py"]
```

**Requirements Management:**
```bash
# Create requirements files for different environments
pip freeze > requirements/base.txt
pip freeze > requirements/development.txt
pip freeze > requirements/production.txt

# Install from specific requirements file
pip install -r requirements/production.txt

# Use pip-tools for better dependency management
pip install pip-tools
pip-compile requirements.in  # Generates requirements.txt
pip-sync requirements.txt    # Syncs environment with requirements
```

### Compatibility Matrix

| Python Version | Flask Version | MongoDB Version | Status |
|---------------|---------------|-----------------|---------|
| 3.8           | 3.1.x         | 5.0+           | ✅ Supported |
| 3.9           | 3.1.x         | 5.0+           | ✅ Recommended |
| 3.10          | 3.1.x         | 6.0+           | ✅ Recommended |
| 3.11          | 3.1.x         | 6.0+           | ✅ Latest |
| 3.12          | 3.1.x         | 7.0+           | ⚠️ Beta |

### Performance Considerations

**Memory Usage:**
- Base installation: ~50MB
- With all dependencies: ~150MB
- Runtime memory: 100-500MB (depending on usage)

**Startup Time:**
- Cold start: 2-5 seconds
- Warm start: 0.5-1 second
- With preloading: <0.5 seconds

## 🤝 Contributing

We welcome contributions to Coglex Intelligence! Here's how you can help improve the project:

### Getting Started

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/coglex.git
   cd coglex
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pylint black pytest pytest-cov flake8 mypy pre-commit
   
   # Set up pre-commit hooks
   pre-commit install
   ```

3. **Create Environment Configuration**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Add your development configuration
   nano .env
   ```

### Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   # or
   git checkout -b bugfix/fix-issue-123
   # or
   git checkout -b docs/update-readme
   ```

2. **Make Your Changes**
   - Follow the existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass

3. **Code Quality Checks**
   ```bash
   # Run linting
   pylint coglex/
   
   # Format code
   black coglex/ utils.py config.py run.py
   
   # Type checking
   mypy coglex/
   
   # Security scanning
   bandit -r coglex/
   
   # Run tests
   pytest tests/ -v --cov=coglex
   ```

4. **Commit Your Changes**
   ```bash
   # Stage your changes
   git add .
   
   # Commit with descriptive message
   git commit -m "feat: add user profile management endpoint"
   # or
   git commit -m "fix: resolve JWT token expiration issue"
   # or
   git commit -m "docs: update API documentation for auth service"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/amazing-feature
   ```
   Then create a Pull Request on GitHub.

### Contribution Guidelines

#### Code Style
- **Python**: Follow PEP 8 guidelines
- **Line Length**: Maximum 100 characters
- **Imports**: Use absolute imports, group by standard/third-party/local
- **Docstrings**: Use Google-style docstrings for functions and classes
- **Type Hints**: Add type hints for function parameters and return values

```python
# Example of good code style
from typing import Dict, List, Optional
from datetime import datetime

def create_user(email: str, password: str, metadata: Optional[Dict] = None) -> Dict:
    """Create a new user account.
    
    Args:
        email: User's email address
        password: Plain text password (will be hashed)
        metadata: Optional user metadata
        
    Returns:
        Dictionary containing user data and authentication token
        
    Raises:
        ValueError: If email is invalid or password is too weak
    """
    # Implementation here
    pass
```

#### Testing Requirements
- **Unit Tests**: All new functions must have unit tests
- **Integration Tests**: Add integration tests for new endpoints
- **Coverage**: Maintain >80% test coverage
- **Test Naming**: Use descriptive test names

```python
# Example test structure
import pytest
from coglex.services.auth.utils import _signup

class TestUserAuthentication:
    def test_signup_with_valid_data_creates_user(self):
        """Test that signup creates user with valid email and password."""
        # Test implementation
        pass
    
    def test_signup_with_invalid_email_raises_error(self):
        """Test that signup raises ValueError for invalid email."""
        # Test implementation
        pass
```

#### Documentation Standards
- **API Documentation**: Update API docs for new endpoints
- **Code Comments**: Add comments for complex logic
- **README Updates**: Update README for new features
- **Changelog**: Add entries to CHANGELOG.md

#### Commit Message Format
Use conventional commit format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add OAuth2 Google authentication
fix(storage): resolve MongoDB connection timeout issue
docs(api): update payment service documentation
test(auth): add unit tests for JWT token validation
```

### Adding New Services

To add a new microservice to Coglex:

1. **Create Service Structure**
   ```bash
   mkdir coglex/services/yourservice
   touch coglex/services/yourservice/__init__.py
   touch coglex/services/yourservice/routes.py
   touch coglex/services/yourservice/utils.py
   ```

2. **Implement Service Routes**
   ```python
   # coglex/services/yourservice/routes.py
   from flask import Blueprint, request, jsonify
   from coglex.gateway.protection import protected
   from .utils import your_service_function
   
   yourservice_bp = Blueprint('yourservice', __name__)
   
   @yourservice_bp.route('/service/yourservice/v1/endpoint', methods=['POST'])
   @protected()
   def your_endpoint():
       """Your endpoint description."""
       try:
           data = request.get_json()
           result = your_service_function(data)
           return jsonify(result), 200
       except Exception as e:
           return jsonify({"error": str(e)}), 500
   ```

3. **Implement Service Logic**
   ```python
   # coglex/services/yourservice/utils.py
   from typing import Dict, Any
   
   def your_service_function(data: Dict[str, Any]) -> Dict[str, Any]:
       """Your service function description.
       
       Args:
           data: Input data dictionary
           
       Returns:
           Result dictionary
       """
       # Implementation here
       return {"result": "success"}
   ```

4. **Register Blueprint**
   ```python
   # coglex/__init__.py
   from coglex.services.yourservice.routes import yourservice_bp
   
   def create_app():
       app = Flask(__name__)
       # ... existing code ...
       app.register_blueprint(yourservice_bp)
       return app
   ```

5. **Add Tests**
   ```python
   # tests/test_yourservice.py
   import pytest
   from coglex import create_app
   
   @pytest.fixture
   def client():
       app = create_app()
       app.config['TESTING'] = True
       with app.test_client() as client:
           yield client
   
   def test_your_endpoint(client):
       """Test your new endpoint."""
       # Test implementation
       pass
   ```

### Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - Coglex version
   - Dependencies versions

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected behavior
   - Actual behavior

3. **Error Messages**
   - Full error traceback
   - Log files (if applicable)

4. **Minimal Example**
   - Smallest code example that reproduces the issue

### Feature Requests

For new features, please provide:

1. **Use Case**: Describe the problem you're trying to solve
2. **Proposed Solution**: Your suggested implementation
3. **Alternatives**: Other solutions you've considered
4. **Impact**: How this affects existing functionality

### Code Review Process

1. **Automated Checks**: All PRs must pass CI/CD checks
2. **Manual Review**: Core maintainers will review code
3. **Testing**: Ensure all tests pass and coverage is maintained
4. **Documentation**: Verify documentation is updated
5. **Approval**: At least one maintainer approval required

### Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Major contributions highlighted
- **GitHub**: Contributor badges and statistics

Thank you for contributing to Coglex Intelligence! 🚀

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

The MIT License is a permissive free software license that allows you to:

✅ **Use** - Use the software for any purpose  
✅ **Modify** - Change the software to suit your needs  
✅ **Distribute** - Share the software with others  
✅ **Private Use** - Use the software in private projects  
✅ **Commercial Use** - Use the software in commercial applications  

**Requirements:**
- Include the original license and copyright notice in any copy of the software
- Include the license notice in any substantial portions of the software

**Limitations:**
- The software is provided "as is" without warranty
- Authors are not liable for any damages or issues

### Third-Party Licenses

This project uses several third-party libraries, each with their own licenses:

| Library | License | Purpose |
|---------|---------|---------|
| Flask | BSD-3-Clause | Web framework |
| PyMongo | Apache-2.0 | MongoDB driver |
| Stripe | MIT | Payment processing |
| google-genai | Apache-2.0 | AI generation |
| PyJWT | MIT | JWT token handling |
| bcrypt | Apache-2.0 | Password hashing |
| Waitress | ZPL-2.1 | WSGI server |
| Requests | Apache-2.0 | HTTP library |
| python-dotenv | BSD-3-Clause | Environment variables |

### License Compliance

When using Coglex Intelligence in your projects:

1. **Include License Notice**: Keep the LICENSE file in your distribution
2. **Attribution**: Credit the original authors in your documentation
3. **Third-Party Compliance**: Ensure compliance with all dependency licenses
4. **Modifications**: Document any significant changes you make

### Commercial Use

Coglex Intelligence can be used in commercial applications without restrictions. However:

- **Support**: Commercial support is not guaranteed under the MIT license
- **Liability**: Use at your own risk - no warranties provided
- **Attribution**: Consider crediting the project in your application

For commercial support or custom licensing arrangements, please contact the maintainers.

## 🆘 Support

Need help with Coglex Intelligence? We're here to assist you! 

### 📚 Documentation & Resources

- **📖 Full Documentation**: [GitHub Wiki](https://github.com/yourusername/coglex/wiki)
- **🚀 Quick Start Guide**: See [Installation](#-installation) section above
- **💡 Examples & Tutorials**: Check the [examples/](examples/) directory
- **🔧 API Reference**: Complete API documentation in this README
- **📝 Changelog**: See [CHANGELOG.md](CHANGELOG.md) for version history

### 🐛 Issue Reporting

Found a bug or have a feature request? Please help us improve!

#### Bug Reports
1. **Search Existing Issues**: Check if the issue already exists
2. **Use Bug Template**: Follow our issue template for consistency
3. **Provide Details**: Include environment info, steps to reproduce, and error messages
4. **Minimal Example**: Provide the smallest code example that reproduces the issue

**Create Bug Report**: [GitHub Issues](https://github.com/yourusername/coglex/issues/new?template=bug_report.md)

#### Feature Requests
1. **Check Roadmap**: See if the feature is already planned
2. **Use Feature Template**: Follow our feature request template
3. **Explain Use Case**: Describe the problem you're trying to solve
4. **Consider Alternatives**: Mention other solutions you've considered

**Request Feature**: [GitHub Issues](https://github.com/yourusername/coglex/issues/new?template=feature_request.md)

### 💬 Community Support

#### GitHub Discussions
- **💭 General Questions**: Ask questions about usage and implementation
- **💡 Ideas & Suggestions**: Share ideas for improvements
- **🎯 Show & Tell**: Share your projects built with Coglex
- **🤝 Help Others**: Answer questions from other users

**Join Discussion**: [GitHub Discussions](https://github.com/yourusername/coglex/discussions)

#### Stack Overflow
- **Tag**: Use `coglex-intelligence` tag for questions
- **Search First**: Check existing questions before posting
- **Be Specific**: Include code examples and error messages

### 📧 Direct Contact

For sensitive issues, security concerns, or business inquiries:

- **Website**: [https://imadelakhaldev.com/](https://imadelakhaldev.com/)
- **Email**: imadelakhaldev@gmail.com
- **Issues**: Create an issue on GitHub
- **Security Issues**: imadelakhaldev@gmail.com (mark as SECURITY)

### 🔒 Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. **Email**: imadelakhaldev@gmail.com with "SECURITY" in subject
3. **Include**: Steps to reproduce and potential impact
4. **Response**: We'll respond within 48 hours

### 📞 Commercial Support

Need professional support for your production deployment?

#### Support Tiers

**🥉 Community Support** (Free)
- GitHub Issues & Discussions
- Community-driven help
- Best effort response time

**🥈 Priority Support** (Contact for pricing)
- Email support with 24-hour response
- Priority issue resolution
- Installation and configuration help
- Basic deployment assistance

**🥇 Enterprise Support** (Custom pricing)
- Dedicated support engineer
- Phone/video call support
- Custom feature development
- SLA guarantees (99.9% uptime)
- On-site training and consultation

**Contact**: imadelakhaldev@gmail.com for commercial support options

### 🌍 Community Guidelines

When seeking support, please:

- **Be Respectful**: Treat all community members with respect
- **Be Patient**: Maintainers and community members volunteer their time
- **Be Helpful**: Help others when you can
- **Search First**: Check existing resources before asking
- **Provide Context**: Include relevant details in your questions

### 📈 Response Times

| Support Channel | Expected Response Time |
|----------------|----------------------|
| GitHub Issues | 2-5 business days |
| GitHub Discussions | 1-3 business days |
| Security Email | Within 48 hours |
| Commercial Support | Per agreement |

### 🛠️ Self-Help Resources

Before reaching out, try these resources:

1. **Check Logs**: Review application and server logs for error details
2. **Environment**: Verify all environment variables are set correctly
3. **Dependencies**: Ensure all dependencies are installed and up-to-date
4. **Configuration**: Double-check your `config.py` and `.env` settings
5. **Documentation**: Review the relevant API documentation section

### 🎯 Getting Better Help

To get faster, more accurate help:

- **Minimal Example**: Provide the smallest code that reproduces the issue
- **Environment Details**: Include Python version, OS, and dependency versions
- **Error Messages**: Include full error tracebacks and log messages
- **Expected vs Actual**: Clearly describe what you expected vs what happened
- **Steps Taken**: List troubleshooting steps you've already tried

Thank you for using Coglex Intelligence! 🚀

## 📈 Version History

### 🚀 Release Timeline

#### v1.0.0 - Genesis (Initial Release)
**Release Date**: TBD  
**Focus**: Core Foundation & Microservices Architecture

**🎯 Core Features:**
- **Authentication Service**: Complete user management system
  - User registration and login
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Session management
- **Storage Service**: MongoDB integration
  - CRUD operations (Create, Read, Update, Delete)
  - Aggregation pipeline support
  - Document validation
- **Archive Service**: File management system
  - File upload and download
  - Multiple file format support
  - Secure file storage
- **Payment Service**: Stripe integration
  - Payment processing
  - Subscription management
  - Webhook handling

**🔧 Technical Improvements:**
- Flask microservices architecture
- RESTful API design
- Environment-based configuration
- Error handling and logging
- Input validation and sanitization

#### v1.1.0 - AI Generation Integration
**Release Date**: TBD  
**Focus**: Google Gemini AI Integration

**🤖 AI Features:**
- **Generation Service**: Google Gemini integration
  - File upload for AI processing
  - Multi-modal content support (text, images, audio, video)
  - Conversational AI capabilities
  - System instructions and tools
  - Safety settings and content filtering
- **Token Management**: AI content tokenization
  - Token counting for cost estimation
  - Content optimization

**📁 File Support:**
- Images: PNG, JPEG, WebP, HEIC, HEIF
- Documents: PDF, TXT, HTML, CSS, JavaScript, Python
- Audio: WAV, MP3, AIFF, AAC, OGG, FLAC
- Video: MP4, MPEG, MOV, AVI, FLV, MPG, WebM, WMV, 3GPP

#### v1.2.0 - Security & Production Readiness
**Release Date**: TBD  
**Focus**: Enhanced Security & Deployment

**🔒 Security Enhancements:**
- Multi-layer API protection
- OAuth integration (Google, Facebook)
- OTP verification system
- CORS configuration
- Input validation improvements
- File type detection and validation
- Rate limiting and throttling

**🚀 Production Features:**
- Waitress WSGI server integration
- Production/development environment separation
- Enhanced logging and monitoring
- Error tracking and reporting
- Performance optimizations

#### v1.3.0 - Developer Experience (Planned)
**Release Date**: TBD  
**Focus**: Developer Tools & Documentation

**🛠️ Developer Tools:**
- Comprehensive API documentation
- Interactive API explorer
- SDK for popular languages
- CLI tools for management
- Development utilities

**📚 Documentation:**
- Complete API reference
- Tutorial series
- Best practices guide
- Deployment guides
- Troubleshooting documentation

#### v1.4.0 - Advanced Features (Planned)
**Release Date**: TBD  
**Focus**: Advanced Functionality

**⚡ Advanced Features:**
- Real-time notifications
- WebSocket support
- Advanced caching strategies
- Database optimization
- Microservices orchestration

**🔄 Integrations:**
- Additional payment providers
- More AI model providers
- Third-party service integrations
- Webhook management system

#### v2.0.0 - Platform Evolution (Future)
**Release Date**: TBD  
**Focus**: Platform Transformation

**🌟 Major Features:**
- GraphQL API support
- Advanced analytics and reporting
- Multi-tenant architecture
- Plugin system
- Advanced AI capabilities

### 🏷️ Version Naming Convention

Coglex Intelligence follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes that require code updates
- **MINOR**: New features that are backward compatible
- **PATCH**: Bug fixes and small improvements

### 📊 Feature Evolution

| Feature | v1.0 | v1.1 | v1.2 | v1.3 | v1.4 | v2.0 |
|---------|------|------|------|------|------|------|
| Authentication | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Storage | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Archive | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Payments | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI Generation | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| OAuth | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| OTP | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Production Ready | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Developer Tools | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Real-time | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| GraphQL | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### 🔄 Migration Guides

#### Upgrading from v1.0 to v1.1
- No breaking changes
- Add `GENERATION_KEY` to environment variables
- Update dependencies: `pip install -r requirements.txt`

#### Upgrading from v1.1 to v1.2
- Add OAuth environment variables
- Update security configurations
- Review CORS settings

### 📝 Changelog

For detailed changes in each version, see [CHANGELOG.md](CHANGELOG.md).

### 🎯 Roadmap

Our development roadmap focuses on:

1. **Stability**: Ensuring robust, production-ready code
2. **Security**: Implementing best-in-class security practices
3. **Performance**: Optimizing for speed and scalability
4. **Developer Experience**: Making integration as smooth as possible
5. **Innovation**: Adding cutting-edge features and capabilities

### 📢 Release Notifications

Stay updated on new releases:

- **GitHub**: Watch the repository for release notifications
- **Email**: Subscribe to our mailing list
- **RSS**: Follow our release feed
- **Social**: Follow us on social media for announcements

---

*Current Version: v1.2.0 (Security & Production Ready)*

---

**Built with ❤️ by IMAD EL AKHAL**

*Coglex Intelligence — secure web development with modular microservices and AI.*
