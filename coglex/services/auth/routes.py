"""
authentication service routes module
the routes handle user registration, authentication, session tracking and logout functionality

this module provides routing rules and endpoints for authentication operations including:
- user signup
- user signin/authentication
- session management
- user signout
"""


# importing flask's built-in modules
from flask import Blueprint, request, session, jsonify, abort

# importing base config parameters, and generic utilities
import config

# importing blueprint utilities used in current routing context
from coglex import protected
from coglex.services.auth.utils import signup, signin


# blueprint instance
auth = Blueprint("auth", config.APP_IMPORT)


# user creation route
@auth.route("/service/auth/v1/signup/<collection>/", methods=["POST"])
@auth.route("/service/auth/v1/signup/<collection>", methods=["POST"])
@protected
def auth_signup(collection: str):
    """
    handle user signup requests for a specified collection
    
    args:
        collection (str): actual name of the collection to register the user in
    """
    try:
        # signing up user
        req = signup(collection, request.json.get("document"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if user exists, return error indicating user already exists
    if not req:
        return abort(400)

    # returning results
    return jsonify(req), 200


# user verification route
@auth.route("/service/auth/v1/signin/<collection>/", methods=["POST"])
@auth.route("/service/auth/v1/signin/<collection>", methods=["POST"])
@protected
def auth_signin(collection: str):
    """
    handle user signin/authentication requests for a specified collection
    
    args:
        collection (str): actual name of the collection to authenticate the user against
    """
    try:
        # signing up user
        req = signin(collection, request.json.get("document"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # updating session
    session.update({collection: req[1]})

    # returning results
    return jsonify(req[0]), 200


# session retrival route
@auth.route("/service/auth/v1/session/<collection>/", methods=["GET"])
@auth.route("/service/auth/v1/session/<collection>", methods=["GET"])
@protected
def auth_session(collection: str):
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


# session deletion route
@auth.route("/service/auth/v1/signout/<collection>/", methods=["GET"])
@auth.route("/service/auth/v1/signout/<collection>", methods=["GET"])
def auth_signout(collection: str):
    """
    handle user signout / session termination requests for a specified collection
    
    args:
        collection (str): actual name of the collection to remove session data from
    """
    try:
        # signing out user
        session.pop(collection, None)

        # returning success response
        return jsonify(True), 200
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))
