import os
import mimetypes
import typing

from . import pathmod


if not mimetypes.inited:
    mimetypes.init()

def _bytes_to_string(__object, *args, **kwargs):
    # Convert bytes object to string.
    # Other object types are returned unchanged.
    if isinstance(__object, bytes):
        return __object.decode(*args, **kwargs)
    else:
        return __object

def guess_content_type(file_path):
    file_path = _bytes_to_string(file_path)
    return mimetypes.guess_type(file_path, False)[0]

def guess_encoding(file_path):
    file_path = _bytes_to_string(file_path)
    return mimetypes.guess_type(file_path, False)[1]

def guess_extension(content_type):
    return mimetypes.guess_extension(content_type, False)

def guess_extensions(content_type):
    file_path = _bytes_to_string(file_path)
    return mimetypes.guess_all_extensions(content_type, False)

def equal_content_type(file_path, other_file_path):
    # Returns True if files paths have same content type
    file_path_type = guess_content_type(file_path)
    other_file_path_type = guess_content_type(other_file_path)
    if file_path_type and other_file_path_type:
        return file_path_type == other_file_path_type
    else:
        return False


def extract_extension(file_path):
    return os.path.splitext(file_path)[1]

def extract_filename(file_path):
    return os.path.split(file_path)[1]

def remove_extension(filename: str):
    return os.path.splitext(filename)[0]


    
def is_pdf_file(file_path):
    return equal_content_type(file_path, " .pdf")

def is_docx_file(file_path):
    return equal_content_type(file_path, " .docx")

def is_doc_file(file_path):
    return equal_content_type(file_path, " .doc")

def is_word_file(file_path):
    return is_docx_file(file_path) or is_doc_file(file_path)

def is_pptx_file(file_path):
    return equal_content_type(file_path, " .pptx")

def is_ppt_file(file_path):
    return equal_content_type(file_path, " .ppt")

def is_html_file(file_path):
    if equal_content_type(file_path, " .html"):
        return True
    elif equal_content_type(file_path, " .htm"):
        return True
    else:
        return False

def is_json_file(file_path):
    return equal_content_type(file_path, " .json")

def is_csv_file(file_path):
    return equal_content_type(file_path, " .csv")

def is_plain_text_file(file_path):
    return equal_content_type(file_path, " .txt")

def is_text_file(file_path):
    content_type = guess_content_type(file_path)
    if content_type:
        return "text/" in content_type
    else:
        return False


if __name__ == "__main__":
    path = "/projects/resid.com"
