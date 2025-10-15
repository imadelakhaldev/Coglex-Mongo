"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup, signin,
and otp verification utilizing mongodb client for user management
"""


# standard imports
import secrets
from datetime import timedelta

# request encoding utilities
from urllib.parse import urlencode
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

        # if no user found or multiple users found (shouldn't happen with unique _key)
        if not authentication or isinstance(authentication, list):
            return None

        # verify if password is present
        if _password:
            # verify password hash matches
            if not pcheck(_password, authentication.get("_password")):
                return None

        # generate and return jwt token for later user authentication
        # nothing is stored server side, stateless approach
        return jwtenc({
            "_key": _key,
            "_password": authentication.get("_password"),
            **query
        }, config.SERVER_SESSION_LIFETIME)
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
def _passgen(length: int = config.VERIFICATION_LENGTH, expiry: timedelta = config.VERIFICATION_EXPIRY) -> tuple[str, str]:
    """
    generates a stateless otp using jwt encoding without database storage

    args:
        length (int): length of the otp code
        expiry (timedelta): expiry time for the otp

    returns:
        tuple(str, str): tuple containing otp code and jwt token if successful
    """
    # generate random otp code
    passcode = "".join([str(secrets.randbelow(10)) for _ in range(length)])

    # encode passcode jwt with expiry and return actual code and token
    return (passcode, jwtenc(passcode, expiry))


def _passver(passcode: str, token: str) -> bool:
    """
    verifies a stateless otp using jwt decoding without database lookup

    args:
        passcode (str): otp code to verify
        token (str): jwt token containing otp data

    returns:
        bool: True if otp is valid, False otherwise
    """
    # decode actual passcode from token, and verify it with provided passcode
    if passcode == jwtdec(token):
        return True

    # otp is invalid, not equal to tokenized passcode
    return False


def _oauth(provider: str, redirect: str) -> str:
    """
    generates oauth authorization url for the specified provider

    args:
        provider (str): oauth provider name (google, facebook)
        redirect (str): callback url for oauth flow

    returns:
        str: authorization url if provider is valid, None otherwise
    """
    # validate provider
    cfg = config.OAUTH_PROVIDERS.get(provider)

    # validate provider configuration
    if not cfg:
        return None

    # generate state parameter for csrf protection
    state = secrets.token_urlsafe(16)

    # build authorization parameters
    params = {
        "client_id": cfg["CLIENT_ID"],
        "redirect_uri": redirect,
        "scope": cfg["SCOPES"],
        "response_type": "code",
        "state": jwtenc(state, config.OAUTH_EXPIRY)  # store state parameter in token for later verification
    }

    # build and return authorization url
    return f"{cfg['AUTHORIZE_URL']}?{urlencode(params)}"


def _ocall(provider: str, redirect: str, state: str, code: str) -> dict | None:
    """
    handles oauth callback by exchanging authorization code for access token and retrieving user info

    args:
        provider (str): oauth provider name (google, facebook)
        redirect (str): callback url used in authorization
        state (str): state parameter used for csrf protection
        code (str): authorization code from oauth provider

    returns:
        dict | None: user information dictionary with normalized fields (name, email, identifier), None if verification fails
    """
    # validate provider configuration
    cfg = config.OAUTH_PROVIDERS.get(provider)

    # verify provider configuration exists
    if not cfg:
        return None

    # decode state parameter from token, if it's valid, it's ours
    if not jwtdec(state):
        return None

    try:
        # exchange authorization code for access token
        access_token = requests.post(
            cfg["TOKEN_URL"],
            data={
                "code": code,
                "client_id": cfg["CLIENT_ID"],
                "client_secret": cfg["CLIENT_SECRET"],
                "redirect_uri": redirect,
                "grant_type": "authorization_code"
            },
            timeout=12
        ).json().get("access_token")

        # verify access token exists in response
        if not access_token:
            return None

        # retrieve user information using access token
        user_info = requests.get(
            cfg["INFO_URL"],
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=12
        ).json()

        # verify user information exists in response
        if not user_info:
            return None

        # normalize user information fields
        return {
            "name": user_info.get("name") or user_info.get("login"),
            "email": user_info.get("email"),
            "identifier": str(user_info.get("id", ""))
        }
    except Exception as ex:
        # handle exception, and raise
        raise ex
