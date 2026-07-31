import math
import re

RIAL_TO_TOOMAN = 10
_MARKDOWN_LINK_RE = re.compile(r"^\[.*?]\((.*?)\)$")

def rial_to_tooman(rial: int | float) -> int:
    """
    Convert Rial to Tooman.
    Digikala API returns prices in Rial.
    MCP tools expose prices in Tooman.
    """
    if rial is None:
        return 0
    return math.floor(float(rial) / RIAL_TO_TOOMAN)

def tooman_to_rial(tooman: int | float) -> int:
    """
    Convert Tooman to Rial.
    """
    if tooman is None:
        return 0
    return int(float(tooman) * RIAL_TO_TOOMAN)

def to_safe_int(value) -> int:
    """
    Safely convert arbitrary values to integer.
    """
    try:
        if value is None:
            return 0

        return math.floor(float(value))
    except (TypeError, ValueError):
        return 0

def extract_plain_url(url: str | None) -> str:
    """
    Convert markdown links into plain URLs.
    """
    if not url:
        return ""
    match = _MARKDOWN_LINK_RE.match(url)
    if match:
        return match.group(1)
    return url

def ensure_trailing_slash(url: str | None) -> str:
    """
    Ensure Digikala URLs end with '/' before
    query parameters or fragments.
    """
    if not url:
        return ""
    if "#" in url:
        path, fragment = url.split("#", 1)
        return path.rstrip("/") + "/#" + fragment
    if "?" in url:
        path, query = url.split("?", 1)
        return path.rstrip("/") + "/?" + query
    return url.rstrip("/") + "/"
