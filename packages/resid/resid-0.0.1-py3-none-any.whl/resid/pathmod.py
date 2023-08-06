import os
import glob
import typing
from urllib import parse

import tempfile

# Defines allowed types for paths
PATH_TYPES = (str, bytes, os.PathLike)
_PATH = typing.Union[str, bytes, os.PathLike]

# Max size of characters pathname(e.g filename) can have.
# This does not mean the whole path.
MAX_PATH_NAME_LENGTH = 100


def walk(path: _PATH, recursive=False):
    # Returns paths(dirs, files) in provided path.
    # recursive if True match paths in sub-folder recursively.
    for root, directories, filenames in os.walk(path):
        for pathname in directories + filenames:
            yield os.path.join(root, pathname)
        if not recursive:
            break

def filter_files(paths: typing.Iterable[_PATH]):
    return filter(os.path.isfile, paths)

def filter_dirs(paths: typing.Iterable[_PATH]):
    return filter(os.path.isdir, paths)


def get_folder_files(path: _PATH, recursive=False):
    # Returns file paths in folder
    return filter_files(walk(path, recursive))

def get_folder_dirs(path: _PATH, recursive=False):
    # Returns file paths in folder
    return filter_dirs(walk(path, recursive)) 

def glob_pattern_paths(glob_path, recursive=False):
    return glob.glob(glob_path, recursive=recursive)


def extract_drive(path):
    return os.path.splitdrive(path)[0]

def remove_drive(path):
    return os.path.splitdrive(path)[1]


def is_path(_source, exists_callback=None, strict=True):
    if exists_callback == None:
        exists_callback = os.path.exists
    if isinstance(_source, PATH_TYPES):
        if strict:
            return exists_callback(_source)
        else:
            if exists_callback(_source):
                return True
            else:
                try:
                    with tempfile.NamedTemporaryFile('w', prefix=_source):
                        pass
                except OSError:
                    return False
                else:
                    return True
    else:
        return False


def is_file_path(_source, strict=True):
    return is_path(_source, os.path.isfile, strict)

def is_dir_path(_source, strict=True):
    return is_path(_source, os.path.isdir, strict)

def resembles_path(_source):
    # Guesses if object resembles path
    if _source and isinstance(_source, PATH_TYPES):
        if isinstance(_source, os.PathLike):
            return True
        _source = str(_source)
        drive, path = os.path.splitdrive(_source)
        parsed = parse.urlparse(_source)

        if parsed.netloc or parsed.params:
            # Path cant have hostname(likely other urls)
            return False
        elif parsed.scheme and not drive:
            # Path cant have scheme but miss drive part.
            return False
        else:
            path = os.path.normpath(path)
            path_names = filter(None, path.split(os.sep))
            for path_name in path_names:
                if not is_path(path_name, os.path.exists, False):
                    return False
            return True


def resembles_dir(_source):
    # Guesses if object resembles directory path
    if resembles_path(_source):
        # dir should not have to end with path sep or extension.
        path = os.path.normcase(_source)
        extension = os.path.splitext(path)[1]
        return path.endswith(os.sep) or not extension
    else:
        return False

def resembles_file_path(_source):
    # Guesses if object resembles file path
    if resembles_path(_source):
        #extension = os.path.splitext(_source)[1]
        path = os.path.normcase(_source)
        return not path.endswith(os.sep)
    else:
        return False


if __name__ == "__main__":
    import pathlib
    path = "/stackoverflow.com/\questions/3207219\\"
    print(resembles_file_path(path))