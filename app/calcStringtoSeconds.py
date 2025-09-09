def convert_to_seconds(time_str):
    """Convert a time string like '2h', '3D', or '1w' to seconds.
    If input is invalid, defaults to 1 hour (3600 seconds).
    """
    time_str = time_str.strip()
    if not time_str:
        print("Warning: Empty input. Defaulting to 1 hour.")
        return 3600

    unit = time_str[-1]
    try:
        value = int(time_str[:-1])
    except ValueError:
        print(f"Warning: Invalid number in '{time_str}'. Defaulting to 1 hour.")
        return 3600

    if unit == 'H':
        return value * 3600
    elif unit == 'D':
        return value * 86400
    elif unit == 'W':
        return value * 604800
    else:
        print(f"Warning: Unsupported time unit '{unit}' in '{time_str}'. Defaulting to 1 hour.")
        return 3600


