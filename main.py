import customtkinter as ctk
from tkinter import filedialog
import os
import re
from auth.auth_manager import register_user, login_user
from crypto.crypto_manager import generate_aes_key, encrypt_file, decrypt_file, calculate_sha256

def check_password_strength(password):
    """Validates password strength according to enterprise security standards."""
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

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SecureFileApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Secure File Encryption Suite")
        self.geometry("500x450")
        self.resizable(False, False)
        
        self.current_user = None
        self.session_key = generate_aes_key() 
        
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        
        title_label = ctk.CTkLabel(self, text="Secure Login", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(40, 20))
        
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack(pady=5)
        
        login_btn = ctk.CTkButton(self, text="Login", width=300, command=self.handle_login)
        login_btn.pack(pady=10)
        
        register_link = ctk.CTkButton(self, text="Don't have an account? Register", fg_color="transparent", text_color="gray", command=self.show_register_screen)
        register_link.pack(pady=10)

    def show_register_screen(self):
        self.clear_screen()
        
        title_label = ctk.CTkLabel(self, text="Create Account", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(40, 20))
        
        self.reg_username_entry = ctk.CTkEntry(self, placeholder_text="Choose Username", width=300)
        self.reg_username_entry.pack(pady=10)
        
        self.reg_password_entry = ctk.CTkEntry(self, placeholder_text="Choose Password", show="*", width=300)
        self.reg_password_entry.pack(pady=10)
        
        self.reg_status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.reg_status_label.pack(pady=5)
        
        register_btn = ctk.CTkButton(self, text="Register", width=300, fg_color="green", hover_color="darkgreen", command=self.handle_register)
        register_btn.pack(pady=10)
        
        login_link = ctk.CTkButton(self, text="Already have an account? Login", fg_color="transparent", text_color="gray", command=self.show_login_screen)
        login_link.pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # ටියුපල් එකක් විදිහට ප්‍රතිඵලය ගන්නවා (Success status, failed attempts)
        is_success, attempts = login_user(username, password)
        
        if is_success:
            self.current_user = username
            self.show_dashboard()
        else:
            if attempts >= 5:
                # පාරවල් 5 හෝ ඊට වැඩි නම් එකවුන්ට් එක ලොක්
                self.status_label.configure(text="Account Locked! Too many failed attempts.", text_color="red")
            else:
                # පාරවල් 5ට වඩා අඩු නම් සාමාන්‍ය වැරදි මැසේජ් එක
                self.status_label.configure(text="Invalid credentials!", text_color="orange")

    def handle_register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        
        if not username or not password:
            self.reg_status_label.configure(text="Fields cannot be empty!", text_color="red")
            return
            
        is_strong, message = check_password_strength(password)
        if not is_strong:
            self.reg_status_label.configure(text=message, text_color="orange")
            return
            
        if register_user(username, password):
            self.reg_status_label.configure(text=f"User '{username}' registered! Go to Login.", text_color="green")
        else:
            self.reg_status_label.configure(text="Username already exists!", text_color="red")

    def show_dashboard(self):
        self.clear_screen()
        
        welcome_label = ctk.CTkLabel(self, text=f"Welcome, {self.current_user}!", font=ctk.CTkFont(size=20, weight="bold"))
        welcome_label.pack(pady=(30, 10))
        
        self.dash_status = ctk.CTkLabel(self, text="Select a file to perform actions", text_color="gray")
        self.dash_status.pack(pady=5)
        
        encrypt_btn = ctk.CTkButton(self, text="Encrypt a File", width=300, command=self.handle_encrypt)
        encrypt_btn.pack(pady=10)
        
        decrypt_btn = ctk.CTkButton(self, text="Decrypt a File", width=300, fg_color="orange", hover_color="darkorange", command=self.handle_decrypt)
        decrypt_btn.pack(pady=10)
        
        logout_btn = ctk.CTkButton(self, text="Logout", width=100, fg_color="darkred", hover_color="red", command=self.show_login_screen)
        logout_btn.pack(pady=20)

    def handle_encrypt(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            success = encrypt_file(file_path, self.session_key)
            if success:
                self.dash_status.configure(text=f"Encrypted: {os.path.basename(file_path)}", text_color="green")
            else:
                self.dash_status.configure(text="Encryption failed!", text_color="red")

    def handle_decrypt(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            success = decrypt_file(file_path, self.session_key)
            if success:
                self.dash_status.configure(text=f"Decrypted: {os.path.basename(file_path)}", text_color="green")
            else:
                self.dash_status.configure(text="Decryption failed!", text_color="red")

if __name__ == "__main__":
    app = SecureFileApp()
    app.mainloop()