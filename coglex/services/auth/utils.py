"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup, signin,
and otp verification utilizing mongodb client for user management
"""


# standard imports
import secrets
import hashlib
import hmac
from datetime import datetime, timezone, timedelta

# flask built-in session module
from flask import session

# mongodb storage module
from coglex.services.storage.utils import _insert, _find, _patch

# local helper imports
from utils import pcheck, phash, jwtenc

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


# identity / password signin approach implemented
# otp and oauth signin approaches are not implemented
# identity verification is not implemented

# identity verification (e.g., email, phone number) is left to be implemented as a gateway extension for other developers,
# this is to allow for custom identity verification methods (e.g., email verification, phone number verification)
# easily create a user with additional "verified" key set to False to require verification, and trigger verification process (e.g., email, sms)
# utilize verification / otp utilities for generating and verifying codes for either otp or verification processes
# on signin, only allow signin if user is verified using additional query
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
        })

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


def _passgen(_key: str, query: dict = {}, length: int = config.VERIFICATION_LENGTH, expiry: timedelta = config.VERIFICATION_EXPIRY, collection: str = config.MONGODB_AUTH_COLLECTION) -> str | None:
    """
    generates a verification code for otp or user verification and stores it in the database

    args:
        _key (str): unique identifier for the user (e.g., email or username)
        query (dict) (optional): additional query parameters to filter user documents
        length (int): length of the verification code
        expiry (timedelta): expiry time for the verification code
        collection (str): name of the collection to store verification data

    returns:
        str | None: generated verification code if successful, None if user not found or generation fails
    """
    try:
        # check if user exists
        authentication = _find(collection, {"_key": _key, **query})

        # if no user found or multiple users found (shouldn't happen with unique _key)
        if not authentication or isinstance(authentication, list):
            return None

        # generate random otp code
        passcode = "".join([str(secrets.randbelow(10)) for _ in range(length)])

        # hash the otp for secure storage
        _encryption = hashlib.sha256(passcode.encode()).hexdigest()

        # update user document with otp data and return code if successful
        if _patch(collection, {
            "$set": {
                "_otp_hash": _encryption,
                "_otp_expiry": datetime.now(timezone.utc) + expiry,  # caluclating expiry time
                "_otp_attempts": 0,
            }
        }, {"_key": _key}): return passcode

        # return None if update failed
        return None
    except Exception as ex:
        raise ex


def _passver(_key: str, passcode: str, query: dict = {}, attempts: int = config.VERIFICATION_ATTEMPTS, collection: str = config.MONGODB_AUTH_COLLECTION) -> bool:
    """
    verifies the provided verification code against the stored hash for the user

    args:
        _key (str): unique identifier for the user
        passcode (str): verification code to verify
        query (dict) (optional): additional query parameters to filter user documents
        attempts (int): maximum verification attempts allowed
        collection (str): name of the collection containing user data

    returns:
        bool: True if otp is valid and not expired, False otherwise
    """
    try:
        # find user with otp data
        authentication = _find(collection, {"_key": _key, **query})

        # if no user found or multiple users found (shouldn't happen with unique _key)
        if not authentication or isinstance(authentication, list):
            return False

        # check if verification hash exists
        if not authentication.get("_otp_hash"):
            return False

        # check if otp has expired
        if datetime.now(timezone.utc) > authentication.get("_otp_expiry", datetime.now(timezone.utc)):
            # optional otp credentials cleanup removed
            return False

        # check attempt limit
        if authentication.get("_otp_attempts", 0) >= attempts:
            # optional otp credentials cleanup removed
            return False

        # verify otp hash
        if hmac.compare_digest(authentication.get("_otp_hash"), hashlib.sha256(passcode.encode()).hexdigest()):
            # otp is valid, optional otp credentials cleanup removed
            return True

        # increment attempt counter in case of failed otp verification (hash mismatch)
        _patch(collection, {
            "$inc": {"_otp_attempts": 1}
        }, {"_key": _key})

        # returning failure
        return False
    except Exception as ex:
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
