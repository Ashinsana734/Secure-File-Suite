import re
import os
from datetime import datetime

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "audit_log.txt")

def check_password_strength(password):
    """
    Checks if the password meets enterprise security standards:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character (@, $, !, %, *, ?, &)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long!"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter!"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter!"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit!"
    if not re.search(r"[@$!%*?&]", password):
        return False, "Password must contain at least one special character (@$!%*?&)."
    
    return True, "Strong password!"

def log_to_file(username, action, details):
    """Writes system audit logs into a text file inside the logs/ folder."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] User: {username} | Action: {action} | Details: {details}\n"
        
        # Append the log message to the text file
        with open(LOG_FILE_PATH, "a") as f:
            f.write(log_message)
    except Exception as e:
        print(f"Failed to write log to file: {e}")