# Parse the YAML configuration file and extract endpoint definitions as dictionaries
def unroll_training_manual(file_path):
    training_manual = []

    with open(file_path, "r") as f:
        endpoint = {}
        for line in f:
            line = line.strip()

            # Start a new endpoint when a list item is encountered (denoted by '-')
            if line.startswith("-"):
                if endpoint:
                    training_manual.append(endpoint)
                endpoint = {}
            elif ": " in line:
                # Split the line into key-value pairs for endpoint attributes
                key, value = line.split(": ", 1)
                endpoint[key] = value
        # Add the last parsed endpoint if it exists
        if endpoint:
            training_manual.append(endpoint)

    return training_manual
