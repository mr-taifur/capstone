import re
import os
import datetime

# Configuration
LOG_FILE = "security_violations.log"
MAX_CHAR_LIMIT = 500
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Prompt injection patterns (case-insensitive)
PROMPT_INJECTION_PATTERNS = [
    r"ignore (prior|previous|all) instructions",
    r"system override",
    r"you are now a(n)? dev",
    r"bypass safety",
    r"forget what we talked",
    r"new instructions:",
    r"act as",
    r"you must now output"
]

# Harmful/unsafe keywords for agricultural context
HARMFUL_KEYWORDS = [
    "anthrax",
    "biological weapon",
    "chemical weapon",
    "weaponize",
    "make poison",
    "sabotage crop",
    "destroy harvest",
    "kill plants",
    "steal data",
    "hack system"
]

def log_violation(reason: str, user_input: str):
    """Logs security violations to a local log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    truncated_input = user_input[:100] + ("..." if len(user_input) > 100 else "")
    log_entry = f"[{timestamp}] REJECTION: {reason} | Input: {truncated_input}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write security log: {e}")

def validate_text(text: str) -> tuple[bool, str]:
    """
    Validates user text prompt against security guardrails.
    Returns (is_safe, error_message).
    """
    if not text:
        return True, ""
        
    # 1. Length validation
    if len(text) > MAX_CHAR_LIMIT:
        reason = f"Input exceeds maximum character limit of {MAX_CHAR_LIMIT}"
        log_violation(reason, text)
        return False, reason
        
    # 2. Prompt injection detection
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            reason = f"Potential prompt injection detected (pattern: {pattern})"
            log_violation(reason, text)
            return False, "Input rejected due to security policy violations."
            
    # 3. Harmful keywords filtering
    for keyword in HARMFUL_KEYWORDS:
        if keyword in text.lower():
            reason = f"Harmful keyword detected: '{keyword}'"
            log_violation(reason, text)
            return False, "Input rejected due to safety policy violations."
            
    return True, ""

def validate_image_file(filename: str) -> tuple[bool, str]:
    """
    Validates if an uploaded image has a safe file extension.
    Returns (is_valid, error_message).
    """
    if not filename:
        return False, "No file uploaded."
        
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        reason = f"Invalid file extension: '{ext}'. Allowed: {list(ALLOWED_EXTENSIONS)}"
        log_violation(reason, filename)
        return False, reason
        
    return True, ""
