"""
this module implements rest api endpoints for user authentication and account management
it provides the following core functionality:

- user registration (signup)
- user authentication (signin) 
- user profile retrievals
- user profile updates

the routes in this module handle http requests for these operations and integrate
with the underlying authentication services
"""


# importing required modules
import json

# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.auth.utils import _signup, _signin, _retrieve, _refresh, _passgen, _passver, _signout


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
    - document: optional additional user data
    """
    # retreiving user id, and additional document from request body (might contain _password for password-enabled auth)
    _key, document = request.json.get("_key"), request.json.get("document")

    # checking required parameters
    if not _key:
        return abort(400)

    try:
        # signing up user
        req = _signup(_key, document)
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
    authenticate a user against the auth collection

    expects json payload with:
    - _key: unique identifier for the user
    - query: optional additional filter criteria

    returns user data and session token on success
    """
    # retreiving user id, and additional query from request body (might contain _password for password-enabled auth)
    _key, query = request.json.get("_key"), request.json.get("query")

    # checking required parameters
    if not _key:
        return abort(400)

    try:
        # signing in user
        req = _signin(_key, query)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/<_key>/", methods=["GET"])
@_auth.route("/service/auth/v1/<_key>", methods=["GET"])
@protected()
def retrieve(_key: str):
    """
    retrieve a user profile by key

    expects path parameter:
    - _key: unique identifier for the user

    expects json payload with:
    - query: optional additional filter criteria

    returns user data on success
    """
    # safely parse query from request args using json.loads if present
    query = request.args.get("query")

    try:
        # retrieving user data
        req = _retrieve(_key, json.loads(query) if query else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no user found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_auth.route("/service/auth/v1/<_key>/", methods=["PATCH"])
@_auth.route("/service/auth/v1/<_key>", methods=["PATCH"])
@protected()
def refresh(_key: str):
    """
    update a user profile by key

    expects path parameter:
    - _key: unique identifier for the user

    expects json payload with:
    - document: updated user data
    - query: optional additional filter criteria

    returns updated user data on success
    """
    # retreiving user id, and additional query from request body
    document, query = request.json.get("document"), request.json.get("query")

    # checking required parameters
    if not document:
        return abort(400)

    try:
        # refreshing user data
        req = _refresh(_key, document, query)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no user found to update, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200

@_auth.route("/service/auth/v1/verification/<_key>/", methods=["GET"])
@_auth.route("/service/auth/v1/verification/<_key>", methods=["GET"])
@protected()
def generation(_key: str):
    """
    generate a one-time passcode (OTP) for the specified user

    expects path parameter:
    - _key: unique identifier for the user

    expects query parameter:
    - query: optional additional filter criteria

    returns the generated otp details on success
    """
    # safely parse query from request args using json.loads if present
    query = request.args.get("query")

    try:
        # generate otp for user
        req = _passgen(_key, json.loads(query) if query else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if otp generation failed because user retrieval, return error
    if not req:
        return abort(404)

    # return success response
    return jsonify(req), 200


@_auth.route("/service/auth/v1/verification/<_key>/<passcode>/", methods=["GET"])
@_auth.route("/service/auth/v1/verification/<_key>/<passcode>", methods=["GET"])
@protected()
def verification(_key: str, passcode: str):
    """
    verify a one-time passcode (otp) for the specified user

    expects path parameters:
    - _key: unique identifier for the user
    - passcode: the otp code to verify

    expects query parameter:
    - query: optional additional filter criteria

    returns verification result on success
    """
    # safely parse query from request args using json.loads if present
    query = request.args.get("query")

    # retrieve parameters from request body
    try:
        # verify otp code
        req = _passver(_key, passcode, json.loads(query) if query else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if verification failed, return error
    if not req:
        return abort(400)

    # return success response
    return jsonify(req), 200


@_auth.route("/service/auth/v1/signout/", methods=["GET"])
@_auth.route("/service/auth/v1/signout", methods=["GET"])
@protected()
def signout():
    """
    this endpoint clears the session token stored on the server side,
    effectively logging the user out

    returns success confirmation on successful invalidation
    """
    # returning success confirmation
    return jsonify(_signout()), 200
