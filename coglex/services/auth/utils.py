"""
authentication service module for managing user authentication operations
this module provides functionality for user authentication including signup and signin
operations utilizing mongodb client for user management and authentication
"""


# pip install bcrypt
# password hashing library
import bcrypt

# mongodb storage module
from coglex.services.storage.utils import insert, find

# global generic utilities
from utils import jwtenc


def signup(collection: str, document: dict) -> str or None:
    """
    creates a new user document in the specified collection

    args:
        collection (str): the name of the collection to store the user document
        document (dict): the user document to be stored

    returns:
        str: the inserted document's / user's id
    """
    try:
        # check if password is present in document
        password = document.pop("_password", None)
        if not password:
            return None

        # check if user already exists
        authentication = find(collection, document)

        # if user already exists
        if authentication:
            return None

        # hash the password before storing
        document["_password"] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # create new user
        return insert(collection, document)
    except Exception as ex:
        # rethrow exception
        raise ex


def signin(collection: str, query: dict) -> tuple or None:
    """
    authenticates a user

    args:
        collection (str): name of the collection to authenticate against
        query (dict): authentication credentials (e.g., email and password)

    returns:
        dict: a dictionary containing the jwt token and user document upon successful authentication
    """
    try:
        # extract password from query before searching
        password = query.pop("_password", None)
        if not password:
            return None

        # find user without password in query
        authentication = find(collection, query)

        # if no user found, return none
        if not authentication:
            return None

        # ensure "user" is a single dictionary, not a list
        if isinstance(authentication, list):
            # this shouldn't happen if email / index is unique, but good to handle
            return None

        # verify password hash matches
        if not bcrypt.checkpw(password.encode("utf-8"), authentication.get("_password").encode("utf-8")):
            return None

        # generate jwt token for user authentication
        # we are passing the collection and query as claims in the token
        # add password back to query before encoding in jwt
        query["_password"] = password
        return jwtenc({"collection": collection, "query": query}), authentication
    except Exception as ex:
        # rethrow exception
        raise ex
