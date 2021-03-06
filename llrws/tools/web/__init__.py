"""
/llrws/tools/web/__init__.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tools for client-interfacing or simple web tasks.
"""

import os

from flask import send_file

# Keep imported
from llrws.tools.web.validation import validate_file_properties


def send_file_for_download(filepath, filename, mimetype="text/csv"):
    """Sends a file for download to caller.

    Args:
        filepath (str): Path of file to send for download
        filename (str): File name to attach to download file

    Returns:
        (flask.wrappers.Response): File object for download
    """
    worklist = send_file(
        filepath,
        mimetype=mimetype,
        as_attachment=True,
        attachment_filename=filename,
        cache_timeout=-1,
    )
    worklist.headers["x-filename"] = filename
    worklist.headers["Access-Control-Expose-Headers"] = "x-filename"

    return worklist


def rm_files(filepaths):
    """Exhaustively removes files in an iterable of file paths.

    Args:
        filepaths (iter[(str)]): An iterable of file paths to be removed

    Returns:
        (None)
    """
    for file in filepaths:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
