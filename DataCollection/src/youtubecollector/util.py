import os as _os


def is_empty_file(filename: str):
    if not isinstance(filename, str):
        raise Exception(f"filename should be a string of an existing file")

    if not _os.path.exists(filename):
        raise Exception(f"{filename} doesn't exists")

    return _os.stat(filename).st_size == 0


def convert_to_dictionary(obj):
    return {field: getattr(obj, field) for field in obj._fields}