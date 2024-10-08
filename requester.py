import urllib.request
import time
import logging

# Send an HTTP request to the specified endpoint and return the URL, response code, and latency
def deliver_the_strike(endpoint):
    method = endpoint.get("method", "GET")  # Default method is GET
    url = endpoint.get("url")
    headers = endpoint.get("headers", {})
    body = endpoint.get("body", None)

    # Construct the HTTP request
    request = urllib.request.Request(url, method=method, headers=headers)
    if body and method == "POST":
        body = body.encode("utf-8")
        request.data = body

    logging.debug(
        f"Sending {method} request to {url} with headers {headers} and body {body}"
    )

    # Measure request latency
    start_time = time.perf_counter()
    try:
        # Attempt to open the URL with a timeout of 500 ms
        with urllib.request.urlopen(request, timeout=1) as response:
            latency = time.perf_counter() - start_time
            response_code = response.getcode()
            logging.debug(
                f"Received response from {url} with status code {response_code} "
                f"in {latency:.4f} seconds"
            )
            return url, response_code, latency  # Return details of the request
    except Exception as e:
        logging.error(f"Error contacting {url}: {e}")
        return url, None, None  # None indicates a failed request
