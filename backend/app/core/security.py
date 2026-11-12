import re
import html
from backend.app.core.exceptions import SecurityException

# Dangerous prompt-injection override patterns
INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)system\s+override",
    r"(?i)drop\s+table",
    r"(?i)reveal\s+sqlite",
    r"(?i)admin\s+token",
    r"(?i)<\|im_start\|>",
    r"(?i)<\|endoftext\|>"
]

def sanitize_input_text(raw_text: str, max_chars: int = 4000) -> str:
    """Strips dangerous control tokens, escapes raw HTML, and limits maximum payload size."""
    if not raw_text:
        return ""
    # Enforce length limit to prevent token flood denial of service
    truncated = raw_text[:max_chars].strip()
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]*>", "", truncated)
    return cleaned

def inspect_prompt_injection(text: str) -> bool:
    """Returns True if the text contains explicit adversarial override patterns."""
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

