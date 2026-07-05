import customtkinter as ctk
import os

# Set up the look and feel of the app
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SecureFileApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Secure File Encryption Suite")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Track current logged-in user
        self.current_user = None
        
        # Initialize to show the Login Screen first
        self.show_login_screen()

    def clear_screen(self):
        """Removes all widgets from the window."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Displays the Login UI."""
        self.clear_screen()
        
        # Title Label
        title_label = ctk.CTkLabel(self, text="Secure Login", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(40, 20))
        
        # Username Entry
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=10)
        
        # Password Entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=10)
        
        # Status Message Label
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack(pady=5)
        
        # Login Button
        login_btn = ctk.CTkButton(self, text="Login", width=300, command=self.handle_login)
        login_btn.pack(pady=10)
        
        # Switch to Register Label/Button
        register_link = ctk.CTkButton(self, text="Don't have an account? Register", fg_color="transparent", hover_color=None, text_color="gray", command=self.show_register_screen)
        register_link.pack(pady=10)

    def show_register_screen(self):
        """Displays the Registration UI."""
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
        
        login_link = ctk.CTkButton(self, text="Already have an account? Login", fg_color="transparent", hover_color=None, text_color="gray", command=self.show_login_screen)
        login_link.pack(pady=10)

    def handle_login(self):
        """Placeholder for login logic integration."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin":  # Temporary check
            self.current_user = username
            self.show_dashboard()
        else:
            self.status_label.configure(text="Invalid username or password!")

    def handle_register(self):
        """Placeholder for registration logic integration."""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        
        if username and password:
            self.reg_status_label.configure(text=f"User '{username}' registered! (Go to Login)", text_color="green")
        else:
            self.reg_status_label.configure(text="Fields cannot be empty!", text_color="red")

    def show_dashboard(self):
        """Displays the main application Dashboard after successful login."""
        self.clear_screen()
        
        welcome_label = ctk.CTkLabel(self, text=f"Welcome, {self.current_user}!", font=ctk.CTkFont(size=20, weight="bold"))
        welcome_label.pack(pady=(30, 10))
        
        info_label = ctk.CTkLabel(self, text="Secure File Encryption Dashboard", text_color="gray")
        info_label.pack(pady=5)
        
        # File Action Buttons
        select_file_btn = ctk.CTkButton(self, text="Select File to Encrypt/Decrypt", width=300)
        select_file_btn.pack(pady=30)
        
        logout_btn = ctk.CTkButton(self, text="Logout", width=100, fg_color="darkred", hover_color="red", command=self.show_login_screen)
        logout_btn.pack(pady=10)

if __name__ == "__main__":
    app = SecureFileApp()
    app.mainloop()