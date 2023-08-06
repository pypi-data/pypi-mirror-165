from . import exceptions

import socket
from urllib import parse


LOCAL_HOST_NAMES = {"localhost", "127.0.0.1"}

# url parsing functions
def urlparse(url):
    return parse.urlparse(url)

def urlparse_dict(url):
    return urlparse(url)._asdict()

def url_unparse(url):
    return parse.urlparse(url)._asdict()

def urljoin(base_url, url):
    return parse.urljoin(base_url, url)

def quote(url, *args, **kwargs):
    return parse.quote(url, *args, **kwargs)

def unquote(url, *args, **kwargs):
    return parse.unquote(url, *args, **kwargs)


# Functions for extracting parts of url
def extract_path(url: str):
    # Extracts path part of url
    return parse.urlparse(url).path

def extract_hostname(url: str):
    # Extracts hostname part of url
    return parse.urlparse(url).hostname

def extract_netloc(url: str):
    # Extracts netloc part of url
    return parse.urlparse(url).netloc

def extract_scheme(url: str):
    # Extracts scheme of url
    return parse.urlparse(url).scheme

def extract_params(url: str):
    # Extracts parameter passed to url
    return parse.urlparse(url).params

def extract_query(url: str):
    return parse.urlparse(url).query

def extract_port(url: str):
    port = parse.urlparse(url).port
    if port == None:
        return ""
    else:
        return str(port)

def extract_fragment(url: str):
    return parse.urlparse(url).fragment


# # Functions for validationg url
# def is_file_path_scheme(scheme):
#     # Checks if chememe is that of file path.
#     # credit: https://stackoverflow.com/questions/29026051
#     return os.path.exists(scheme + ":\\")


def is_url(_source, schemes=None):
    # Checks if source is url for web resource.
    if isinstance(_source, (str, bytes)):
        scheme = extract_scheme(_source)
        netloc = extract_netloc(_source)
        path = extract_path(_source)
        any_items = (netloc, path)
        if schemes != None:
            return scheme in schemes and any(any_items)
        else:
            return bool((scheme)) and any(any_items)
    return False

def resembles_scheme(_url, scheme):
    # Checks if url resembles containing scheme
    # It does not mean that scheme is real scheme of url.
    url_scheme = extract_scheme(_url)
    if scheme != None:
        return scheme == url_scheme
    else:
        return bool(url_scheme)
        


def resembles_hostname(_url, hostname):
    # Checks if url resembles containing hostname
    url_hostname = extract_hostname(_url)
    if hostname != None:
        return url_hostname == hostname
    else:
        return bool(url_hostname)

def resembles_schemes(_url, schemes):
    # Checks if url resembles containing schemes
    for scheme in schemes:
        if resembles_scheme(_url, scheme):
            return True
    return False

def resembles_url(_source, schemes=None):
    # Checks if source resembles url.
    # 1. source should 2 of any of url parts excluding path and hostname.
    # 2. Or source should have scheme(or resemble) and path.
    # 2. Or source should have atleast hostname.
    if isinstance(_source, (str, bytes)):
        if schemes != None:
            # URL needs to have atleast one of provided schemes
            scheme_satisfied = resembles_schemes(_source, schemes)
        else:
            # Dont care if url has scheme if schemes not provided
            scheme_satisfied = True

        if scheme_satisfied and resembles_hostname(_source, None):
            # Hostname is enough to satify url
            return True
        elif scheme_satisfied and extract_path(_source):
            # scheme and path satisfies url
            return True
        else:
            # source satifying scheme and atleast 2 other parts of url
            # can be considered resembling url.
            any_items = [
                extract_query(_source),
                extract_params(_source),
                extract_port(_source),
                extract_fragment(_source)
            ]
            any_items_filtered = list(filter(None, any_items))
            return scheme_satisfied and len(any_items_filtered) >= 2
    return False


# Functions for transforming url
def make_url_absolute(url:str, base_url:str):
    # Makes url absolute by adding missing parts from base_url
    # inspired by: requests-html requests_html.BaseParse._make_absolute()

    # Parse url componets into dictionary
    parsed = urlparse(url)._asdict()

    # url almost complete but missing scheme
    if url.startswith("//"):
        parsed['scheme'] = urlparse(base_url).scheme

        # Recreates url with new scheme
        parsed = [value for value in parsed.values()]
        return url_unparse(parsed)

    # Link is absolute; its just missing scheme and netloc
    elif url.startswith("/"):
        parsed['scheme'] = urlparse(base_url).scheme
        parsed['netloc'] = urlparse(base_url).netloc

        # Recreates url with new scheme and netloc
        parsed = [value for value in parsed.values()]
        return url_unparse(parsed)

    # The link is relative to current url
    elif not parsed['netloc']:
        # parse.urljoin() is intelligent than os.path.join()
        return urljoin(base_url, url)
    
    # URL is complete and should have everything
    elif is_url(url):
        return url
    else:
        raise exceptions.InvalidURLError(url + " is not a valid url")



# Functions relating to IP addresses
def _get_local_adress():
    # Gets ip adress of local machine
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def _get_local_ip_adresses():
    # Gets ip adresses of local machine.
    # Functions is not reliable and shouldnt be depended.
    # source: https://stackoverflow.com/questions/270745/
    addreses = set()
    for info in socket.getaddrinfo(socket.gethostname(), None):
        addreses.add(info[4][0])
    return addreses

def is_local_ip_address(ip_address):
    # Checks if url is built on local ip address.
    # Not reliable function.
    return ip_address in _get_local_ip_adresses()


# Functions for checking if url is hosted locally or remotely
def is_local_host(hostname):
    # Checks hostname identifies this machine e.g localhost
    # Not reliable function.
    return hostname in LOCAL_HOST_NAMES

def is_remote_host(hostname):
    # Checks if host is remote host e.g example.com
    return not is_local_host(hostname)

def is_locally_hosted(_url):
    # Checks if url is served by local machine.
    # Functions is not reliable and shouldnt be depended.
    hostname = extract_hostname(_url)
    if hostname:
        return is_local_host(hostname) or is_local_ip_address(hostname)
    else:
        return True

def is_remotely_hosted(_url):
    # Checks if url is served by remote machine.
    # Functions is not reliable and shouldnt be depended.
    return not is_locally_hosted(_url)


if __name__ == "__main__":
    base_url = "parsy.readthedocs.io/en/latest?name#10/name"
    relative_url = "tutorial.html"
    print(resembles_url(base_url, None))
    print(make_url_absolute(base_url, base_url))