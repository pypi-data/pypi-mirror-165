# Todo: TBD - REMOVE if not needed
DISCOVERY_ENDPOINTS = {
    "enterprise": "enterprise",
    "organization": "organization",
    "environment": "environment",
}


def map_resource_to_endpoint(command: str):
    sanitized_command = command.lower()

    try:
        endpoint = DISCOVERY_ENDPOINTS[sanitized_command]
    except KeyError as e:
        print(f"The resource '{sanitized_command}' was not found.")
        print("#######################################")
        print("available resources include:")
        for i in DISCOVERY_ENDPOINTS:
            print(i, end=" ")
            print()
        print("#######################################")
        raise e

    return endpoint
