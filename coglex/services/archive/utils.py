"""
archive service module for managing file storage and retrieval operations
this module provides functionality for file management including upload, download, and delete
operations utilizing mongodb client for file metadata management and local file system for storage
"""


# standard imports
import os

# pip install python-magic
# file type identification
import magic

# werkzeug utilities and types
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

# mongodb storage module
from coglex.services.storage.utils import _insert, _find, _delete

# global configurations
import config


def _list(query: dict = {}, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> list[dict] | None:
    """
    retrieves metadata of all uploaded files from the specified collection

    args:
        query (dict): optional filter to apply when retrieving documents
        collection (str): name of the collection to retrieve from

    returns:
        list[dict] | None: a list of dictionaries containing file metadata for each uploaded file, or None if no documents found
    """
    try:
        # retrieve all documents from the collection
        documents = _find(collection, query)

        # if no documents found
        if not documents:
            return None

        # return list of file metadata
        return documents
    except Exception as ex:
        # rethrow exception
        raise ex


def _upload(file: FileStorage, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> str | None:
    """
    uploads a file and stores its metadata in the specified collection

    args:
        collection (str): the name of the collection to store the file metadata
        file: the file object to be stored

    returns:
        str: the inserted document's / file's id
        None: if file size exceeds max file size limit
    """
    try:
        # check file size against maximum limit
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)

        # reject file upload if size exceeds max size limit configuration; it is automatically rejected in http route by flask
        if size > config.MAX_CONTENT_LENGTH:
            return None

        # secure the filename
        name = secure_filename(file.filename)

        # save file to default upload folder
        path = os.path.join(config.APP_UPLOAD, name)
        file.save(path)

        # store metadata in our database system and return the id
        return _insert(collection, [{
            "_filename": name,
            "_filepath": path,  # store the upload folder path
            "_filesize": size,  # store file size in metadata
            "_filetype": magic.from_file(path, mime=True)  # store file type in metadata
        }])
    except Exception as ex:
        # rethrow exception
        raise ex


def _download(reference: str, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> tuple[str | None, str | None]:
    """
    retrieves a file path and filename based on its id from the specified collection

    args:
        collection (str): name of the collection to retrieve from
        reference (str): the id of the file to download

    returns:
        tuple: a tuple containing the file path and filename upon successful retrieval, or (None, None) if file not found
    """
    try:
        # retrieve file metadata
        document = _find(collection, {"_id": reference})

        # check if metadata exists
        if not document:
            return None, None

        # metadata is a dictionary and contains "_filepath" and "_filename" system reserved keys
        path = document.get("_filepath")

        # check if filepath exists
        if not path or not os.path.exists(path):
            return None, None

        # return filepath and filename
        return document.get("_filename"), path
    except Exception as ex:
        # rethrow exception
        raise ex


def _destroy(reference: str, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> bool:
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
        document = _find(collection, {"_id": reference})

        # check if metadata exists
        if not document:
            return False

        # retrieve filepath
        path = document.get("_filepath")

        # delete file from upload folder if it exists
        if path and os.path.exists(path):
            os.remove(path)

        # delete metadata from database system
        return _delete(collection, {"_id": reference})
    except Exception as ex:
        # rethrow exception
        raise ex
