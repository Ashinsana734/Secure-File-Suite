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
    """Verifies user credentials and returns (status, failed_attempts)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash, is_locked, failed_attempts FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            return False, 0
            
        stored_hash, is_locked, failed_attempts = user
        
        # දැනටමත් ලොක් වෙලා නම් කෙලින්ම ලොක් කියලා කියනවා
        if is_locked == 1:
            return False, failed_attempts
            
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            cursor.execute('UPDATE users SET failed_attempts = 0 WHERE username = ?', (username,))
            cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "USER_LOGIN", "Successful login."))
            conn.commit()
            conn.close()
            log_to_file(username, "USER_LOGIN", "Successful login.")
            return True, 0
        else:
            failed_attempts += 1
            if failed_attempts >= 5:
                cursor.execute('UPDATE users SET failed_attempts = ?, is_locked = 1 WHERE username = ?', (failed_attempts, username))
                cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "ACCOUNT_LOCKOUT", "Account locked."))
                conn.commit()
                conn.close()
                log_to_file(username, "ACCOUNT_LOCKOUT", "Account locked due to failed attempts.")
                return False, failed_attempts
            else:
                cursor.execute('UPDATE users SET failed_attempts = ? WHERE username = ?', (failed_attempts, username))
                cursor.execute('INSERT INTO audit_logs (username, action, details) VALUES (?, ?, ?)', (username, "LOGIN_FAILED", f"Attempt {failed_attempts}"))
                conn.commit()
                conn.close()
                log_to_file(username, "LOGIN_FAILED", f"Failed attempt {failed_attempts}.")
                return False, failed_attempts
    except Exception as e:
        return False, 0