import tkinter as tk
from tkinter import ttk, messagebox

from database import login_user, register_user
from user_dashboard import UserDashboard
from admin_dashboard import AdminDashboard


BG = "#F5F1F7"
PURPLE = "#76558F"
DARK = "#3D3147"
WHITE = "#FFFFFF"


class LoginWindow:

    def __init__(self, root, show_login):

        self.root = root
        self.show_login = show_login

        # Hide the main/root window
        self.root.withdraw()

        # Create login window
        self.window = tk.Toplevel(self.root)
        self.window.title("Path to Peace - Login")

        # Full screen
        self.window.attributes("-fullscreen", True)

        self.window.configure(bg=BG)

        # Close the whole application
        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.root.destroy
        )

        self.build()

    def build(self):

        # =========================
        # LEFT PURPLE SECTION
        # =========================

        left = tk.Frame(
            self.window,
            bg=PURPLE,
            width=380
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="🌿",
            font=("Segoe UI", 60),
            bg=PURPLE,
            fg=WHITE
        ).pack(pady=(120, 10))

        tk.Label(
            left,
            text="Path to Peace",
            font=("Segoe UI", 30, "bold"),
            bg=PURPLE,
            fg=WHITE
        ).pack()

        tk.Label(
            left,
            text="A safe space to pause,\n"
                 "connect and seek support.",
            font=("Segoe UI", 13),
            bg=PURPLE,
            fg=WHITE,
            justify="center"
        ).pack(pady=25)

        tk.Label(
            left,
            text="“It is okay to ask for help.”",
            font=("Segoe UI", 11, "italic"),
            bg=PURPLE,
            fg=WHITE
        ).pack(
            side="bottom",
            pady=60
        )

        # =========================
        # RIGHT WHITE SECTION
        # =========================

        right = tk.Frame(
            self.window,
            bg=WHITE
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Center the login form
        form = tk.Frame(
            right,
            bg=WHITE,
            width=500
        )

        form.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            form,
            text="Welcome Back",
            font=("Segoe UI", 28, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w")

        tk.Label(
            form,
            text="Log in to continue to Path to Peace",
            font=("Segoe UI", 11),
            bg=WHITE,
            fg="#777777"
        ).pack(
            anchor="w",
            pady=(8, 35)
        )

        # =========================
        # USERNAME
        # =========================

        tk.Label(
            form,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w")

        self.username = ttk.Entry(
            form,
            font=("Segoe UI", 12)
        )

        self.username.pack(
            fill="x",
            pady=(6, 18),
            ipady=7
        )

        # =========================
        # PASSWORD
        # =========================

        tk.Label(
            form,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w")

        self.password = ttk.Entry(
            form,
            font=("Segoe UI", 12),
            show="•"
        )

        self.password.pack(
            fill="x",
            pady=(6, 25),
            ipady=7
        )

        # =========================
        # LOGIN BUTTON
        # =========================

        tk.Button(
            form,
            text="LOGIN",
            command=self.login,
            bg=PURPLE,
            fg=WHITE,
            activebackground=PURPLE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            pady=13,
            cursor="hand2"
        ).pack(
            fill="x"
        )

        # =========================
        # REGISTER BUTTON
        # =========================

        tk.Button(
            form,
            text="Create a User Account",
            command=self.open_register,
            bg=WHITE,
            fg=PURPLE,
            activebackground=WHITE,
            activeforeground=PURPLE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            pady=12,
            cursor="hand2"
        ).pack(
            fill="x",
            pady=10
        )

        # NO ADMIN PASSWORD SHOWN HERE

        tk.Label(
            form,
            text="Please use your registered account to continue.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg="#888888"
        ).pack(pady=10)

        # Focus username
        self.username.focus_set()

        # Press Enter to login
        self.window.bind(
            "<Return>",
            lambda event: self.login()
        )

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        if not username or not password:

            messagebox.showwarning(
                "Login",
                "Please enter username and password."
            )

            return

        # Check login using database.py
        user = login_user(
            username,
            password
        )

        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

            return

        # Close login window
        self.window.destroy()

        # Open correct dashboard
        if user["role"] == "admin":

            AdminDashboard(
                self.root,
                user,
                self.show_login
            )

        else:

            UserDashboard(
                self.root,
                user,
                self.show_login
            )

    def open_register(self):

        RegisterWindow(
            self.window
        )


# =====================================================
# REGISTER WINDOW
# =====================================================

class RegisterWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Create Account"
        )

        self.window.geometry(
            "450x500"
        )

        self.window.configure(
            bg=WHITE
        )

        self.window.resizable(
            False,
            False
        )

        # Keep registration above login
        self.window.transient(parent)

        self.window.grab_set()

        tk.Label(
            self.window,
            text="Create User Account",
            font=("Segoe UI", 22, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            pady=(35, 25)
        )

        form = tk.Frame(
            self.window,
            bg=WHITE
        )

        form.pack(
            fill="x",
            padx=45
        )

        self.entries = {}

        fields = [
            ("Full Name", "name"),
            ("Username", "username"),
            ("Password", "password"),
            ("Confirm Password", "confirm")
        ]

        for label, key in fields:

            tk.Label(
                form,
                text=label,
                bg=WHITE,
                fg=DARK,
                font=("Segoe UI", 10, "bold")
            ).pack(
                anchor="w",
                pady=(8, 3)
            )

            entry = ttk.Entry(
                form,
                width=38,
                show="•"
                if key in ["password", "confirm"]
                else ""
            )

            entry.pack(
                fill="x"
            )

            self.entries[key] = entry

        tk.Button(
            self.window,
            text="CREATE ACCOUNT",
            command=self.create,
            bg=PURPLE,
            fg=WHITE,
            activebackground=PURPLE,
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            pady=10,
            cursor="hand2"
        ).pack(
            fill="x",
            padx=45,
            pady=25
        )

    def create(self):

        name = self.entries["name"].get().strip()

        username = self.entries["username"].get().strip()

        password = self.entries["password"].get()

        confirm = self.entries["confirm"].get()

        if not all([
            name,
            username,
            password,
            confirm
        ]):

            messagebox.showwarning(
                "Registration",
                "Please complete all fields."
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Registration",
                "Passwords do not match."
            )

            return

        if len(password) < 4:

            messagebox.showwarning(
                "Registration",
                "Password should contain at least 4 characters."
            )

            return

        success, message = register_user(
            name,
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Registration",
                message
            )

            self.window.destroy()

        else:

            messagebox.showerror(
                "Registration",
                message
            )