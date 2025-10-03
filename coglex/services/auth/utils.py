"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup and signin
operations utilizing mongodb client for user management and authentication
"""


# flask built-in session module
from flask import session

# mongodb storage module
from coglex.services.storage.utils import _insert, _find, _patch

# local helper imports
from utils import pcheck, phash, jwtenc

# global confirgurations
import config


def _signup(_key: str, _password: str, document: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> str | None:
    """
    creates a new user document in the specified collection, handles user registration by storing their information in the database

    args:
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str): user's password for authentication 
        document (dict) (optional): additional user information to store
        collection (str): the name of the collection to store the user document

    returns:
        str: the unique identifier (_id) of the newly created user document, None if user creation fails or required fields are missing
    """
    try:
        # check if user already exists
        if _find(collection, {"_key": _key}):
            return None

        # hash the password before storing
        _password = phash(_password)

        # inject _key and _password to document and create new user
        return _insert(collection, [{"_key": _key, "_password": _password, **document}])
    except Exception as ex:
        # rethrow exception
        raise ex


def _signin(_key: str, _password: str, query: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> str | None:
    """
    authenticates a user by validating their credentials and issues a jwt token

    args:
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str): user's password for authentication
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

        # verify password hash matches
        if not pcheck(_password, authentication.get("_password")):
            return None

        # storing user identifier
        # storing hashed password (not a good practice, but it's safe since we are storing the "hashed" password (not plaintext one), into a secured jwt token)
        # storing additonal query (allows us to verify if user is active or not, and other criteria)
        # generate jwt token for later user authentication
        token = jwtenc((_key, authentication.get("_password"), query))

        # store generated token in session
        session["token"] = token

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
            if operation == "$set" and isinstance(fields, dict) and "_password" in fields:
                # clone and hash the password inside $set
                fields = fields.copy()
                fields["_password"] = phash(fields["_password"])

            # add operation to construction
            construction[operation] = fields

        # update user document
        return _patch(collection, construction, {"_key": _key})
    except Exception as ex:
        raise ex
