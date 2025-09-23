"""
archive service module for managing file storage and retrieval operations
this module provides functionality for file management including upload, download, and delete
operations utilizing mongodb client for file metadata management and local file system for storage
"""

# standard imports
import os
import tempfile
import subprocess

# werkzeug utilities
from werkzeug.utils import secure_filename

# mongodb storage module
from coglex.services.storage.utils import _insert, _find, _delete

# global configurations
import config


def _upload(file, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> str or None:
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
            "_filesize": size  # store file size in metadata
        }])
    except Exception as ex:
        # rethrow exception
        raise ex


def _download(reference: str, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> tuple[str, str] or None:
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
        metadata = _find(collection, {"_id": reference})

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


def _fdelete(reference: str, collection: str = config.MONGODB_ARCHIVE_COLLECTION) -> bool:
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
        metadata = _find(collection, {"_id": reference})

        # check if metadata exists
        if not metadata:
            return False

        # retrieve filepath
        filepath = metadata.get("_filepath")

        # delete file from upload folder if it exists
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

        # delete metadata from database system
        return _delete(collection, {"_id": reference})
    except Exception as ex:
        # rethrow exception
        raise ex


def _scan(file) -> tuple[bool, str]:
    """
    scans a file for potential viruses using ClamAV antivirus engine, refer to README documentation for installation details

    args:
        file: file object from flask request

    returns:
        tuple: (clean: bool, raw: str)
            - clean: true if file is clean, false if infected
            - raw: scan result message or error description
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temporary = tmp.name
            # save uploaded file to temporary location
            file.save(temporary)

        try:
            # run clamscan cli
            execution = subprocess.run(
                ["clamscan", "--no-summary", temporary],
                capture_output=True, check=False,
                text=True
            )

            # parsing execution output
            stdout = execution.stdout.strip()

            # file is clean
            if "OK" in stdout:
                return True, str(stdout)

            # threat signature has been found
            if "FOUND" in stdout:
                return False, str(stdout)

            # analysis failed
            return False, str(stdout)
        finally:
            # clean up temporary file
            os.remove(temporary)
    except Exception as ex:
        raise ex
