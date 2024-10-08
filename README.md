# HTTP Endpoint Health Checker

This project implements a health check monitor for a set of HTTP endpoints. The program periodically tests the availability of specified endpoints, logs the results, and reports the availability percentage for each domain.

## Features
- Monitors multiple HTTP endpoints in parallel.
- Logs the availability of each endpoint every 15 seconds.
- Provides detailed logging on the status of each request, including response codes and latencies.
- Displays the cumulative availability percentage for each domain after each test cycle.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration File](#configuration-file)
- [Running the Program](#running-the-program)
- [Output](#output)
- [Notes](#notes)
- [License](#license)

## Requirements

The project uses **Python 3.x**. Please ensure Python is installed on your system before proceeding.

To verify Python is installed, run:

    python3 --version

If Python is not installed, you can download and install it from [python.org](https://www.python.org/downloads/).

## Installation

No external dependencies are required, as the project only uses Python's standard libraries. You can simply clone the repository and run the program.

### Steps:

    # Clone the repository to your local machine:
    git clone <repository_url>
    cd <repository_folder>

## Usage

To run the health check monitor, you need to pass a configuration file containing the HTTP endpoints you wish to monitor. The configuration file must be in **YAML** format.

### Configuration File

    - name: Example GET request
      method: GET
      url: https://example.com
      headers:
        user-agent: health-checker

    - name: Example POST request
      method: POST
      url: https://example.com/api
      headers:
        content-type: application/json
      body: '{"key":"value"}'

    - name: Subdomain request
      method: GET
      url: https://sub.example.com

- **name** (string, required): A descriptive name for the endpoint.
- **url** (string, required): The URL of the endpoint.
- **method** (string, optional): The HTTP method (GET, POST, etc.). Defaults to GET if not provided.
- **headers** (dictionary, optional): HTTP headers to include with the request.
- **body** (string, optional): A JSON-encoded body to include with POST requests.

## Running the Program

To run the program, use the following command:

    python health_checker.py <path_to_configuration_file>

### Command-Line Arguments:

- `<path_to_configuration_file>`: The path to your YAML configuration file.
- `--enable-logging`: An optional flag to enable detailed logging for debugging.

### Example with logging:

    python health_checker.py /path/to/endpoints.yaml --enable-logging

By default, the program will only log the **availability percentage** for each domain after each test cycle. Use the `--enable-logging` flag to see more detailed information (e.g., "is UP" and "is DOWN" messages for each endpoint).

## Output

The program will log the status of each endpoint and display the availability percentage of each domain every 15 seconds.

### Example output (with logging enabled):

    2024-10-08 14:35:04,697 - INFO - https://example.com is UP (status: 200, latency: 0.1197 seconds)
    2024-10-08 14:35:04,861 - INFO - https://sub.example.com is UP (status: 200, latency: 0.2830 seconds)
    2024-10-08 14:35:05,010 - WARNING - https://example.com/api is DOWN (status: 500, latency: 0.5678 seconds)
    example.com has 50% availability percentage
    sub.example.com has 100% availability percentage

### Example output (without logging enabled):

    example.com has 50% availability percentage
    sub.example.com has 100% availability percentage

## Notes

- The health checks run indefinitely until you manually stop the program using **Ctrl+C**.
- Availability is calculated as the percentage of successful (UP) checks over the total number of checks performed.

## License

This project is licensed under the MIT License.
