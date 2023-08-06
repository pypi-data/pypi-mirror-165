import io


def is_memory_file(_source):
    # Checks if source is a file like object
    # created from: navaly source/naval/utility/file.py
    if isinstance(_source, io.IOBase):
        return True
    elif hasattr(_source, "write"):
        file_objs_attr = ["read", "truncate", "seek", "closed"]
        # this will work for _TemporaryFileWrapper class
        # its returned by tempfile.TemporaryFile() on windows
        return all([hasattr(_source, attr) for attr in file_objs_attr])
    else:
        return False
