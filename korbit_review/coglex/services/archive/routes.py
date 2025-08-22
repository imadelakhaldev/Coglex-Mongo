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
from coglex.services.archive.utils import upload, download, f_delete


# blueprint instance
archive = Blueprint("archive", config.APP_IMPORT)


# file upload route
@archive.route("/service/archive/v1/upload/<collection>/", methods=["POST"])
@archive.route("/service/archive/v1/upload/<collection>", methods=["POST"])
@protected
def archive_upload(collection: str):
    """
    handle file upload requests for a specified collection
    
    args:
        collection (str): actual name of the collection to store the file in
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
        req = upload(collection, file)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # returning results
    return jsonify(req), 200


# file download route
@archive.route("/service/archive/v1/download/<collection>/<reference>/", methods=["GET"])
@archive.route("/service/archive/v1/download/<collection>/<reference>", methods=["GET"])
@protected
def archive_download(collection: str, reference: str):
    """
    handle file download requests for a specified collection and reference
    
    args:
        collection (str): actual name of the collection to retrieve the file from
        reference (str): the id of the file to download
    """
    try:
        # downloading file
        filepath, filename = download(collection, reference)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # check if the file exists
    if not filepath:
        return abort(404)

    # return file for download
    return send_file(filepath, as_attachment=True, download_name=filename)


# file deletion route
@archive.route("/service/archive/v1/delete/<collection>/<reference>/", methods=["DELETE"])
@archive.route("/service/archive/v1/delete/<collection>/<reference>", methods=["DELETE"])
@protected
def archive_delete(collection: str, reference: str):
    """
    handle file deletion requests for a specified collection and reference
    
    args:
        collection (str): actual name of the collection to delete the file from
        reference (str): the id of the file to delete
    """
    try:
        # deleting file
        req = f_delete(collection, reference)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # check if the file exists
    if not req:
        return abort(404)

    # return success
    return jsonify(True), 200
