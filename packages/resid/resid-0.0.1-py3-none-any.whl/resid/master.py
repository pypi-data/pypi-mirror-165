# Manages resource classes and objects.
# It takes care of creating resource object based on source.
# This is inspired from 'navaly project.

from . import resource
from . import document

from typing import List
from typing import Type
from typing import Iterable


# Default resources classes(order matters)
# The more specific class is the more top it is.
# FilePath is more specific than Path.
_DEFAULT_RESOURCE_TYPES = (
    # file-system like path
    document.FilePathURL,
    document.FilePathLike,
    document.FilePath,
    document.DirPathLike,
    document.DirPath,
    document.Path,

    # urls
    document.WebURL,
    document.URL,

    # file like object
    document.FileMemory,
)
resources_types = [*_DEFAULT_RESOURCE_TYPES]



class ResourceTypes():
    # Manages Resource types(classes) to be used by Master class.
    # Class is not used in favour of list of Resource objects.
    def __init__(self, resources_types) -> None:
        self._resource_types = list(resources_types)

    def add_resource_type(self, resource_type):
        self._resource_types.add(resource_type)

    def remove_resource_type_(self, resource_type):
        self._resource_types.discard(resource_type)

    def get_resource_types(self):
        return self._resource_types


class Resources():
    # Manages Resource instances to be used by Master class.
    def __init__(self, resources: Iterable[resource.Resource]) -> None:
        self._resources = resources

    def set_resources(self, resources):
        self._resources = resources

    def get_resources(self):
        return self._resources

    def _filter(self, resources, callback) -> List[resource.Resource]:
        # returns list with filtered resources by provided callback
        return list(filter(callback, resources))

    def _single_filter(self, resources, callback) -> resource.Resource:
        # Returns first resource satisfyting callback
        for resource in resources:
            if callback(resource):
                return resource
        return None

    @property
    def supported_resources(self):
        # Returns list of supported resources
        return self._filter(self._resources, lambda res: res.supported)

    @property
    def resembles_resources(self):
        # Returns list of resources resembling source
        return self._filter(self._resources, lambda res: res.resembles)

    @property
    def issues_resources(self):
        # Returns list of resources with issues
        return self._filter(self._resources, lambda res: res.issues)

    @property
    def success_resources(self):
        # Returns list of success resources.
        # This is opposite of issues_resources.
        return self._filter(self._resources, lambda res: res.success)


    @property
    def supported_resource(self):
        # Returns first resource supported.
        callback = lambda res: res.supported
        return self._single_filter(self._resources, callback)

    @property
    def resembles_resource(self):
        # Returns first resource resembling its source
        callback = lambda res: res.resembles
        return self._single_filter(self._resources, callback)

    @property
    def issues_resource(self):
        # Returns first resource with issues
        callback = lambda res: res.issues
        return self._single_filter(self._resources, callback)

    @property
    def success_resource(self):
        # Returns first success resource.
        callback = lambda res: res.success
        return self._single_filter(self._resources, callback)


class Master(Resources):
    # Master class for Resource classes.
    # Creates Resource instances on request and help in accessing them.
    # Internally creates instances as compared to parent class Resources.
    def __init__(self, source, *args, **kwargs):
        super().__init__(list())
        self._source = source
        self._args = args
        self._kwargs = kwargs
        # Calling object method within initialiser can cause problems.
        # Object not yet completely created.
        self._resource_types = resources_types.copy()
        # Updates resources instances as resources types(classes) changed.
        # set_resource_types() automatically does update resource objects.
        self.__update_resources()


    def set_resource_types(self, resource_types):
        # Sets resources types(classes) and updates instances.
        self._resource_types = resource_types
        self.__update_resources()

    def get_resources_types(self):
        return self._resource_types


    def __create_resources(self):
        # Creates resources objects for source using resources classes.
        def func(resource_type):
            return resource_type(self._source, *self._args, **self._kwargs)
        # Convert to list to avoid iterator from getting exausted.
        # That is common with python iterator
        return list(map(func, self._resource_types))

    def __update_resources(self):
        # Updates resource resources by creating new instances.
        self._resources = self.__create_resources()


if __name__ == "__main__":
    source = "file"
    master = Master(source)
    print(master.resembles_resource.uri_type)
    