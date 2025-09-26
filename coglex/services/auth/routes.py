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
from flask import Blueprint, request, session, jsonify, abort

# importing base config parameters, and generic utilities
import config

# importing blueprint utilities used in current routing context
from coglex import protected
from coglex.services.auth.utils import _signup, _signin, _signout, _refresh


# blueprint instance
_auth = Blueprint("_auth", config.APP_IMPORT)


@_auth.route("/service/auth/v1/signup/", methods=["POST"])
@_auth.route("/service/auth/v1/signup", methods=["POST"])
@protected()
def signup():
    """
    handle user signup requests for a specified collection
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
    handle user signin/authentication requests for a specified collection
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


@_auth.route("/service/auth/v1/session/", methods=["GET"])
@_auth.route("/service/auth/v1/session", methods=["GET"])
@protected()
def _session():
    """
    retrieve the current session data for a specified collection
    """
    try:
        return jsonify(session.get(config.MONGODB_AUTH_COLLECTION)), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))


@_auth.route("/service/auth/v1/refresh/", methods=["PATCH"])
@_auth.route("/service/auth/v1/refresh", methods=["PATCH"])
@protected()
def refresh():
    """
    handle user data refresh/update requests for a specified collection
    """
    # get document from request body
    _key, document = request.json.get("_key"), request.json.get("document")

    # checking required parameters
    if not _key or not document:
        return abort(400)

    try:
        # refreshing user data
        req = _refresh(_key, document)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no user found to update, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/signout/", methods=["GET"])
@_auth.route("/service/auth/v1/signout", methods=["GET"])
def signout():
    """
    handle user signout / session termination requests for a specified collection
    """
    try:
        return jsonify(_signout()), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))
