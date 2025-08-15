"""
utility module containing multi-use functions and local helpers used throughout the project scope
this module provides common utility functions and helper methods that are used across different parts of the project
"""


# standard library imports
import random
from datetime import datetime

# pip install PyJWT
# jwt for token generation
import jwt

# pip install colorama
# cross-platform terminal colored inputs
from colorama import Fore, Style

# programmable signal handling
from blinker import Namespace

# stripe webhook signal
stripe_webhook_received = Namespace().signal("stripe-webhook-received")

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


# generate a random hexadecimal string of specified length
def hexgen(length: int = config.MONGODB_HEX_LENGTH) -> str:
    """
    generate a random hexadecimal string of specified length

    args:
        length (int): length of the hexadecimal string to generate

    returns:
        str: randomly generated hexadecimal string of specified length
    """
    return "".join([hex(x)[2:] for x in random.randbytes(length // 2)])


# encode jwt token for user authentication
def jwtenc(document: dict, expiration: datetime = datetime.utcnow() + config.SERVER_SESSION_LIFETIME, key: str = config.SERVER_SECRET) -> str:
    """
    generate a jwt (json web token) for user authentication

    args:
        document (dict): dictionary containing user data to be encoded in the token
        expiration (datetime): token expiration timestamp, defaults to current utc time plus global value
        key (str): secret key used for token encoding, defaults to global value

    returns:
        str: generated jwt token string encoded with the server secret
    """
    # generate and return jwt token
    return jwt.encode({**document, **{"exp": expiration}}, key, algorithm="HS256")


# decode jwt token for user authentication
def jwtdec(token: str, key: str = config.SERVER_SECRET) -> dict:
    """
    decode a jwt (json web token) for user authentication

    args:
        token (str): jwt token string to decode
        key (str): secret key used for token decoding, defaults to global value

    returns:
        dict: decoded token payload containing user data
    """
    try:
        # decode and return jwt token
        return jwt.decode(token, key, algorithms=["HS256"])
    except Exception:
        # return none if token is invalid
        return None
