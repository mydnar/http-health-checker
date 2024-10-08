import time
import argparse
import logging
from config_parser import unroll_training_manual
from scheduler import prepare_the_routine
from logger import record_victory_status

# Configure logging; disabled by default but can be enabled with --enable-logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    parser = argparse.ArgumentParser(description="Monitor HTTP endpoints for availability.")
    
    # Required argument for the YAML configuration file
    parser.add_argument("file_path", type=str, help="Path to the YAML configuration file.")
    
    # Optional argument to enable logging
    parser.add_argument(
        "--enable-logging",
        action="store_true",  # If provided, this will set enable_logging to True
        help="Enable logging for debugging purposes."
    )
    
    args = parser.parse_args()

    # Disable logging by default unless --enable-logging is passed
    if not args.enable_logging:
        logging.disable(logging.CRITICAL)
    
    # Indicate that the program is starting
    print("Starting HTTP endpoint health checker")

    logging.info(f"Reading configuration from {args.file_path}")
    training_manual = unroll_training_manual(args.file_path)

    # Start health check threads and get the barrier object
    logging.info("Starting health check threads for each endpoint")
    barrier = prepare_the_routine(training_manual)

    # Main loop to log availability status every 15 seconds
    interval = 15
    while True:
        start_time = time.time()

        # Wait for all health checks to complete
        barrier.wait()  # Synchronize with health check threads

        # Log the availability status after each cycle
        record_victory_status()

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Sleep to ensure the next test cycle starts exactly 15 seconds after the previous cycle
        sleep_time = max(0, interval - elapsed_time)
        time.sleep(sleep_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Monitoring terminated by user.")
