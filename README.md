# Coglex Intelligence

<div align="center">

🧠 A powerful Flask-based backend framework for secure API development

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/mongodb-latest-success.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 📖 Overview

Coglex Intelligence is a modular Flask-based backend framework designed to provide secure and scalable API endpoints. The framework follows a service-oriented architecture with clearly separated modules for authentication, storage, file management, function execution, and payment processing.

## 🌟 Core Features

- 🔐 **Multi-layered Security** - API key protection and JWT-based authentication
- 📦 **MongoDB Integration** - Comprehensive CRUD operations with flexible query support
- 🔄 **Dynamic Collection Handling** - Collection-based data management for flexible schema design
- 📁 **File Management** - Secure file upload, download, and deletion with metadata tracking
- 💳 **Payment Processing** - Stripe integration for handling payments and subscriptions
- 🧩 **Extensible Architecture** - Gateway system for building custom applications on top of core services

## 🏗️ Project Structure

```
coglex/
├── __init__.py        # Flask app initialization, DB connection, security decorators
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

## 🔒 Security Implementation

Coglex implements a robust multi-layered security approach:

### API Key Protection (`@protected` decorator)

```python
def protected(secret: str = config.SERVER_SECRET):
    """Decorator that protects routes by requiring a valid server key in request headers"""
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Check if key exists in request headers and is valid
            if request.headers.get("X-API-Key") == secret:
                return function(*args, **kwargs)
            # If key is missing or invalid, return 401
            return abort(401)
        return wrapper
    return decorator
```

- Requires `X-API-Key` header in requests
- Validates against `SERVER_SECRET` in configuration
- Provides first-level security for all service endpoints

### JWT Authentication (`@authenticated` decorator)

```python
def authenticated(collection: str = config.MONGODB_AUTH_COLLECTION):
    """Decorator that protects routes by requiring valid authentication"""
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Check if required session data exists
            if not session.get(collection):
                return abort(401)
                
            # Authenticate user
            authentication = _signin(collection, 
                                    session.get(collection, {}).get("_key"), 
                                    session.get(collection, {}).get("_password"))
                                    
            # If authentication fails, return 401
            if not authentication:
                return abort(401)
                
            return function(*args, **kwargs)
        return wrapper
    return decorator
```

- Validates user session data stored in Flask session
- Re-authenticates user credentials on each request
- Ensures secure access to user-specific resources

## 🛠️ Authentication Service

The authentication service provides comprehensive user management functionality:

### Core Functions

#### User Registration (`_signup`)

```python
def _signup(collection: str, _key: str, _password: str, document: dict = {}) -> str | None:
    """Creates a new user document in the specified collection"""
    # Check if user already exists
    if _find(collection, {"_key": _key}):
        return None
        
    # Hash password and create user
    _password = phash(_password)
    return _insert(collection, [{"_key": _key, "_password": _password, **document}])
```

#### User Authentication (`_signin`)

```python
def _signin(collection: str, _key: str, _password: str, query: dict = {}) -> dict or None:
    """Authenticates a user by validating their credentials"""
    # Find user
    authentication = _find(collection, {"_key": _key, **query})
    if not authentication:
        return None
        
    # Verify password
    if not pcheck(_password, authentication.get("_password")):
        return None
        
    # Update session
    authentication["_password"] = _password
    session.update({collection: authentication})
    
    return authentication
```

#### User Update (`_refresh`)

```python
def _refresh(collection: str, _key: str, document: dict) -> int | None:
    """Updates user information in the specified collection"""
    # Verify user exists
    if not _find(collection, {"_key": _key}):
        return None
        
    # Handle password updates
    if "_password" in document:
        document["_password"] = phash(document.get("_password"))
        
    # Update user document
    return _patch(collection, document, {"_key": _key})
```

### API Endpoints

```
POST /service/auth/v1/signup/<collection>/   # Register new user
POST /service/auth/v1/signin/<collection>/   # User login
GET  /service/auth/v1/session/<collection>/  # Validate session
GET  /service/auth/v1/signout/<collection>/  # User logout
PATCH /service/auth/v1/refresh/<collection>/ # Update user data
```

## 📦 Storage Service

The storage service provides flexible CRUD operations for MongoDB collections:

### Core Functions

#### Find Documents (`_find`)

```python
def _find(collection: str, query: dict = {}, keys: dict = {}) -> dict or list[dict] or None:
    """Find records in a MongoDB collection that match a specific query"""
    retrievals = list(storage.get_collection(collection).find(query, keys))
    
    if retrievals:
        # Return single result or list based on result count
        return retrievals[0] if len(retrievals) == 1 else retrievals
    
    return None
```

#### Insert Documents (`_insert`)

```python
def _insert(collection: str, documents: list[dict]) -> list[str]:
    """Insert multiple records into a specified MongoDB collection"""
    # Generate unique IDs and insert documents
    execution = storage.get_collection(collection).insert_many(
        [{**document, **{"_id": hexgen()}} for document in documents]
    )
    
    # Convert ObjectIds to strings
    references = [str(_id) for _id in execution.inserted_ids]
    
    return references[0] if len(references) == 1 else references
```

#### Update Documents (`_patch`)

```python
def _patch(collection: str, document: dict, query: dict = {}) -> int or None:
    """Update records in a MongoDB collection that matches a specific query"""
    execution = storage.get_collection(collection).update_many(query, {"$set": document})
    
    if execution.matched_count > 0:
        return execution.modified_count
    
    return None
```

#### Delete Documents (`_delete`)

```python
def _delete(collection: str, query: dict = {}) -> int or None:
    """Delete records from a MongoDB collection that matches a specific query"""
    execution = storage.get_collection(collection).delete_many(query)
    
    if execution.deleted_count > 0:
        return execution.deleted_count
    
    return None
```

### API Endpoints

```
GET    /service/storage/v1/<collection>/       # List documents with query filtering
GET    /service/storage/v1/<collection>/<key>/  # Get single document by ID
POST   /service/storage/v1/<collection>/       # Create document(s)
PATCH  /service/storage/v1/<collection>/<key>/  # Update document by ID
PATCH  /service/storage/v1/<collection>/       # Update multiple documents by query
DELETE /service/storage/v1/<collection>/<key>/  # Delete document by ID
DELETE /service/storage/v1/<collection>/       # Delete multiple documents by query
```

## 🚀 Getting Started

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
# Edit .env with your configuration
```

5. Run the application
```bash
python run.py
```

## 🧩 Extending the Framework

### Gateway System

The `gateway` directory serves as an entry point for building custom applications on top of Coglex's core services. Developers can create new routes and applications that leverage the existing authentication, storage, and other services.

### Example: Creating a Custom API

```python
# In coglex/gateway/myapi/routes.py
from flask import Blueprint, jsonify
import config
from coglex import protected, authenticated
from coglex.services.storage.utils import _find

# Create blueprint
myapi = Blueprint("myapi", config.APP_IMPORT)

@myapi.route("/api/myapi/v1/data/", methods=["GET"])
@protected()  # API key protection
@authenticated("users")  # User authentication
def get_data():
    # Use core services
    data = _find("my_collection", {"type": "important"})
    return jsonify(data), 200

# Register in coglex/__init__.py
# from coglex.gateway.myapi.routes import myapi
# application.register_blueprint(myapi)
```

## 👥 Authors

- **IMAD EL AKHAL** - *Initial work* - [Website](https://ielakhal.com/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
