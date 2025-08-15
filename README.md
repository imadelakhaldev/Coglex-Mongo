# Coglex Intelligence

**Version:** Genesis
**Company:** IMAD EL AKHAL
**Website:** [https://ielakhal.com/](https://ielakhal.com/)


## Overview

Coglex Intelligence is a backend service built with Flask. It provides API endpoints for user authentication and data storage, utilizing MongoDB as its database. The application is designed to be modular, with services for authentication and storage clearly separated.


## Project Structure
├── .pylintrc             # Pylint configuration file
├── .venv/                # Python virtual environment
├── coglex/               # Main application package
│   ├── init .py       # Initializes Flask app, DB, blueprints, decorators
│   ├── gateway/          # Entry point for developers to build new routes and applications
│   ├── services/         # Core service modules
│   │   ├── init .py
│   │   ├── auth/         # Authentication service
│   │   │   ├── init .py
│   │   │   ├── routes.py # API routes for signup, signin, session, signout
│   │   │   └── utils.py  # Helper functions for authentication logic
│   │   ├── archive/      # Archive (file storage) service
│   │   │   ├── init .py
│   │   │   ├── routes.py # API routes for file upload, download, delete
│   │   │   └── utils.py  # Helper functions for file operations
│   │   ├── execution/    # Function execution service
│   │   │   ├── init .py
│   │   │   ├── routes.py # API routes for dynamic function execution
│   │   │   └── utils.py  # Helper functions for function execution
│   │   ├── payment/      # Payment processing service (Stripe integration)
│   │   │   ├── init .py
│   │   │   ├── routes.py # API routes for checkout, subscription, and webhooks
│   │   │   └── utils.py  # Helper functions for Stripe API interactions
│   │   └── storage/      # Storage (database) service
│   │       ├── init .py
│   │       │   ├── routes.py # API routes for CRUD operations on MongoDB
│   │       └── utils.py  # Helper functions for MongoDB interactions
│   ├── static/           # Static files (CSS, JS, images)
│   │   └── uploads/      # Directory for file uploads
│   └── templates/        # HTML templates (if any frontend part exists)
├── config.py             # Global application configuration
├── run.py                # Entry point to run the application
└── utils.py              # General utility functions


## Core Components

*   **Flask Application (`coglex/__init__.py`)**: Initializes the Flask app, connects to MongoDB, and registers service blueprints. It also defines crucial decorators for API protection:
    *   `@protected`: Ensures the presence and validity of an `X-API-Key` header, matching `SERVER_SECRET` from `config.py`.
    *   `@authenticated`: Validates a JWT (JSON Web Token) provided in the `Authorization: Bearer <token>` header, ensuring the user is logged in and authorized.
*   **Configuration (`config.py`)**: Manages all settings, including server parameters, database connection strings, application metadata, and secrets.
*   **Entry Point (`run.py`)**: Starts the development or production server (Waitress).
*   **Utilities (`utils.py`)**: Provides common helper functions for tasks like JWT encoding/decoding, hex string generation, and colored console output.


## Services

### Authentication Service (`coglex/services/auth/`)

Manages user authentication, including registration, login, session handling, and logout. It integrates with MongoDB for user data storage.

*   **Endpoints**:
    *   `POST /service/auth/v1/signup/<collection>/`: Registers a new user into the specified MongoDB collection.
    *   `POST /service/auth/v1/signin/<collection>/`: Authenticates a user and issues a JWT for subsequent authenticated requests.
    *   `GET /service/auth/v1/session/<collection>/`: Retrieves current session data for an authenticated user.
    *   `GET /service/auth/v1/signout/<collection>/`: Invalidates the user's session and logs them out.
*   **Mechanism**: Leverages JWT (JSON Web Tokens) for secure, stateless authentication. The `@authenticated` decorator ensures that only requests with a valid JWT can access protected resources.


### Archive Service (`coglex/services/archive/`)

Provides robust file management capabilities, including secure upload, download, and deletion of files. It uses MongoDB to store file metadata and the local file system for the actual file content.

*   **Endpoints**:
    *   `POST /service/archive/v1/upload/<collection>/`: Uploads a file to a specified collection, storing its metadata in MongoDB.
    *   `GET /service/archive/v1/download/<collection>/<reference>/`: Retrieves a file by its unique reference from a given collection.
    *   `DELETE /service/archive/v1/delete/<collection>/<reference>/`: Deletes a file and its associated metadata.
*   **Mechanism**: Files are stored on the server's file system, while their corresponding metadata (e.g., filename, size, path) is managed within MongoDB, ensuring data integrity and efficient retrieval.

### Execution Service (`coglex/services/execution/`)

Enables dynamic remote execution of Python functions. This service is designed for extensibility, allowing new functionalities to be exposed via API calls without direct code deployment.

*   **Endpoints**:
    *   `POST /service/execution/v1/execute/<function_name>/`: Executes a pre-defined Python function by its name, accepting parameters via the request body.
*   **Mechanism**: Functions are defined in `coglex/services/execution/utils.py` and are dynamically loaded and executed based on the `function_name` provided in the API request. This allows for a flexible and powerful way to extend backend logic.

### Storage Service (`coglex/services/storage/`)

Facilitates comprehensive CRUD (Create, Read, Update, Delete) operations directly with MongoDB collections. It provides a standardized interface for interacting with your database.

*   **Endpoints**:
    *   `GET /service/storage/v1/<collection>/`: Retrieves multiple documents from a specified collection, with optional query parameters for filtering.
    *   `GET /service/storage/v1/<collection>/<key>/`: Fetches a single document by its unique identifier (`key`) from a given collection.
    *   `POST /service/storage/v1/<collection>/`: Inserts a new document into the specified collection. A unique hexadecimal ID is automatically generated.
    *   `PATCH /service/storage/v1/<collection>/<key>/`: Updates an existing document identified by its `key` in the specified collection.
    *   `DELETE /service/storage/v1/<collection>/<key>/`: Removes a document by its `key` from the designated collection.
*   **Mechanism**: Directly interfaces with MongoDB using PyMongo, abstracting database interactions behind RESTful API endpoints. It ensures data consistency and efficient management of document-based data.


## Setup and Running

1.  **Prerequisites**:
    *   Python 3.x
    *   MongoDB instance accessible
2.  **Installation**:
    *   Clone the repository.
    *   Create and activate a Python virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    *   Install dependencies (assuming a `requirements.txt` file, which is not explicitly listed but typical for Python projects):
        ```bash
        pip install Flask PyMongo PyJWT colorama waitress
        ```
3.  **Configuration**:
    *   Update `config.py` with your specific settings, especially:
        *   `SERVER_SECRET`
        *   `SMTP_PASSWORD` (if email functionality is used)
        *   `MONGODB_URI`
4.  **Running the Application**:
    *   For development:
        ```bash
        python run.py
        ```
        The server will typically run on `http://0.0.0.0:80` (or as configured in `config.py`). `SERVER_DEBUG` in `config.py` should be `True`.
    *   For production (using Waitress):
        Set `SERVER_DEBUG` to `False` in `config.py` and run:
        ```bash
        python run.py
        ```

## API Testing with Postman/Insomnia

A Postman collection named `postman.json` has been created to facilitate testing of all implemented API endpoints. This file can be imported directly into Postman or Insomnia.

### Included Requests:

*   **Auth Service**:
    *   Signup
    *   Signin
    *   Session Retrieval
    *   Signout
*   **Storage Service**:
    *   Get Multiple Documents
    *   Get Single Document
    *   Insert Document
    *   Update Document
    *   Delete Document
*   **Archive Service**:
    *   Upload File
    *   Download File
    *   Delete File
*   **Execution Service**:
    *   Execute Function (e.g., `example_function`)
*   **Payment Service**:
    *   Checkout (One-time Payment)
    *   Create Subscription
    *   Stripe Webhook

### Payment Service (`coglex/services/payment/`)

Integrates Stripe for handling one-time payments, subscriptions, and webhook events. This service enables secure and efficient processing of financial transactions.

*   **Endpoints**:
    *   `POST /service/payment/v1/checkout/`: Initiates a one-time payment process via Stripe Checkout.
    *   `POST /service/payment/v1/subscription/`: Creates a new subscription for a user through Stripe.
    *   `POST /service/payment/v1/webhook/`: Receives and processes events from Stripe webhooks, such as successful payments or subscription changes.
*   **Mechanism**: Utilizes the Stripe API for payment processing. The `checkout` and `subscription` endpoints interact with Stripe to create payment intents and manage subscriptions, while the `webhook` endpoint securely handles asynchronous notifications from Stripe.

## API Protection

Coglex Intelligence employs a multi-layered security approach to protect its API endpoints:

*   **API Key Protection (`@protected` decorator)**: Most service API endpoints are secured using a mandatory `X-API-Key` header. Requests must include this header with a value that matches the `SERVER_SECRET` configured in `config.py`. This provides a first line of defense against unauthorized access.
*   **JWT Authentication (`@authenticated` decorator)**: Routes that require user-specific authorization are further protected by JWT. After a successful sign-in via the Authentication Service, a `Bearer` token is issued. This token must be included in the `Authorization` header for all subsequent requests to authenticated endpoints, ensuring that only legitimate and logged-in users can access their resources.

## Gateway

The `gateway` concept in Coglex Intelligence is designed as an extensible entry point for developers to build new routes and applications that leverage the core functionalities of the framework and its services. It acts as a central hub where custom logic and new API endpoints can be integrated seamlessly, utilizing the existing authentication, storage, archive, execution, and payment services. This modular approach promotes rapid development and allows for the creation of diverse applications on top of the Coglex platform.


## Extending Functionality with Signals

Coglex Intelligence utilizes Flask signals to allow developers to easily extend and customize its behavior without modifying core service logic. This is particularly useful for reacting to events like Stripe webhooks.

### Intercepting Stripe Webhooks

The `payment` service dispatches a `stripe_webhook_received` signal whenever a Stripe webhook event is successfully processed. Developers can connect to this signal to implement custom logic, such as updating order statuses, sending confirmation emails, or triggering other business processes.

**Example Usage:**

To intercept the `stripe_webhook_received` signal, you can add code similar to the following in your application (e.g., in a custom module or a `gateway` route):

```python
from coglex.utils import stripe_webhook_received

@stripe_webhook_received.connect
def handle_successful_payment(sender, **kwargs):
    payload = sender # the payload object is passed as the sender
    # process the payload data here
    # e.g., update order status in database, send confirmation email, etc.
```

In this example:
*   `stripe_webhook_received.connect` registers `handle_successful_payment` as a listener for the signal.
*   The `sender` argument will be the `payload` object (or relevant Stripe event data) that triggered the signal.
*   You can then process this data as needed for your application's specific requirements.

## Key Technologies

*   **Flask**: Micro web framework for Python.
*   **MongoDB**: NoSQL document database.
*   **PyMongo**: Python driver for MongoDB.
*   **JWT (PyJWT)**: For generating and verifying JSON Web Tokens for authentication.
*   **Waitress**: Production-quality WSGI server.
*   **Colorama**: For producing colored terminal output.
