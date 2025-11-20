"""
utility functions for interacting with the google gemini api

this module provides helper functions to create content objects, upload files,
count tokens, and generate responses using the google gemini model
"""


# standard imports
import json

# pip install google-genai
from google import genai
from google.genai import types

# pip install groq
from groq import Groq

# global configuration variables
import config


def _goconverse(contents: list[str | dict], system: str = None, model: str = config.GOOGLE_GENERATION_MODEL, key: str = config.GOOGLE_GENERATION_KEY, structured: bool = False) -> str | dict:
    """
    generate content using the gemini model with optional system instructions and structured output

    args:
        contents (list[str | dict]): list of content parts (text or dict representations).
        system (str, optional): system instruction to guide the model's behavior.
        model (str, optional): the gemini model to use for generation.
        key (str, optional): google ai api key.
        structured (bool, optional): if True, parse the response as a json object.

    returns:
        tuple[str | dict | None, int | None, int | None]:
            - generated content (string or parsed json dict if structured=True)
            - number of input tokens used
            - number of output tokens used
            returns (None, None, None) if no valid response or usage data.
    """
    try:
        # configure gemini client
        client = genai.Client(api_key=key)

        # passing content json format parts, and generation config
        generation = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json" if structured else None
            )
        )

        # check generation candidates and token usage metadata
        if not generation.candidates or not generation.usage_metadata:
            return None, None, None

        # extracting content from generation candidates
        content = generation.candidates[0].content.parts[0].text

        # if structured output requested, parse json text
        if structured:
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                pass

        # extracting token usage from generation candidates
        itokens = generation.usage_metadata.prompt_token_count
        otokens = generation.usage_metadata.candidates_token_count

        # retrieving parts from generation candidates
        return content, itokens, otokens
    except Exception as ex:
        # rethrow exception
        raise ex


def _grconverse(contents: list[str | dict], system: str = None, model: str = config.GROQ_GENERATION_MODEL, key: str = config.GROQ_GENERATION_KEY, structured: bool = False) -> tuple[str | dict | list | None, int | None, int | None]:
    """
    generate content using groq chat completions with optional system instruction and structured output

    args:
        contents (list[str | dict]): list of message parts, strings are treated as user messages.
        system (str, optional): system instruction to guide the model's behavior.
        model (str, optional): groq model name (default: llama-3.1-8b-instant).
        key (str, optional): groq api key; if not provided, uses GROQ_API_KEY env var.
        structured (bool, optional): if true, parse response as json object.

    returns:
        tuple[str | dict | list | None, int | None, int | None]:
            - generated content (string, parsed json, or list)
            - number of input tokens used
            - number of output tokens used
            returns (None, None, None) if no valid response or usage data.
    """
    try:
        # configure groq client
        client = Groq(api_key=key)

        # include system instruction at the first of content parts if provided
        if system:
            contents.insert(0, {"role": "system", "content": system.strip()})

        # generate completion using groq chat completions
        completion = client.chat.completions.create(
            model=model,
            messages=contents,
            temperature=1,
            max_completion_tokens=4096,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"} if structured else None,
            stop=None
        )

        # check completion choices, and token usage metadata
        if not completion.choices or not completion.usage:
            return None, None, None

        # prefer content string; fallback to stringified message
        content = completion.choices[0].message.content

        # if structured output requested, parse json text
        if structured:
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                pass

        # extract prompt and completion tokens from usage metadata
        itokens = completion.usage.prompt_tokens
        otokens = completion.usage.completion_tokens

        # return content with separate token counts
        return content, itokens, otokens
    except Exception as ex:
        # rethrow exception
        raise ex
