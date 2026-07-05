import os
import hashlib
from cryptography.fernet import Fernet

def generate_aes_key():
    """Generates a new AES-256 (Fernet) key."""
    return Fernet.generate_key()

def calculate_sha256(file_path):
    """Calculates the SHA-256 hash of a file to ensure integrity."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files smoothly
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def encrypt_file(file_path, key):
    """Encrypts a file using the provided AES key."""
    try:
        fernet = Fernet(key)
        
        # Read the original file data
        with open(file_path, "rb") as f:
            file_data = f.read()
            
        # Encrypt the data
        encrypted_data = fernet.encrypt(file_data)
        
        # Overwrite the file with encrypted data
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
            
        print(f"File '{os.path.basename(file_path)}' encrypted successfully!")
        return True
    except Exception as e:
        print(f"Encryption failed: {e}")
        return False

def decrypt_file(file_path, key):
    """Decrypts an encrypted file using the provided AES key."""
    try:
        fernet = Fernet(key)
        
        # Read the encrypted file data
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
            
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Restore the original file data
        with open(file_path, "wb") as f:
            f.write(decrypted_data)
            
        print(f"File '{os.path.basename(file_path)}' decrypted successfully!")
        return True
    except Exception as e:
        print(f"Decryption failed: {e}. Invalid key or corrupted file.")
        return False

if __name__ == "__main__":
    # Test Cryptography Setup
    print("--- Testing Cryptography Core ---")
    
    # 1. Create a dummy text file to test
    test_file = "test_document.txt"
    with open(test_file, "w") as f:
        f.write("Hello Machan! This is a top-secret message.")
        
    print(f"Created a dummy file: {test_file}")
    
    # 2. Generate Key and Calculate original SHA-256
    aes_key = generate_aes_key()
    original_hash = calculate_sha256(test_file)
    print(f"Original File SHA-256: {original_hash}")
    
    # 3. Test Encryption
    print("\nEncrypting file...")
    encrypt_file(test_file, aes_key)
    
    # 4. Test Decryption
    print("\nDecrypting file...")
    decrypt_file(test_file, aes_key)
    
    # 5. Verify Integrity
    decrypted_hash = calculate_sha256(test_file)
    print(f"Decrypted File SHA-256: {decrypted_hash}")
    
    if original_hash == decrypted_hash:
        print("\nSuccess: Integrity verified! The file contents are perfectly intact.")
    else:
        print("\nError: Integrity check failed!")
        
    # Clean up the test file
    if os.path.exists(test_file):
        os.remove(test_file)