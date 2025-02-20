import re
import opheliaNeurals as opheNeu


BLACKLISTED_KEYWORDS = [
    r"\bimport\b", r"\bexec\b", r"\beval\b", r"\bsystem\(", r"\bos\.",  # Matches function calls
    r"\bsubprocess\.", r"\brm\s+-rf\b", r"\brmdir\b", r"\bdel\b",  # Matches dangerous shell commands
    r"\bopen\(", r"\bwrite\(", r"\bread\(", r"\bchmod\b", r"\bchown\b",  # Matches file system access
]


def sanitizeText(text):
    for keyword in BLACKLISTED_KEYWORDS:
        if re.search(keyword, text, re.IGNORECASE):
            log_message = f"Blocked potentially dangerous input: {text}"
            if "subprocess" in keyword or "exec" in keyword:  # Extremely dangerous
                opheNeu.logging.critical(log_message)
            else:
                opheNeu.logging.warning(log_message)
            return None
    return text

