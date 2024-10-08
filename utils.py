from urllib.parse import urlparse

# Extract the domain (dojo) from a URL
def locate_dojo(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Return the domain
