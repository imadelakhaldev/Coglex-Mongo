"""
this module provides routing rules and endpoints for the database storage service
it handles http requests for crud operations (create, read, update, delete) on documents
in collections, with support for query parameters and document keys

routes:
    GET /service/storage/v1/<collection>/ - retrieve multiple documents
    GET /service/storage/v1/<collection>/<key>/ - retrieve a specific document
    POST /service/storage/v1/<collection>/ - insert a new document
    PATCH /service/storage/v1/<collection>/<key>/ - update a specific document
    DELETE /service/storage/v1/<collection>/<key>/ - delete a specific document
"""


# importing required modules
import json

# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.storage.utils import find, insert, patch, delete


# blueprint instance
storage = Blueprint("storage", config.APP_IMPORT)


# accepting get requests for multiple document queries
@storage.route("/service/storage/v1/<collection>/", methods=["GET"])
@storage.route("/service/storage/v1/<collection>", methods=["GET"])
@protected
def storage_find_many(collection: str):
    """
    retrieve multiple documents from the specified collection based on query parameters

    args:
        collection (str): actual name of the collection to query
    """
    # convert keys string to dictionary if present
    # safely parse keys from request args using json.loads if present
    query = request.args.get("query")
    keys = request.args.get("keys")

    try:
        # find documents matching query
        req = find(collection, json.loads(query) if query else None, json.loads(keys) if keys else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


# accepting get requests for single specific document query
@storage.route("/service/storage/v1/<collection>/<key>/", methods=["GET"])
@storage.route("/service/storage/v1/<collection>/<key>", methods=["GET"])
@protected
def storage_find_one(collection: str, key: str):
    """
    retrieve a single document from the specified collection based on its key

    args:
        collection (str): name of the collection to query
        key (str): unique identifier of the document to retrieve
    """
    # convert keys string to dictionary if present
    # safely parse keys from request args using json.loads if present
    keys = request.args.get("keys")

    try:
        # find document matching query
        req = find(collection, {"_id": key}, json.loads(keys) if keys else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


# accepting post requests for single insertions
@storage.route("/service/storage/v1/<collection>/", methods=["POST"])
@storage.route("/service/storage/v1/<collection>", methods=["POST"])
@protected
def storage_insert(collection: str):
    """
    insert a new document into the specified collection

    args:
        collection (str): name of the collection to insert the document into
    """
    try:
        # insert document
        req = insert(collection, request.json.get("document"))
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if record inserted, return success
    return jsonify(req), 200


# accepting patch requests for single document updates
@storage.route("/service/storage/v1/<collection>/<key>/", methods=["PATCH"])
@storage.route("/service/storage/v1/<collection>/<key>", methods=["PATCH"])
@protected
def storage_patch(collection: str, key: str):
    """
    update a single document in the specified collection based on its key

    args:
        collection (str): name of the collection containing the document to update
        key (str): unique identifier of the document to update
    """
    try:
        # patch document
        req = patch(collection, request.json.get("document"), {"_id": key})
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # if record patched, return success
    return jsonify(req), 200


# accepting delete requests for single document suppressions
@storage.route("/service/storage/v1/<collection>/<key>/", methods=["DELETE"])
@storage.route("/service/storage/v1/<collection>/<key>", methods=["DELETE"])
@protected
def storage_delete(collection: str, key: str):
    """
    delete a single document from the specified collection based on its key

    args:
        collection (str): name of the collection containing the document to delete
        key (str): unique identifier of the document to delete
    """
    try:
        # delete document
        req = delete(collection, {"_id": key})
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # if record deleted, return success
    return jsonify(req), 200
