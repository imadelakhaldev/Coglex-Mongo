"""
utility module containing multi-use functions and local helpers used throughout the project scope
this module provides common utility functions and helper methods that are used across different parts of the project
"""


# standard imports
from typing import Any
from datetime import datetime

# pip install colorama
# cross-platform terminal colored inputs
from colorama import Fore, Style

# pip install bcrypt
# password hashing library
# heavy import moved to local functions, instead of global module import
# import bcrypt

# pip install PyJWT
# jwt for token generation
import jwt

# pip install google-genai
from google import genai
from google.genai import types

# local imports
import config


# prints colored terminal output using colorama
def sprint(color: str, content: str) -> None:
    """
    print colored terminal text using colorama

    args:
        color (str): color to print the text in, must be a valid "colorama.Fore" color name
        content (str): actual text to print in color
    """
    print(f"{getattr(Fore, color.upper(), Fore.RESET)}{content}{Style.RESET_ALL}")


def phash(password: str) -> str:
    """
    hash a password using bcrypt with salt

    args:
        password (str): the plain text password to hash

    returns:
        str: the hashed password as a utf-8 string
    """
    import bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def pcheck(password: str, hashed: str) -> bool:
    """
    check if a password matches a hashed password using bcrypt

    args:
        password (str): the plain text password to check
        hashed (str): the hashed password to compare against

    returns:
        bool: true if the password matches the hashed password, false otherwise
    """
    import bcrypt
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def jwtenc(content: Any, expiration: datetime = None, key: str = config.SERVER_SECRET) -> str:
    """
    generate a jwt (json web token) for user authentication

    args:
        content (any): any data to be encoded in the token
        expiration (datetime) (optional): token expiration timestamp, defaults to none (no expiration)
        key (str): secret key used for token encoding

    returns:
        str: generated jwt token string encoded with the server secret
    """
    # prepare payload with content (using "_" as key to store all types of content in the token)
    payload = {"_": content}

    # add expiration timestamp if provided, if not no expiration will be set
    if expiration:
        payload["exp"] = expiration

    # generate and return jwt token
    return jwt.encode(payload, key, algorithm="HS256")


def jwtdec(token: str, key: str = config.SERVER_SECRET) -> Any | None:
    """
    decode a jwt (json web token) for user authentication

    args:
        token (str): jwt token string to decode
        key (str): secret key used for token decoding, defaults to global value

    returns:
        any | None: decoded token payload containing data if valid, none otherwise
    """
    try:
        # decode and return jwt token
        return jwt.decode(token, key, algorithms=["HS256"]).get("_")
    except Exception:
        # return none if token is invalid or expired
        return None


def tokenize(contents: list[str | types.Content | types.File], model: str = config.GENERATION_MODEL, key: str = config.GENERATION_KEY) -> int:
    """
    count the number of tokens in a list of contents using a specified model's tokenizer

    args:
        contents (list[str | types.Content | types.File]): the input contents to tokenize and count
        model (str): the name of the model whose tokenizer will be used for counting
        key (str): google ai api key

    returns:
        int: the total number of tokens in the contents
    """
    try:
        # configure gemini client
        client = genai.Client(api_key=key)

        # Count tokens using the client method
        return client.models.count_tokens(model=model, contents=contents).total_tokens
    except Exception as ex:
        raise ex
