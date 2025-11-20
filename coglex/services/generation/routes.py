"""
generation service routes for handling google gemini and groq api interactions
provides endpoints for ai conversation generation using either Google Gemini or Groq models
"""


# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.generation.utils import _goconverse, _grconverse


_generation = Blueprint("_generation", config.APP_IMPORT)


@_generation.route("/service/generation/v1/google/", methods=["POST"])
@_generation.route("/service/generation/v1/google", methods=["POST"])
@protected()
def goconverse():
    """
    generate response using google's gemini model with content references
    """

    # retrieve request parameters
    contents, system, model, key = request.json.get("contents"), request.json.get("system"), request.json.get("model"), request.json.get("key")

    # validate required contents parameter
    if not contents:
        abort(400)

    try:
        # generate response using google gemini api
        req = _goconverse(contents, system, model if model else config.GOOGLE_GENERATION_MODEL, key if key else config.GOOGLE_GENERATION_KEY)
    except Exception as ex:
        # rethrow exception
        abort(500, description=str(ex))

    # return generated response as json
    return jsonify({req}), 200


@_generation.route("/service/generation/v1/groq/", methods=["POST"])
@_generation.route("/service/generation/v1/groq", methods=["POST"])
@protected()
def grconverse():
    """
    generate response using groq's model with content references
    """

    # retrieve request parameters
    contents, system, model, key = request.json.get("contents"), request.json.get("system"), request.json.get("model"), request.json.get("key")

    # validate required contents parameter
    if not contents:
        abort(400)

    try:
        # generate response using groq api
        req = _grconverse(contents, system, model if model else config.GROQ_GENERATION_MODEL, key if key else config.GROQ_GENERATION_KEY)
    except Exception as ex:
        # rethrow exception
        abort(500, description=str(ex))

    # return generated response as json
    return jsonify({req}), 200
