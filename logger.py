from utils import locate_dojo
import logging

# Dictionary to store the availability status of each domain
dojo_status = {}

# Update the availability status (UP or DOWN) for each endpoint
def update_victory_status(url, is_up):
    dojo = locate_dojo(url)
    if dojo not in dojo_status:
        dojo_status[dojo] = {"total_requests": 0, "up_requests": 0}

    # Increment total requests and UP requests
    dojo_status[dojo]["total_requests"] += 1
    if is_up:
        dojo_status[dojo]["up_requests"] += 1

# Calculate and log the availability percentage for each domain
def record_victory_status():
    for dojo, data in dojo_status.items():
        if data["total_requests"] == 0:
            availability = 0
        else:
            # Calculate availability as a percentage (UP requests / total requests)
            availability = round(100 * (data["up_requests"] / data["total_requests"]))
        print(f"{dojo} has {availability}% availability percentage")
