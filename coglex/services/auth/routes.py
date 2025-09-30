"""
this module implements rest api endpoints for user authentication and account management
it provides the following core functionality:

- user registration (signup)
- user authentication (signin) 
- session management and tracking
- user logout (signout)
- user profile updates

the routes in this module handle http requests for these operations and integrate
with the underlying authentication services
"""


# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config

# importing blueprint utilities used in current routing context
from coglex import authenticated, protected
from coglex.services.auth.utils import _signup, _signin, _retrieve, _refresh, _session, _signout


# blueprint instance
_auth = Blueprint("_auth", config.APP_IMPORT)


@_auth.route("/service/auth/v1/signup/", methods=["POST"])
@_auth.route("/service/auth/v1/signup", methods=["POST"])
@protected()
def signup():
    """
    handle user signup requests for a specified collection

    expects json payload with:
    - _key: unique identifier for the user
    - _password: user password
    - document: optional additional user data
    """
    # get document from request body
    _key, _password = request.json.get("_key"), request.json.get("_password")

    # checking required parameters
    if not _key or not _password:
        return abort(400)

    try:
        # signing up user
        req = _signup(_key, _password, request.json.get("document"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if user exists, return error indicating user already exists
    if not req:
        return abort(400)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/signin/", methods=["POST"])
@_auth.route("/service/auth/v1/signin", methods=["POST"])
@protected()
def signin():
    """
    authenticate a user against the auth collection.
    
    expects json payload with:
    - _key: unique identifier for the user
    - _password: user password
    - query: optional additional filter criteria
    
    returns user data and session token on success.
    """
    # get document from request body
    _key, _password = request.json.get("_key"), request.json.get("_password")

    # checking required parameters
    if not _key or not _password:
        return abort(400)

    try:
        # signing up user
        req = _signin(_key, _password, request.json.get("query"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/retrieve/", methods=["GET"])
@_auth.route("/service/auth/v1/retrieve", methods=["GET"])
@protected()
@authenticated()
def retrieve(_key: str):
    """
    retrieve user profile data for the authenticated user

    returns the stored profile information for the user identified by the
    provided key, requires an active session and valid authentication
    """
    try:
        # retrieving user data
        req = _retrieve()
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no user found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/refresh/", methods=["PATCH"])
@_auth.route("/service/auth/v1/refresh", methods=["PATCH"])
@protected()
@authenticated()
def refresh(_key: str):
    """
    refresh or update an existing user's profile data

    expects json payload with:
    - document: updated user data to merge into the profile

    returns the updated user document on success.
    """
    # get document from request body
    document = request.json.get("document")

    # checking required parameters
    if not document:
        return abort(400)

    try:
        # refreshing user data
        req = _refresh(document)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no user found to update, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/session/", methods=["GET"])
@_auth.route("/service/auth/v1/session", methods=["GET"])
@protected()
def session():
    """
    retrieve the current user session data

    returns the user session data if available, otherwise returns (None, None)
    """
    try:
        return jsonify(_session()), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))


@_auth.route("/service/auth/v1/signout/", methods=["GET"])
@_auth.route("/service/auth/v1/signout", methods=["GET"])
@protected()
def signout():
    """
    handle user signout / session termination requests for a specified collection
    """
    try:
        return jsonify(_signout()), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))
