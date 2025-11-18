"""Utility functions for the application."""

import re
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    """Sanitize string input by removing special characters and trimming."""
    if not isinstance(value, str):
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = value.strip()
    
    # Remove multiple spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Truncate if max_length specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, remove diacritics)."""
    if not isinstance(text, str):
        return ""
    
    text = text.lower().strip()
    
    # Simple diacritic removal for French characters
    diacritic_map = {
        'à': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
        'ñ': 'n'
    }
    
    for char, replacement in diacritic_map.items():
        text = text.replace(char, replacement)
    
    return text


def generate_hash(data: str) -> str:
    """Generate SHA256 hash of data."""
    return hashlib.sha256(data.encode()).hexdigest()


def format_currency(value: float, currency: str = "CAD") -> str:
    """Format float as currency string."""
    if currency == "CAD":
        return f"${value:,.2f}"
    elif currency == "USD":
        return f"US${value:,.2f}"
    else:
        return f"{value:,.2f}"


def parse_csv_line(line: str) -> List[str]:
    """Parse CSV line into list of values."""
    if not isinstance(line, str):
        return []
    
    values = []
    current = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            values.append(current.strip())
            current = ""
        else:
            current += char
    
    values.append(current.strip())
    return values


def dict_to_query_string(params: Dict[str, Any]) -> str:
    """Convert dictionary to URL query string."""
    if not isinstance(params, dict):
        return ""
    
    pairs = []
    for key, value in params.items():
        if value is not None:
            pairs.append(f"{key}={value}")
    
    return "&".join(pairs)


def chunk_list(items: List, chunk_size: int) -> List[List]:
    """Split list into chunks of specified size."""
    if not isinstance(items, list) or chunk_size <= 0:
        return []
    
    chunks = []
    for i in range(0, len(items), chunk_size):
        chunks.append(items[i:i + chunk_size])
    
    return chunks


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


def safe_get(data: Dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with default fallback."""
    if not isinstance(data, dict):
        return default
    
    return data.get(key, default)


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries, with dict2 values taking precedence."""
    if not isinstance(dict1, dict):
        dict1 = {}
    if not isinstance(dict2, dict):
        dict2 = {}
    
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def filter_dict(data: Dict, keys: List[str]) -> Dict:
    """Filter dictionary to only include specified keys."""
    if not isinstance(data, dict):
        return {}
    
    if not isinstance(keys, list):
        return {}
    
    return {key: data[key] for key in keys if key in data}


def log_performance(func_name: str, duration_ms: float, threshold_ms: float = 1000):
    """Log function performance if exceeds threshold."""
    if duration_ms > threshold_ms:
        logger.warning(
            f"Performance: {func_name} took {duration_ms:.2f}ms (threshold: {threshold_ms}ms)"
        )
    else:
        logger.debug(f"Performance: {func_name} took {duration_ms:.2f}ms")


def is_valid_email(email: str) -> bool:
    """Validate email address format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return isinstance(email, str) and bool(re.match(email_pattern, email))


def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    url_pattern = r'^https?://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?$'
    return isinstance(url, str) and bool(re.match(url_pattern, url))
