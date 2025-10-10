"""
generation service routes for handling google gemini api interactions
provides endpoints for content creation, file uploads, and ai conversation generation.
"""


# standrad imports
import os
import tempfile

# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.generation.utils import _file, _converse


_generation = Blueprint("_generation", config.APP_IMPORT)


@_generation.route("/service/generation/v1/file/", methods=["POST"])
@_generation.route("/service/generation/v1/file", methods=["POST"])
@protected()
def transfer():
    """
    upload a file to the gemini api and return its url and mime type
    """
    try:
        # file upload attachment only
        if "file" not in request.files:
            abort(400)

        # retrieve required file attachment
        file = request.files.get("file")

        # validate attachment is not empty
        if not file or not file.filename:
            abort(400)

        # retrieving optional key parameter
        key = request.form.get("key")

        # save attachment to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            path = tmp.name

        # uploading file to google gemini api
        req = _file(path, key if key else config.GENERATION_KEY)

        # return file data as json response
        return jsonify({
            "fileData": {
                "fileUri": req.uri,
                "mimeType": req.mime_type
            }
        })
    except Exception as ex:
        abort(500, description=str(ex))
    finally:
        # ensure temporary file is deleted after use
        if os.path.exists(path):
            os.unlink(path)


@_generation.route("/service/generation/v1/converse/", methods=["POST"])
@_generation.route("/service/generation/v1/converse", methods=["POST"])
@protected()
def converse():
    """Generate response using Gemini model with content references."""

    # retrieve request parameters
    contents, system, tools, model, key = request.json.get("contents"), request.json.get("system"), request.json.get("tools"), request.json.get("model"), request.json.get("key")

    # validate required contents parameter
    if not contents:
        abort(400)

    try:
        # generate response using google gemini api
        req = _converse(contents, system, tools, model if model else config.GENERATION_MODEL, key if key else config.GENERATION_KEY)
    except Exception as ex:
        # rethrow exception
        abort(500, description=str(ex))

    # return generated response as json
    return jsonify({req}), 200
