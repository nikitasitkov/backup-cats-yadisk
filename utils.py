import re
from urllib.parse import quote


INVALID_FILENAME_CHARS = r'\\/:*?"<>|'


def sanitize_filename(text: str, default: str = "cat") -> str:
    if text is None:
        return default

    cleaned = text.strip()
    if not cleaned:
        return default

    cleaned = re.sub(f"[{re.escape(INVALID_FILENAME_CHARS)}]", "_", cleaned)

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned or default


def sanitize_user_text(value: str) -> str:
    if value is None:
        return ""

    value = value.strip()

    value = value.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    return value


def url_encode_path_part(value: str) -> str:
    return quote(value, safe="")