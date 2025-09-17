"""
mongodb interpretation utilities for crud operations
this module provides utility functions for creating, reading, updating and deleting
records in mongodb collections, it includes functions for finding records,
inserting new records, patching existing records, and deleting records
"""


# importing base config parameters, and generic utilities
from utils import hexgen

# importing the mongodb client created in application initialization
from coglex import storage


def _find(collection: str, query: dict = {}, keys: dict = {}) -> dict or list[dict] or None:
    """
    find records in a mongodb collection that match a specific query

    args:
        collection (str): name of the mongodb collection to search in
        query (dict, optional): filter criteria to filter records
        keys (dict, optional): fields to include/exclude in the response

    returns:
        dict or list[dict] or none: list of records if multiple records are found, single record if single record is found, none if no records are found
    """
    try:
        # find records matching query
        retrievals = list(storage.get_collection(collection).find(query, keys))

        # returning results
        if retrievals:
            # returning single result if single record is found or list if multiple records are found
            return retrievals[0] if len(retrievals) == 1 else retrievals

        # returning no results
        return None
    except Exception as ex:
        # rethrow exception
        raise ex


def _insert(collection: str, documents: list[dict]) -> list[str]:
    """
    insert multiple records into a specified mongodb collection

    args:
        collection (str): name of the mongodb collection to insert into
        documents (list[dict]): list of records to be inserted into the collection

    returns:
        list[str]: list of inserted ids of the records if successful
    """
    try:
        # generate _id for each document and prepare for insertion
        # insert documents with generated IDs
        execution = storage.get_collection(collection).insert_many([{**document, **{"_id": hexgen()}} for document in documents])

        # convert ObjectIds to strings
        references = [str(_id) for _id in execution.inserted_ids]

        # return single id if one document, list if multiple
        return references[0] if len(references) == 1 else references
    except Exception as ex:
        # rethrow exception
        raise ex


def _patch(collection: str, document: dict, query: dict = {}) -> int or None:
    """
    update records in a mongodb collection that matches a specific query

    args:
        collection (str): name of the mongodb collection to update
        document (dict): record containing the fields to update ($set, $inc, $push, and every other operator are accepted)
        query (dict, optional): filter criteria to identify records to update

    returns:
        int or none: count of records updated if successful, none if no records were updated
    """
    try:
        # update document
        execution = storage.get_collection(collection).update_many(query, document)

        # if record updated, return success
        if execution.matched_count > 0:
            return execution.modified_count

        # if record not found, return error
        return None
    except Exception as ex:
        # rethrow exception
        raise ex


def _delete(collection: str, query: dict = {}) -> int or None:
    """
    delete records from a mongodb collection that matches a specific query

    args:
        collection (str): name of the mongodb collection to delete from
        query (dict, optional): filter criteria to identify the record to delete

    returns:
        int or none: count of records deleted if successful, none if no records were deleted
    """
    try:
        # delete document
        execution = storage.get_collection(collection).delete_many(query)

        # if record deleted, return success
        if execution.deleted_count > 0:
            return execution.deleted_count

        # if record not found, return error
        return None
    except Exception as ex:
        # rethrow exception
        raise ex
