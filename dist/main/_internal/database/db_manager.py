import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "secure_suite.db")

def init_db():
    """Initializes the database and creates the required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Users Table (Stores user credentials and account status)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            failed_attempts INTEGER DEFAULT 0,
            is_locked INTEGER DEFAULT 0
        )
    ''')
    
    # 2. Audit Logs Table (Tracks system events and user actions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            username TEXT,
            action TEXT NOT NULL,
            details TEXT
        )
    ''')
    
    # 3. Encrypted Files Table (Stores metadata of encrypted files)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encrypted_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            sha256_hash TEXT NOT NULL,
            encryption_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and tables initialized successfully!")

if __name__ == "__main__":
    init_db()