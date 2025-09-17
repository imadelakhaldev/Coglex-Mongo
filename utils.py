"""
utility module containing multi-use functions and local helpers used throughout the project scope
this module provides common utility functions and helper methods that are used across different parts of the project
"""


# standard library imports
import random

# pip install colorama
# cross-platform terminal colored inputs
from colorama import Fore, Style

# pip install bcrypt
# password hashing library
# heavy import moved to local functions, instead of global module import
# import bcrypt

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


def fstring(template: str, variables: dict) -> str:
    """
    format a string by replacing placeholders with values from a dictionary
    
    args:
        template (str): string template with placeholders in format "{ key }"
        variables (dict): dictionary containing key-value pairs for replacement
        
    returns:
        str: formatted string with replaced placeholders
    """
    for key, value in variables.items():
        placeholder = "{ " + key + " }"
        template = template.replace(placeholder, str(value))

    return template


def hexgen(length: int = config.MONGODB_HEX_LENGTH) -> str:
    """
    generate a random hexadecimal string of specified length

    args:
        length (int): length of the hexadecimal string to generate

    returns:
        str: randomly generated hexadecimal string of specified length
    """
    return "".join([hex(x)[2:] for x in random.randbytes(length // 2)])


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
