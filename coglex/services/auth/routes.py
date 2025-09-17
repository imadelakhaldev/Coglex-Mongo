"""
authentication service routes module
the routes handle user registration, authentication, session tracking and logout functionality

this module provides routing rules and endpoints for authentication operations including:
- user signup
- user signin/authentication
- session management
- user signout
- user update
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


@_auth.route("/service/auth/v1/signup/<collection>/", methods=["POST"])
@_auth.route("/service/auth/v1/signup/<collection>", methods=["POST"])
@protected()
def signup(collection: str):
    """
    handle user signup requests for a specified collection
    
    args:
        collection (str): actual name of the collection to register the user in
    """
    try:
        # signing up user
        req = _signup(collection, request.json.get("_key"), request.json.get("_password"), request.json.get("document"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if user exists, return error indicating user already exists
    if not req:
        return abort(400)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/signin/<collection>/", methods=["POST"])
@_auth.route("/service/auth/v1/signin/<collection>", methods=["POST"])
@protected()
def signin(collection: str):
    """
    handle user signin/authentication requests for a specified collection
    
    args:
        collection (str): actual name of the collection to authenticate the user against
    """
    try:
        # signing up user
        req = _signin(collection, request.json.get("_key"), request.json.get("_password"), request.json.get("query"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/session/<collection>/", methods=["GET"])
@_auth.route("/service/auth/v1/session/<collection>", methods=["GET"])
@protected()
def _session(collection: str):
    """
    retrieve the current session data for a specified collection
    
    args:
        collection (str): actual name of the collection to get session data from
    """
    try:
        return jsonify(session.get(collection)), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))


@_auth.route("/service/auth/v1/signout/<collection>/", methods=["GET"])
@_auth.route("/service/auth/v1/signout/<collection>", methods=["GET"])
def signout(collection: str):
    """
    handle user signout / session termination requests for a specified collection
    
    args:
        collection (str): actual name of the collection to remove session data from
    """
    try:
        return jsonify(_signout(collection)), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))


@_auth.route("/service/auth/v1/refresh/<collection>/", methods=["PATCH"])
@_auth.route("/service/auth/v1/refresh/<collection>", methods=["PATCH"])
@protected()
def refresh(collection: str):
    """
    handle user data refresh/update requests for a specified collection
    
    args:
        collection (str): actual name of the collection to update user data in
    """
    try:
        # refreshing user data
        req = _refresh(collection, request.json.get("_key"), request.json.get("document"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no user found to update, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200
