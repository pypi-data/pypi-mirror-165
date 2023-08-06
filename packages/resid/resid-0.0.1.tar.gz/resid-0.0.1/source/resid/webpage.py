from . import filepath
from . import weburl
from . import urlmod

def is_webpage(_source):
    # Checks if source is points to webpage
    if weburl.is_web_url(_source):
        path = urlmod.extract_path(_source)
        if path:
            if filepath.extract_extension(path):
                # url resembling html is likely webpage
                # e.g https://www.example.com/sample.html
                return filepath.is_html_file(path)
            else:
                # url has path part but less likely to be a file.
                # e.g https://www.example.com/page
                return True
        else:
            # No path part means its likely webpage.
            # e.g https://www.example.com/
            return True
    else:
        return False
        