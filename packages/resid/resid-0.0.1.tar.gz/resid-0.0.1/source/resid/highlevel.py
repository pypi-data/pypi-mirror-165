# Define high level functions for the project.
# Functions that are useful at high level are defined here.
# It include guessing content type, encoding and others.

from . import master
from . import document

__all__ = [
    "find_resource",
    "find_resources",
    "guess_content_type",
    "guess_encoding",
    "locally_hosted",
    "remotely_hosted",
    "is_supported",
    "is_resembled",
    "to_string",
    "guess_type",
    "guess_name",

    "is_path",
    "is_file_path",
    "is_dir_path",
    "is_path_like",
    "is_file_path_url",
    "is_url",
    "is_web_url",
    "is_file_like"
]

def find_resources(source, strict=False, **kwargs):
    # Find resources instances closely related to source.
    # master contains resource objects created from source.
    master_obj = master.Master(source, **kwargs)
    # Gets supported resources from master.
    # Supported resources clearly matches the source.
    # Supported resources take precidence over resembled ones.
    supported_resources = master_obj.supported_resources
    if supported_resources:
        return supported_resources
    elif not strict:
        # Gets resources resembling source.
        # Resemblimg resources are not guaranteed to be supported.
        # e.g url may still be invalid or file path not existing.
        return master_obj.resembles_resources
    else:
        return []
    
def find_resource(source, strict=False, **kwargs):
    # Find resource instance supporting or resembling source.
    # Returns None if source cannot satisfy any of resource object.
    # find_resources() but performance may be impacted.
    # Supported resource has priority over resmbling ones.
    master_obj = master.Master(source, **kwargs)
    supported_resource = master_obj.supported_resource
    if supported_resource:
        return supported_resource
    elif not strict:
        return master_obj.resembles_resource


def _find_resource_types(source, strict=False, **kwargs):
    # Returns resources classes supported or rembling source.
    # This is done by first finding resource objects and then getting
    # their classes.
    _resources = find_resources(source, strict, **kwargs)
    return [_resource.__class__ for _resource in _resources]

def _resource_access_attr(_resource, attribute, default=None):
    # Accesses attribute of resource object.
    # Takes into account resource being None(see find_resource())
    # 'default' argument will be returned in place of None.
    # If attribute does not exists exception will be raised.
    if _resource:
        value = getattr(_resource, attribute)
        if value != None:
            return value
    return default

def _find_resource_access_attr(source, attribute, strict=False, 
    default=None, **kwargs):
    # Finds resource object and access attribute from it.
    # None is returned when resource object cannot be found.
    # None also when the attribute has value of None(likely)
    resource_object = find_resource(source, strict, **kwargs)
    return _resource_access_attr(resource_object, attribute, default)

def guess_content_type(source):
    # Guesses content type of contents of source
    return _find_resource_access_attr(source, "content_type")

def guess_encoding(source):
    # Guesses encording of contents of source
    return _find_resource_access_attr(source, "encoding")

def locally_hosted(source):
    # Returns True if contents of source are available locally
    return _find_resource_access_attr(source, "locally")

def remotely_hosted(source):
    # Returns True if contents of source are available remotely.
    return _find_resource_access_attr(source, "remotely")

def is_supported(source):
    # Returns if source is supported(e.g is valid url)
    return _find_resource_access_attr(source, "supported", default=False)

def is_resembled(source):
    # Returns True if source resembles classes for supported sources.
    # Source may be valid file path but not existing.
     return _find_resource_access_attr(source, "resembles", default=False)

def to_string(source):
    # returns string version of source(None if not supported)
    return _find_resource_access_attr(source, "uri")

def guess_type(source):
    # Returns string about type of source provided source.
    # It may be files path, file like object, etc.
    return _find_resource_access_attr(source, "uri_type")

def guess_name(source):
    # Guesses name of source(string version of source)
    return to_string(source)



def _source_matches_resource_type(source, resource_type, strict=False):
    # Checks if ssource upports or resembles resource type(class)
    # resource_types = _find_resource_types(source, strict)
    # return resource_type in resource_types
    _resource = resource_type(source)
    supported = _resource.supported
    if supported:
        return supported
    elif not strict:
        return _resource.resembles
    else:
        return False

def is_path(source, strict=False):
    # Checks if source is dir or file path
    return _source_matches_resource_type(source, document.Path, strict)

def is_file_path(source, strict=False):
    # Checks if source is file path
    return _source_matches_resource_type(source, document.FilePath, strict)

def is_dir_path(source, strict=False):
    # Checks if source is file path
    return _source_matches_resource_type(source, document.DirPath, strict)

def is_path_like(source, strict=False):
    # Checks if source is a path like object
    return _source_matches_resource_type(source, document.PathLike, strict)

def is_file_path_url(source, strict=False):
    # Checks if source is url for local file path(file://)
    return _source_matches_resource_type(source, document.FilePathURL, strict)

def is_url(source, strict=False):
    # Checks if source is url(file path not included)
    return _source_matches_resource_type(source, document.URL, strict)

def is_web_url(source, strict=False):
    # Checks if source is url for web documents
    return _source_matches_resource_type(source, document.WebURL, strict)

def is_file_like(source, strict=False):
    # Checks if source is file like object
    return _source_matches_resource_type(source, document.FileMemory, strict)

def is_memory_file(source, strict=False):
    # Checks if source is file like object
    return is_file_like(source, strict)



if __name__ == "__main__":
    resource = find_resource("file.py")
    print(guess_type("git://www.example.com/search?q=mimetypes+"))
    