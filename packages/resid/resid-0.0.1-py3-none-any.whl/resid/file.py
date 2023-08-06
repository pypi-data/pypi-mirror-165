from . import urlmod
from . import weburl
from . import filepath
from . import file_memory


def is_memory_file(_source):
    # Checks if source is a file like object
    # created from: navaly source/naval/utility/file.py
    return file_memory.is_memory_file(_source)

def is_remote_file(_source):
    # Checks if source points to remote file(e.g webpage)
    if weburl.is_web_url(_source):
        # extract the path part of url
        path_part = urlmod.extract_path(_source)
        content_type = filepath.guess_content_type(path_part)
        # url pointing to file should have file extension
        return bool(content_type)
    return False


def is_local_file(_source):
    # Checks if source points to file on local machine
    if not is_remote_file(_source):
        return filepath.is_file_path(_source, False)
    else:
        return False


     
