"""
this module provides routing rules and endpoints for the database storage service
it handles http requests for crud operations on documents
in collections, with support for query parameters and document keys
"""


# importing required modules
import json

# importing flask's built-in modules
from flask import Blueprint, request, jsonify, abort

# importing base config parameters, and generic utilities
import config
from coglex import protected

# importing blueprint utilities used in current routing context
from coglex.services.storage.utils import _aggregate, _find, _insert, _patch, _delete


# blueprint instance
_storage = Blueprint("_storage", config.APP_IMPORT)


@_storage.route("/service/storage/v1/<collection>/aggregate/", methods=["POST"])
@_storage.route("/service/storage/v1/<collection>/aggregate", methods=["POST"])
@protected()
def aggregate(collection: str):
    """
    perform aggregation operations on documents in the specified collection

    args:
        collection (str): name of the collection to perform aggregation on
    """
    # get pipeline from request body
    pipeline = request.json.get("pipeline")

    # checking required parameters
    if not pipeline:
        return abort(400)

    try:
        # perform aggregation
        req = _aggregate(collection, pipeline)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no results found, return error
    if not req:
        return abort(404)

    # return aggregation results
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/<key>/", methods=["GET"])
@_storage.route("/service/storage/v1/<collection>/<key>", methods=["GET"])
@protected()
def find_one(collection: str, key: str):
    """
    retrieve a single document from the specified collection based on its key

    args:
        collection (str): name of the collection to query
        key (str): unique identifier of the document to retrieve
    """
    # safely parse keys from request args using json.loads if present
    keys = request.args.get("keys")

    try:
        # find document matching query
        req = _find(collection, {"_id": key}, json.loads(keys) if keys else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/", methods=["GET"])
@_storage.route("/service/storage/v1/<collection>", methods=["GET"])
@protected()
def find_many(collection: str):
    """
    retrieve multiple documents from the specified collection based on query parameters

    args:
        collection (str): actual name of the collection to query
    """
    # safely parse query and keys from request args using json.loads if present
    query, keys = request.args.get("query"), request.args.get("keys")

    try:
        # find documents matching query
        req = _find(collection, json.loads(query) if query else None, json.loads(keys) if keys else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # returning results
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/", methods=["POST"])
@_storage.route("/service/storage/v1/<collection>", methods=["POST"])
@protected()
def insert_many(collection: str):
    """
    insert multiple documents into the specified collection

    args:
        collection (str): name of the collection to insert the documents into
    """
    # get documents from request body
    documents = request.json.get("documents")

    # checking required parameters
    if not documents:
        return abort(400)

    try:
        # insert documents
        req = _insert(collection, documents)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if record inserted, return success
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/<key>/", methods=["PATCH"])
@_storage.route("/service/storage/v1/<collection>/<key>", methods=["PATCH"])
@protected()
def patch_one(collection: str, key: str):
    """
    update a single document in the specified collection based on its key

    args:
        collection (str): name of the collection containing the document to update
        key (str): unique identifier of the document to update
    """
    # get document from request body
    document = request.json.get("document")

    # checking required parameters
    if not document:
        return abort(400)

    try:
        # patch document
        req = _patch(collection, document, {"_id": key})
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # if record patched, return success
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/", methods=["PATCH"])
@_storage.route("/service/storage/v1/<collection>", methods=["PATCH"])
@protected()
def patch_many(collection: str):
    """
    update multiple documents in the specified collection based on query parameters

    args:
        collection (str): actual name of the collection to query
    """
    # retreiving document and query from request body
    document, query = request.json.get("document"), request.json.get("query")

    # checking required parameters
    if not document:
        return abort(400)

    try:
        # patch document
        req = _patch(collection, document, query)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # if record patched, return success
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/<key>/", methods=["DELETE"])
@_storage.route("/service/storage/v1/<collection>/<key>", methods=["DELETE"])
@protected()
def delete_one(collection: str, key: str):
    """
    delete a single document from the specified collection based on its key

    args:
        collection (str): name of the collection containing the document to delete
        key (str): unique identifier of the document to delete
    """
    try:
        # delete document
        req = _delete(collection, {"_id": key})
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # if record deleted, return success
    return jsonify(req), 200


@_storage.route("/service/storage/v1/<collection>/", methods=["DELETE"])
@_storage.route("/service/storage/v1/<collection>", methods=["DELETE"])
@protected()
def delete_many(collection: str):
    """
    delete multiple documents from the specified collection based on query parameters

    args:
        collection (str): actual name of the collection to query
    """
    # safely parse query from request args using json.loads if present
    query = request.args.get("query")

    try:
        # delete document
        req = _delete(collection, json.loads(query) if query else None)
    except Exception as ex:
        # rethrow exception
        return abort(500, description=str(ex))

    # if no records found, return error
    if not req:
        return abort(404)

    # if record deleted, return success
    return jsonify(req), 200
