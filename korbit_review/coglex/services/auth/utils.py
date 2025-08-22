"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup and signin
operations utilizing mongodb client for user management and authentication
"""


# pip install bcrypt
# password hashing library
import bcrypt

# mongodb storage module
from coglex.services.storage.utils import insert, find, patch

# global generic utilities
from utils import jwtenc


def signup(collection: str, _key: str, _password: str, document: dict) -> str | None:
    """
    creates a new user document in the specified collection

    this function handles user registration by storing their information in the database

    args:
        collection (str): the name of the collection to store the user document
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str): user's password for authentication 
        document (dict): additional user information to store

    returns:
        str: the unique identifier (_id) of the newly created user document, None if user creation fails or required fields are missing
    """
    try:
        # remove duplicated fields in document
        document.pop("_key", None)
        document.pop("_password", None)

        # check if user already exists
        if find(collection, {"_key": _key}):
            return None

        # hash the password before storing
        _password = bcrypt.hashpw(_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # inject _key and _password to document and create new user
        return insert(collection, {"_key": _key, "_password": _password, **document})
    except Exception as ex:
        # rethrow exception
        raise ex


def signin(collection: str, _key: str, _password: str) -> tuple or None:
    """
    authenticates a user by validating their credentials

    args:
        collection (str): name of the collection to authenticate against
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str): user's password for authentication

    returns:
        tuple: a tuple containing (jwt_token, user_document) upon successful authentication, where jwt_token is a string and user_document is a dictionary containing user information, returns None if authentication fails
    """
    try:
        # find user without password in query
        authentication = find(collection, {"_key": _key})

        # if no user found, return none
        if not authentication:
            return None

        # ensure "user" is a single dictionary, not a list
        if isinstance(authentication, list):
            # this shouldn't happen if _key is unique, but good to handle
            return None

        # verify password hash matches
        if not bcrypt.checkpw(_password.encode("utf-8"), authentication.get("_password").encode("utf-8")):
            return None

        # generate jwt token for user authentication
        # we are passing the collection and query as claims in the token
        return jwtenc({"collection": collection, "_key": _key, "_password": _password}), authentication
    except Exception as ex:
        # rethrow exception
        raise ex


def refresh(collection: str, _key: str, document: dict) -> int | None:
    """
    updates user information in the specified collection

    args:
        collection (str): the name of the collection containing user documents
        _key (str): unique identifier for the user to update
        document (dict): dictionary containing the fields to update and their new values

    returns:
        int | None: number of documents updated if successful, none otherwise
    """
    try:
        # handle password updates separately if included
        if "_password" in document:
            document["_password"] = bcrypt.hashpw(document.get("_password").encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # find user first to verify existence
        if not find(collection, {"_key": _key}):
            return None

        # update user document
        return patch(collection, document, {"_key": _key})
    except Exception as ex:
        raise ex


# email verification can be added as an extended custom authentication utility in gateway using smtp and token generation
# signup fraud can be added as an extended custom authentication utility in gateway using fingerprintjs
# password reset can be added as an extended custom authentication utility in gateway using smtp and token generation
# social login can be later added as an extended custom authentication utility in gateway using oauth2
# mentioned utilities can be later decided to be included in core system framework
