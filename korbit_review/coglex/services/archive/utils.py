"""
archive service module for managing file storage and retrieval operations
this module provides functionality for file management including upload, download, and delete
operations utilizing mongodb client for file metadata management and local file system for storage
"""

# standard imports
import os
import tempfile

# werkzeug utilities
from werkzeug.utils import secure_filename

# mongodb storage module
from coglex.services.storage.utils import insert, find, delete


def upload(collection: str, file) -> str:
    """
    uploads a file and stores its metadata in the specified collection

    args:
        collection (str): the name of the collection to store the file metadata
        file: the file object to be stored

    returns:
        str: the inserted document's / file's id
    """
    try:
        # secure the filename
        filename = secure_filename(file.filename)

        # create a temporary directory to save the file
        filepath = os.path.join(tempfile.mkdtemp(), filename)
        file.save(filepath)

        # store metadata in our database system and return the id
        return insert(collection, {
            "_filename": filename,
            "_filepath": filepath,  # store the temporary path
        })
    except Exception as ex:
        # rethrow exception
        raise ex


def download(collection: str, reference: str) -> tuple or None:
    """
    retrieves a file path and filename based on its id from the specified collection

    args:
        collection (str): name of the collection to retrieve from
        reference (str): the id of the file to download

    returns:
        tuple: a tuple containing the file path and filename upon successful retrieval
    """
    try:
        # retrieve file metadata
        metadata = find(collection, {"_id": reference})

        # check if metadata exists
        if not metadata:
            return None, None

        # assuming file_metadata is a dictionary and contains "_filepath" and "_filename" system reserved keys
        filepath = metadata.get("_filepath")
        filename = metadata.get("_filename")

        # check if filepath exists
        if not filepath or not os.path.exists(filepath):
            return None, None

        # return filepath and filename
        return filepath, filename
    except Exception as ex:
        # rethrow exception
        raise ex


def f_delete(collection: str, reference: str) -> bool:
    """
    deletes a file and its metadata from the specified collection

    args:
        collection (str): name of the collection to delete from
        reference (str): the id of the file to delete

    returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # retrieve file metadata
        metadata = find(collection, {"_id": reference})

        # check if metadata exists
        if not metadata:
            return False

        # retrieve filepath
        filepath = metadata.get("_filepath")

        # delete file from local storage if it exists
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

            # also remove the temporary directory if it's empty
            temp = os.path.dirname(filepath)
            if not os.listdir(temp):
                os.rmdir(temp)

        # delete metadata from database system
        return delete(collection, {"_id": reference})
    except Exception as ex:
        # rethrow exception
        raise ex
