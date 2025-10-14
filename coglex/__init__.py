"""
this module handles the core initialization of the coglex framework, including:
- flask application setup and configuration
- database connection and initialization
- authentication decorators setup
- service module registration
"""


# standard imports
import os

# python's built-in function wrappers
from functools import wraps

# pip install flask
# micro server routing, services, templating, and http serving toolkit
from flask import Flask, request, session, g, abort

# pip install pymongo
# initialize mongodb client
from pymongo import MongoClient

# pip install stripe
# online payment processing provider
import stripe

# importing generic utilities
from utils import jwtdec

# importing base config parameters, and generic utilities
import config


# server application / coglex container
application = Flask(config.APP_IMPORT, template_folder=config.APP_TEMPLATES, static_folder=config.APP_STATIC)

# application's extra config
application.config.from_mapping({
    "SECRET_KEY": config.SERVER_SECRET,
    "PERMANENT_SESSION_LIFETIME": config.SERVER_SESSION_LIFETIME,
    "UPLOAD_FOLDER": config.APP_UPLOAD,
    "MAX_CONTENT_LENGTH": config.MAX_CONTENT_LENGTH,
    "SEND_FILE_MAX_AGE_DEFAULT": config.SEND_FILE_MAX_AGE,
})

# check and create upload folder if it doesn't exist
if not os.path.exists(config.APP_UPLOAD):
    os.makedirs(config.APP_UPLOAD)

# connect to mongodb with credentials
storage = MongoClient(config.MONGODB_URI).get_database(config.MONGODB_DATABASE)

# setting up stripe payment api key
stripe.api_key = config.STRIPE_SECRET_KEY


# server key requirement decorator for routes
def protected(secret: str = config.SERVER_SECRET):
    """
    decorator that protects routes by requiring a valid server key in request headers
    
    args:
        secret (str): the expected secret key to validate against
        
    returns:
        decorator: a wrapped function that checks for valid server key before executing the handler
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # check if key exists in request headers and is valid
            if request.headers.get("X-API-Key") == secret:
                return function(*args, **kwargs)

            # if key is missing or invalid, return 401
            return abort(401)

        # return wrapper
        return wrapper

    # return decorator
    return decorator


# user auth requirement decorator for routes
def authenticated(collection: str = config.MONGODB_AUTH_COLLECTION):
    """
    decorator that protects routes by requiring valid authentication
    requires user to be logged in with valid session data and credentials
    validates user authentication state before allowing access to protected routes

    args:
        collection (str): the session key to validate user authentication against

    returns:
        decorator: a wrapped function that validates user authentication
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # get token from request headers
            token = request.headers.get("Authorization", "").replace("Bearer ", "")

            # if token is missing from headers, try session
            if not token:
                token = session.get(collection)

            # if token is missing from headers and session, return 401
            if not token:
                return abort(401)

            # decode given token and
            content = jwtdec(token)

            # if content is empty or invalid, return 401
            if not content:
                return abort(401)

            # extract user key from content
            _key = content.pop("_key")

            # if user key is missing from content, return 401
            if not _key:
                return abort(401)

            # importing generic utilities
            from coglex.services.auth.utils import _retrieve

            # authenticate / verify user using key and the rest of the content params
            authentication = _retrieve(_key, content, collection)

            # if user doesn't exist or is inactive to the given query, return 401
            if not authentication:
                return abort(401)

            # store user authentication data in global context for route scope use
            g.authentication = authentication

            # if we get here, token is valid and user verified
            return function(*args, **kwargs)

        # return wrapper
        return wrapper

    # return decorator
    return decorator


# importing service modules
from coglex.services.auth.routes import _auth
from coglex.services.storage.routes import _storage
from coglex.services.archive.routes import _archive
from coglex.services.payment.routes import _payment
from coglex.services.generation.routes import _generation

# importing gateway modules
# from coglex.gateway.module.routes import module

# register service blueprints with application
application.register_blueprint(_auth)
application.register_blueprint(_storage)
application.register_blueprint(_archive)
application.register_blueprint(_payment)
application.register_blueprint(_generation)

# register gateway blueprints with application
# application.register_blueprint(module)
