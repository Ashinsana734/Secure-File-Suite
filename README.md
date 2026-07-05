🔐 Secure File Encryption Suite

An enterprise-style desktop application designed to protect sensitive files using modern cryptography. It demonstrates secure software development, robust authentication mechanisms, auditing, and practical cybersecurity concepts, making it a high-quality portfolio project.

✨ Core Features

🔐 Advanced Authentication & RBAC:

User Registration & Login with Password Hashing & Strength Checker.

Security-first Account Lockout mechanism (Locks automatically after 5 failed attempts).

Role-Based Access Control (RBAC) to enforce least privilege.

🛡️ Military-Grade Cryptography:

AES-256 Encryption: To encrypt and decrypt any file type securely.

RSA Key Protection: Secure asymmetrical key management.

SHA-256 Integrity Verification: Ensures files are not tampered with.

📊 Monitoring & Database Management:

Built-in SQLite Database to manage user and file metadata securely.

Comprehensive Audit Logs and Encryption History with an option to Export Logs.

🎨 User Experience & Architecture:

Modern, eye-friendly Dark Mode GUI.

Enterprise-grade Exception Handling to prevent crashes and resource leaks.

⚙️ Workflow

Register/Login ➡️ Validate Password ➡️ Lockout Rule (5 Failures max) ➡️ Select File ➡️ AES-256 Encryption ➡️ RSA Key Protection ➡️ SHA-256 Verification ➡️ Store Metadata ➡️ Audit Log ➡️ Secure Decryption



📸 Screenshots

| Login Screen | Dashboard |
|  |  |

🛠️ Built With (Tech Stack)

Language: Python

GUI Framework: Custom Tkinter / Tkinter

Cryptography: Cryptography (Fernet standard), RSA, SHA-256

Database: SQLite

Core Modules: Logging, JSON, OOP Concepts

📂 Project Structure

├── app/
├── auth/
├── crypto/
├── database/
├── gui/
├── logs/
├── reports/
├── utils/
├── assets/
└── main.py



Database Schema Includes:

Users, Roles, Encrypted Files, AuditLogs, LoginAttempts, Settings

🔒 Implemented Security Practices

Secure Key Management & Input Validation.

Principle of Least Privilege & Integrity Verification.

Fail-safe Exception Handling & Continuous Audit Logging.

🚀 Future Roadmap

$$$$

 Multi-Factor Authentication (MFA) & Biometric Login

$$$$

 Cloud Backup integration & Cloud Key Management Service (KMS)

$$$$

 Digital Signatures & Email Alert system

$$$$

 Exposing core functionalities via a REST API