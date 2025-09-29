"""
archive service routes module
the routes handle file storage and retrieval functionality

this module provides routing rules and endpoints for archive operations including:
- file upload
- file download
- file deletion
"""


# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort, send_file

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.archive.utils import _upload, _download, _destroy, _list


# blueprint instance
_archive = Blueprint("_archive", config.APP_IMPORT)


@_archive.route("/service/archive/v1/", methods=["GET"])
@_archive.route("/service/archive/v1", methods=["GET"])
@protected()
def directory():
    """
    list all uploaded files
    """
    try:
        # listing files
        req = _list(query=request.json.get("query"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no documents found
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_archive.route("/service/archive/v1/", methods=["POST"])
@_archive.route("/service/archive/v1", methods=["POST"])
@protected()
def upload():
    """
    handle file upload requests for a specified collection
    """
    # uploading file
    if "file" not in request.files:
        return abort(400)

    # get the file from the request
    file = request.files.get("file")

    # check if the file is valid
    if file.filename == "":
        return abort(400)

    try:
        # upload the file
        req = _upload(file)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # check if the file was uploaded successfully in case of file size was too large
    # file entity size configuration is left to be handled by flask itself, since it will reject request by itself when file size exceeds MAX_CONTENT_LENGTH config
    if not req:
        return abort(413)

    # returning results
    return jsonify(req), 200


@_archive.route("/service/archive/v1/<reference>/", methods=["GET"])
@_archive.route("/service/archive/v1/<reference>", methods=["GET"])
@protected()
def download(reference: str):
    """
    handle file download requests for a specified collection and reference
    
    args:
        reference (str): the id of the file to download
    """
    try:
        # downloading file
        filename, filepath = _download(reference)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # check if the file exists
    if not filepath:
        return abort(404)

    # return file for download
    return send_file(filepath, as_attachment=True, download_name=filename)


@_archive.route("/service/archive/v1/<reference>/", methods=["DELETE"])
@_archive.route("/service/archive/v1/<reference>", methods=["DELETE"])
@protected()
def destroy(reference: str):
    """
    handle file deletion requests for a specified collection and reference
    
    args:
        reference (str): the id of the file to delete
    """
    try:
        # deleting file
        req = _destroy(reference)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # check if the file exists
    if not req:
        return abort(404)

    # return success
    return jsonify(True), 200
