def parse_time(time_str):
    """
    Converts a time string of the format "HH:MM:SS,ms" to total seconds as a float.
    """
    hours, minutes, seconds_ms = time_str.split(':')
    seconds, milliseconds = seconds_ms.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000.0
