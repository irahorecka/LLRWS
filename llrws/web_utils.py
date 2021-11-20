import os

from flask import current_app, send_file
from werkzeug.utils import secure_filename


def save_CSV_fileobj_to_filepath(fileobj, filepath):
    """Validates then saves CSV fileobj as filepath if validation is successful.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage object to validate and save
        filepath (str): Filepath to save fileobj if validation succeeds

    Returns:
        (bool, str): Indicator of validation success, "" (if success) or error message (if failure)
    """
    # Null error message
    error_msg = ""
    # Convert fileobj.filename to secure filename before evaluating.
    filename = secure_filename(fileobj.filename)
    # Extract missing filetype: e.g., 'reference' from 'X-X-X-X-X-reference.csv'.
    missing_filetype = f'MAVE {filepath.split("-")[-1].split(".")[0]}'

    # Validate fileobj
    if not fileobj:
        error_msg = f"Missing {missing_filetype} CSV file."
        return False, error_msg
    # Validate filename
    if not bool(filename):
        error_msg = f"Missing {missing_filetype} CSV file."
        return False, error_msg
    # Validate file extension
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{missing_filetype} file does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        return False, error_msg

    # Save file
    fileobj.save(filepath)
    return True, error_msg


def send_file_for_download(filepath, filename):
    """Sends a file for download to the web-app user.

    Args:
        filepath (str): Path to file to send for download
        filename (str): File name to attach to file for download

    Returns:
        (flask.wrappers.Response): File object for download
    """
    worklist = send_file(
        filepath,
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
        filepaths (iter): An iterable of file paths to be removed

    Returns:
        (None)
    """
    # Check if filepaths in an iterable container.
    if not isinstance(filepaths, (dict, list, set, tuple)):
        filepaths = [filepaths]
    for file in filepaths:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass