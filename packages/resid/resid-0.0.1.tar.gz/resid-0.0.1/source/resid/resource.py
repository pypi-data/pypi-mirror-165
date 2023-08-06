from . import exceptions


class Resource(): 
    # Base class for analysing source for information like content type.
    # Most of attributes can be accessed as properties.
    # It contains properties for determining if source is supported,
    # located locally and others.
    # This is the most important class in this library.
    _uri_type = None

    def __init__(self, source, content_type:str=None, encoding:str=None):
        self._source = source
        self._content_type = content_type
        self._encoding = encoding


    def _validate_source(self):
        # Raises exception when source is not supported
        if not self.source_supported(self._source):
            err_msg = "Source '{}' is not supported for {}"
            err_msg = err_msg.format(
                self.uri[:20], 
                type(self)
            )
            raise exceptions.UnsupportedSourceError(err_msg)

    def source_supported(self, source):
        # Checks if source is supported
        # Any object is supported and can be used as source.
        # No source is supported for now.
        return False

    def to_string(self):
        # Returns string version of source
        return ""

    def to_dict(self):
        return {
            "uri": self.uri,
            "uri_type": self.uri_type,
            "content_type": self.content_type,
            "encoding": self.encoding,
            "supported": self.supported,
            "resembles": self.resembles,
            "available_localy": self.locally,
            "issues": self.issues,
            "status": self.status
        }

    def available_locally(self, source):
        # Checks if source data is available on this local machine
        return False

    def source_resembles(self, source):
        # Returns True if source is likely to be supported.
        # That does not mean source is supported.
        return self.source_supported(source)

    @property
    def supported(self):
        return self.source_supported(self._source)

    @property
    def resembles(self):
        return self.source_resembles(self._source)

    @property
    def issues(self):
        return not (self.supported or self.resembles)

    @property
    def success(self):
        return not self.issues

    @property
    def status(self):
        if self.supported:
            return "OK"
        elif self.source_resembles(self._source):
            return "Not Supported(resembles)"
        else:
            return "Not Supported(critically!!)"

    @property
    def locally(self):
        return self.available_locally(self._source)

    @property
    def remotely(self):
        return not self.available_locally(self._source)

    @property
    def uri(self):
        return self.to_string()

    @property
    def uri_type(self):
        return self._uri_type

    @property
    def summary(self):
        return self.to_dict()
    
    @property
    def source(self):
        return self._source

    @property
    def content_type(self):
        return self._content_type

    @property
    def encoding(self):
        return self._encoding


class Generic(Resource):
    # This sources that are generic but useful.
    # This can include path which can be dir path or url path.
    # Or url which can be web url, local file url, etc.
    # Sources for in this class do
    def source_supported(self, source):
        # Does not need to be supported as its too generic
        return False

    @property
    def supported(self):
        # Does not need to be supported as its too generic
        return False
