"""
utility functions for interacting with the google gemini api

this module provides helper functions to create content objects, upload files,
count tokens, and generate responses using the google gemini model
"""


# standard imports
from pathlib import Path

# pip install google-genai
from google import genai
from google.genai import types

# pip install python-magic
# file type identification
import magic

# global configuration variables
import config


def _file(file: str, key: str = config.GENERATION_KEY) -> types.File:
    """
    return a gemini file object, if a path is provided, upload it
    if a gemini file id (e.g., "files/abc123xyz") is provided, retrieve it

    args:
        file (str): path or gemini file id
        key (str): google ai api key
    """
    try:
        # configure gemini client
        client = genai.Client(api_key=key)

        # case 1: already a Gemini file id
        if file.startswith("files/"):
            # return file object
            return client.files.get(name=file)

        # case 2: local file path, upload it
        # return processed file
        return client.files.upload(file=Path(file, mime_type=magic.from_file(file, mime=True)))
    except Exception as ex:
        # rethrow exception
        raise ex


def _converse(contents: list[str | dict], system: str = None, tools: list[dict] = None, model: str = config.GENERATION_MODEL, key: str = config.GENERATION_KEY,) -> str | dict:
    """
    generate content using the gemini model with optional system instructions and tools

    args:
        contents (list[str | dict]): list of content parts (text or dict representations)
        system (str, optional): system instruction to guide the model's behavior
        tools (list[dict], optional): list of function declarations for tool use
        model (str, optional): the gemini model to use for generation
        key (str, optional): google ai api key

    returns:
        str | dict: the first candidate's content parts from the generation, or None if no candidates
    """
    try:
        # configure gemini client
        client = genai.Client(api_key=key)

        # passing content json format parts, and generation config
        generation = client.models.generate_content(model=model, contents=contents, config=types.GenerateContentConfig(system_instruction=system, tools=[types.Tool(function_declarations=tools)]))

        # check generation candidates
        if not generation.candidates:
            return None

        # retrieving parts from generation candidates (including text, function call, images, audio, etc)
        return generation.candidates[0].content.parts
    except Exception as ex:
        # rethrow exception
        raise ex
