from . import urlmod


WEB_URL_SCHEMES = {"http", "https", "ftp"}

def is_web_url(_source):
    # Checks if source is url for web resource
    return urlmod.is_url(_source, WEB_URL_SCHEMES)

def resembles_web_url(_source):
    return urlmod.resembles_url(_source, WEB_URL_SCHEMES)


if __name__ == "__main__":
    base_url = "https://parsy.readthedocs.io/en/latest/"
    print(is_web_url(base_url))
    print(resembles_web_url("http://172.18.128.1/"))
