import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class LoginPage(ctk.CTkToplevel):
    def __init__(self, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app = main_app
        self.title("Login")
        self.geometry("400x250")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.login_label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_event)
        self.login_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.new_user_label = ctk.CTkLabel(self, text="Don't have an account?")
        self.new_user_label.grid(row=4, column=0, padx=20, pady=(10, 5))

        self.register_button = ctk.CTkButton(self, text="Create New Account", command=self.open_registration_page, fg_color="gray70", text_color="white", hover_color="gray55")
        self.register_button.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.main_app.check_credentials(username, password):
            self.destroy()
            self.main_app.destroy()
            subprocess.Popen([sys.executable, "App.py"])

        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_registration_page(self):
        RegistrationPage(self.main_app)

    def on_closing(self):
        self.main_app.destroy()


class RegistrationPage(ctk.CTkToplevel):
    def __init__(self, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app = main_app
        self.title("Create New Account")
        self.geometry("400x300")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        register_label = ctk.CTkLabel(self, text="Create New Account", font=ctk.CTkFont(size=24, weight="bold"))
        register_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="New Username")
        self.new_username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        register_button = ctk.CTkButton(self, text="Register", command=self.register_user)
        register_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if new_password == confirm_password:
            if self.main_app.register_user(new_username, new_password):
                messagebox.showinfo("Registration Successful", f"Account created for user: {new_username}. You can now log in.")
                self.destroy()
            else:
                messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            messagebox.showerror("Password Mismatch", "Passwords do not match.")


# Example main application classimport customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# ------------------- Login Page ------------------- #
class LoginPage(ctk.CTkToplevel):
    def __init__(self, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app = main_app
        self.title("Login")
        self.geometry("400x400")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.login_label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_event)
        self.login_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.new_user_label = ctk.CTkLabel(self, text="Don't have an account?")
        self.new_user_label.grid(row=4, column=0, padx=20, pady=(10, 5))

        self.register_button = ctk.CTkButton(self, text="Create New Account", command=self.open_registration_page, fg_color="gray70", text_color="white", hover_color="gray55")
        self.register_button.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.main_app.check_credentials(username, password):
            self.destroy()
            self.main_app.destroy()
            subprocess.Popen([sys.executable, "momo_V3.py"])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_registration_page(self):
        RegistrationPage(self.main_app)

    def on_closing(self):
        self.main_app.destroy()


# ------------------- Registration Page ------------------- #
class RegistrationPage(ctk.CTkToplevel):
    def __init__(self, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app = main_app
        self.title("Create New Account")
        self.geometry("400x300")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        register_label = ctk.CTkLabel(self, text="Create New Account", font=ctk.CTkFont(size=24, weight="bold"))
        register_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="New Username")
        self.new_username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        register_button = ctk.CTkButton(self, text="Register", command=self.register_user)
        register_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if new_password == confirm_password:
            if self.main_app.register_user(new_username, new_password):
                messagebox.showinfo("Registration Successful", f"Account created for user: {new_username}. You can now log in.")
                self.destroy()
            else:
                messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            messagebox.showerror("Password Mismatch", "Passwords do not match.")


# ------------------- Main App ------------------- #
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")
        self.geometry("200x100")
        self.withdraw()  # Hide the root window

        # In-memory user store
        self.users = {"admin": "admin"}  # Default user
        LoginPage(self)

    def check_credentials(self, username, password):
        return username in self.users and self.users[username] == password

    def register_user(self, username, password):
        if username in self.users:
            return False  # Username already exists
        self.users[username] = password
        return True

    def show_main_ui(self):
        self.deiconify()


# ------------------- Start App ------------------- #
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
