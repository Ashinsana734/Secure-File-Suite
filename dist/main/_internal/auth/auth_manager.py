import sqlite3
import os
import bcrypt
from datetime import datetime

# Paths for the database and log file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "secure_suite.db")
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "audit_log.txt")

def log_to_file(username, action, details):
    """Writes system audit logs into a text file inside the logs/ folder."""
    try:
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] User: {username} | Action: {action} | Details: {details}\n"
        
        with open(LOG_FILE_PATH, "a") as f:
            f.write(log_message)
    except Exception as e:
        print(f"Failed to write log to file: {e}")

def register_user(username, password):
    """Registers a new user, hashes the password, and logs the action."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "USER_REGISTRATION", "User registered successfully."))
        conn.commit()
        conn.close()
        
        log_to_file(username, "USER_REGISTRATION", "User registered successfully.")
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        return False

def login_user(username, password):
    """Verifies user credentials, handles lockouts after 5 failed attempts, and returns detailed status."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash, is_locked, failed_attempts FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            return "INVALID" # User නැත්නම් සාමාන්‍ය වැරදි මැසේජ් එකක්
            
        stored_hash, is_locked, failed_attempts = user
        
        # එකවුන්ට් එක දැනටමත් ලොක් නම් කෙලින්ම LOCKED කියලා යවනවා
        if is_locked == 1:
            return "LOCKED"
            
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            cursor.execute('UPDATE users SET failed_attempts = 0 WHERE username = ?', (username,))
            cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "USER_LOGIN", "Successful login."))
            conn.commit()
            conn.close()
            log_to_file(username, "USER_LOGIN", "Successful login.")
            return "SUCCESS" # ලොගින් සාර්ථකයි
        else:
            failed_attempts += 1
            if failed_attempts >= 5:
                # 5 වෙනි පාර වැරදුණු සැනින් ඩේටාබේස් එකේ ලොක් කරනවා
                cursor.execute('UPDATE users SET failed_attempts = ?, is_locked = 1 WHERE username = ?', (failed_attempts, username))
                cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "ACCOUNT_LOCKOUT", "Account locked."))
                conn.commit()
                conn.close()
                log_to_file(username, "ACCOUNT_LOCKOUT", "Account locked due to failed attempts.")
                return "JUST_LOCKED" # දැන්ම ලොක් වුණා කියලා කියනවා
            else:
                cursor.execute('UPDATE users SET failed_attempts = ? WHERE username = ?', (failed_attempts, username))
                cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "LOGIN_FAILED", f"Attempt {failed_attempts}"))
                conn.commit()
                conn.close()
                log_to_file(username, "LOGIN_FAILED", f"Failed attempt {failed_attempts}.")
                return "INVALID" # තවම පාරවල් තියෙනවා, සාමාන්‍ය වැරදි මැසේජ් එකක්
    except Exception as e:
        return "ERROR"