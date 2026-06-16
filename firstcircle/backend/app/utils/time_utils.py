from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def parse_iso_datetime(dt_str: str) -> datetime:
    """
    Parses ISO 8601 strings into datetime objects.
    """
    # Remove Z flag or timezone offsets for simple local parsing if needed
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1]
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
