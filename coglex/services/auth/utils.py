"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup and signin
operations utilizing mongodb client for user management and authentication
"""


# importing flask's built-in modules
from flask import session

# local helper imports
from utils import pcheck, phash

# mongodb storage module
from coglex.services.storage.utils import _insert, _find, _patch

# global confirgurations
import config


def _signup(_key: str, _password: str, document: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> str | None:
    """
    creates a new user document in the specified collection

    this function handles user registration by storing their information in the database

    args:
        collection (str): the name of the collection to store the user document
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str): user's password for authentication 
        document (dict) (optional): additional user information to store

    returns:
        str: the unique identifier (_id) of the newly created user document, None if user creation fails or required fields are missing
    """
    try:
        # check if user already exists
        if _find(collection, {"_key": _key}):
            return None

        # remove duplicated fields in document
        document.pop("_key", None)
        document.pop("_password", None)

        # hash the password before storing
        _password = phash(_password)

        # inject _key and _password to document and create new user
        return _insert(collection, [{"_key": _key, "_password": _password, **document}])
    except Exception as ex:
        # rethrow exception
        raise ex


def _signin(_key: str, _password: str, query: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> dict or None:
    """
    authenticates a user by validating their credentials

    args:
        collection (str): name of the collection to authenticate against
        _key (str): unique identifier for the user (e.g., email or username)
        _password (str): user's password for authentication
        query (dict) (optional): additional query parameters to filter user documents for example active=True to only allow signin for active users

    returns:
        dict | None: user document dictionary containing user information upon successful authentication, None if authentication fails
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

        # saving signin query for later user checking (e.g., active=True)
        authentication["_query"] = query

        # updating flask session for usage across framework
        session.update({collection: authentication})

        # returning the authentication document (user)
        return authentication
    except Exception as ex:
        # rethrow exception
        raise ex


def _verify(_key: str, query: dict = {}, collection: str = config.MONGODB_AUTH_COLLECTION) -> dict | None:
    """
    verifies if a user exists and matches additional query criteria

    args:
        collection (str): name of the collection to verify against
        _key (str): unique identifier for the user (e.g., email or username)
        query (dict) (optional): additional query parameters to filter user documents

    returns:
        dict | None: user document if user exists and matches criteria, None otherwise
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
        raise ex



def _signout(collection: str = config.MONGODB_AUTH_COLLECTION) -> bool:
    """
    signs out a user by removing their session data

    args:
        collection (str): the name of the collection to remove session data from

    returns:
        bool: true if signout is successful, exception otherwise
    """
    try:
        # signing out user, remove user's session
        if collection in session:
            session.pop(collection, None)

        # success return
        return True
    except Exception as ex:
        # rethrow exception
        raise ex


def _refresh(_key: str, document: dict, collection: str = config.MONGODB_AUTH_COLLECTION) -> int | None:
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
        # find user first to verify existence
        if not _find(collection, {"_key": _key}):
            return None

        # handle password updates separately if included
        if "_password" in document:
            document["_password"] = phash(document.get("_password"))

        # update user document
        return _patch(collection, {"$set": document}, {"_key": _key})
    except Exception as ex:
        raise ex
