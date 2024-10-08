import threading
import time
import logging
from requester import deliver_the_strike
from logger import update_victory_status

# Create a barrier to synchronize threads
def prepare_the_routine(endpoints):
    barrier = threading.Barrier(len(endpoints) + 1)  # +1 for the main thread
    health_check_threads = []
    
    for endpoint in endpoints:
        disciple = threading.Thread(target=perform_check_loop, args=(endpoint, barrier))
        disciple.daemon = True  # Threads close when the main program exits
        health_check_threads.append(disciple)
        logging.info(f"Starting health check thread for {endpoint.get('url')}")
        disciple.start()

    return barrier

# Continuous loop that performs health checks on a single endpoint every 15 seconds
def perform_check_loop(endpoint, barrier):
    interval = 15
    while True:
        start_time = time.time()

        # Perform the health check and determine the status (UP or DOWN)
        perform_check(endpoint)

        # Wait for all threads to reach the barrier
        barrier.wait()

        # Sleep to maintain the fixed 15-second interval between checks
        elapsed_time = time.time() - start_time
        sleep_time = max(0, interval - elapsed_time)
        logging.debug(f"Sleeping for {sleep_time:.2f} seconds before the next check for {endpoint.get('url')}")
        time.sleep(sleep_time)

# Perform an HTTP health check and update the status of the endpoint
def perform_check(endpoint):
    url, response_code, latency = deliver_the_strike(endpoint)

    # An endpoint is UP if it returns a 2xx response code and responds within 500 ms
    if response_code is not None and 200 <= response_code < 300 and latency is not None and latency < 0.5:
        logging.info(f"{url} is UP (status: {response_code}, latency: {latency:.4f} seconds)")
        update_victory_status(url, True)
    else:
        # Handle case where latency or response code is None
        if latency is None:
            logging.warning(f"{url} is DOWN (status: {response_code}, latency: N/A)")
        else:
            logging.warning(f"{url} is DOWN (status: {response_code}, latency: {latency:.4f} seconds)")
        update_victory_status(url, False)
