"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup, signin,
and otp verification utilizing mongodb client for user management
"""


# standard imports
import secrets
from datetime import timedelta

# url parsing and encoding utilities
from urllib.parse import urlencode

# flask built-in session module
from flask import session

# third-party imports for oauth
import requests

# mongodb storage module
from coglex.services.storage.utils import _insert, _find, _patch

# local helper imports
from utils import pcheck, phash, jwtenc, jwtdec

# global confirgurations
import config


def _signup(_key: str, _password: str = None, document: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> str | None:
    """
    creates a new user document in the specified collection, handles user registration by storing their information in the database

    args:
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str) (optional): password for the user account, None if not password enabled authentication
        document (dict) (optional): additional user information to store
        collection (str): the name of the collection to store the user document

    returns:
        str: the unique identifier (_id) of the newly created user document, None if user creation fails or required fields are missing
    """
    try:
        # check if user already exists
        if _find(collection, {"_key": _key}):
            return None

        # hash password if present before storing
        if _password:
            _password = phash(_password)

        # inject _key and _password to document and create new user
        return _insert(collection, [{"_key": _key, "_password": _password, **document}])
    except Exception as ex:
        # rethrow exception
        raise ex


# identity / password signin approach implemnentation
def _signin(_key: str, _password: str = None, query: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> str | None:
    """
    authenticates a user by validating their credentials and issues a jwt token

    args:
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str) (optional): password for the user account, None if not password enabled authentication
        query (dict) (optional): additional query parameters to filter user documents for example active=True to only allow signin for active users
        collection (str): name of the collection to authenticate against

    returns:
        str | None: jwt token string upon successful authentication, None if authentication fails
    """
    try:
        # find user without password in query
        authentication = _find(collection, {"_key": _key, **query})

        # if no user found, return none
        if not authentication:
            return None

        # ensure "user" is a single dictionary, not a list
        if isinstance(authentication, list):
            # this shouldn't happen if _key is unique, but good to handle
            return None

        # verify if password is present
        if _password:
            # verify password hash matches
            if not pcheck(_password, authentication.get("_password")):
                return None

        # storing user identifier
        # storing hashed password (allows us to password change)
        # storing additonal query (allows us to verify if user is active or not, and other criteria)
        # generate jwt token for later user authentication
        token = jwtenc({
            "_key": _key,
            "_password": authentication.get("_password"),
            **query
        }, config.SERVER_SESSION_LIFETIME)

        # store generated token in session
        session[collection] = token

        # return generated token
        return token
    except Exception as ex:
        # rethrow exception
        raise ex


def _retrieve(_key: str, query: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> dict | None:
    """
    retrieves a user document from the specified collection by _key and optional query filters

    args:
        _key (str): unique identifier for the user (e.g., email or username)
        query (dict) (optional): additional query parameters to filter user documents
        collection (str): name of the collection to search against

    returns:
        dict | None: user document if found and matches criteria, None otherwise
    """
    try:
        # find user document
        authentication = _find(collection, {"_key": _key, **query})

        # if no user found or multiple users found (shouldn't happen with unique _key)
        if not authentication or isinstance(authentication, list):
            return None

        # return authentication document
        return authentication
    except Exception as ex:
        # rethrow exception
        raise ex


def _refresh(_key: str, document: dict, query: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> int | None:
    """
    updates user information in the specified collection

    args:
        _key (str): unique identifier for the user whose document is to be updated
        document (dict): dictionary containing update operators (e.g. $set) and their values
        query (dict) (optional): additional filter criteria to apply before updating
        collection (str): the name of the collection containing user documents

    returns:
        int | None: number of documents updated if successful, None otherwise
    """
    try:
        # find user first to verify existence
        if not _find(collection, {"_key": _key, **query}):
            return None

        # prepare the update document
        construction = {}

        # reconstruct given document to hash password if exists
        for operation, fields in document.items():
            if operation == "$set" and isinstance(fields, dict) and fields.get("_password"):
                # clone and hash the password inside $set
                fields = fields.copy()
                fields["_password"] = phash(fields["_password"])

            # add operation to construction
            construction[operation] = fields

        # update user document
        return _patch(collection, construction, {"_key": _key})
    except Exception as ex:
        raise ex


# otp and verification utilities implementation
def _passgen(length: int = config.VERIFICATION_LENGTH, expiry: timedelta = config.VERIFICATION_EXPIRY) -> tuple(str, str):
    """
    generates a stateless otp using jwt encoding without database storage

    args:
        length (int): length of the otp code
        expiry (timedelta): expiry time for the otp

    returns:
        tuple(str, str): tuple containing otp code and jwt token if successful
    """
    try:
        # generate random otp code
        passcode = "".join([str(secrets.randbelow(10)) for _ in range(length)])

        # encode passcode jwt with expiry and return actual code and token
        return (passcode, jwtenc(passcode, expiry))
    except Exception as ex:
        # rethrow exception
        raise ex


def _passver(passcode: str, token: str) -> bool:
    """
    verifies a stateless otp using jwt decoding without database lookup

    args:
        passcode (str): otp code to verify
        token (str): jwt token containing otp data

    returns:
        bool: True if otp is valid, False otherwise
    """
    try:
        # decode actual passcode from token, and verify it with provided passcode
        if passcode == jwtdec(token):
            return True

        # otp is invalid, not equal to tokenized passcode
        return False
    except Exception as ex:
        # rethrow exception
        raise ex


def _oauth(provider: str, redirect_uri: str) -> str | None:
    """
    generates oauth authorization url for the specified provider

    args:
        provider (str): oauth provider name (google, facebook)
        redirect_uri (str): callback url for oauth flow

    returns:
        str | None: authorization url if provider is valid, None otherwise
    """
    try:
        # validate provider
        if provider not in config.OAUTH_CONFIG:
            return None

        # generate jwt-based state for csrf protection if not provided
        state = jwtenc({
            "provider": provider,
            "redirect_uri": redirect_uri,
            "nonce": secrets.token_urlsafe(16)
        })

        # get provider configuration
        provider_config = config.OAUTH_CONFIG[provider]

        # build authorization parameters
        params = {
            "client_id": provider_config["CLIENT_ID"],
            "redirect_uri": redirect_uri,
            "scope": provider_config["SCOPES"],
            "response_type": "code",
            "state": state
        }

        # return authorization url
        return f"{provider_config['AUTHORIZE_URL']}?{urlencode(params)}"
    except Exception as ex:
        # rethrow exception
        raise ex


def _ocall(code: str, state: str) -> dict | None:
    """
    handles oauth callback by exchanging authorization code for access token and retrieving user info

    args:
        code (str): authorization code from oauth provider
        state (str): state parameter for csrf verification
        redirect_uri (str): callback url used in authorization

    returns:
        dict | None: user information dictionary with normalized fields (name, email, provider), None if verification fails
    """
    try:
        # decode and verify jwt state for csrf protection
        state = jwtdec(state)

        # verify state payload contains required fields and nonce
        if not state or not state.get("provider") or not state.get("redirect_uri") or not state.get("nonce"):
            return None

        # validate provider
        if state.get("provider") not in config.OAUTH_CONFIG:
            return None

        # get provider configuration
        provider_config = config.OAUTH_CONFIG[state.get("provider")]

        # exchange code for access token
        token_data = {
            "code": code,
            "client_id": provider_config["CLIENT_ID"],
            "client_secret": provider_config["CLIENT_SECRET"],
            "redirect_uri": state.get("redirect_uri"),
            "grant_type": "authorization_code"
        }

        # request access token
        token_response = requests.post(provider_config["TOKEN_URL"], data=token_data, headers={}, timeout=12)
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        # check for access token
        if not access_token:
            return None

        # get user info using access token
        user_response = requests.get(provider_config["USERINFO_URL"], headers={"Authorization": f"Bearer {access_token}"}, timeout=12)
        user_info = user_response.json()

        # check for user info
        if not user_info:
            return None

        # normalize user data (different providers return different fields)
        normalized_user = {
            "name": user_info.get("name") or user_info.get("login") or "User",
            "email": user_info.get("email") or "No email provided",
            "provider": state.get("provider"),
            "provider_id": str(user_info.get("id", ""))
        }

        return normalized_user
    except Exception as ex:
        # rethrow exception
        raise ex


def _signout(collection: str = config.MONGODB_AUTH_COLLECTION) -> bool:
    """
    signs out the current user by removing the token from the session

    args:
        collection (str): the name of the collection (used as session key) to remove the token from

    returns:
        bool: True if the token was successfully removed, False otherwise
    """
    # checking if token exists in session
    if not session.get(collection):
        return False

    # remove token from collection key if it exists
    session.pop(collection, None)

    # return success
    return True
