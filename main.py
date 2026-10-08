import tkinter as tk
from database import init_db, create_default_admin
from login import LoginWindow


def main():
    # Create database and default counsellor account
    init_db()
    create_default_admin()

    root = tk.Tk()
    root.withdraw()

    def show_login():
        LoginWindow(root, show_login)

    show_login()

    root.mainloop()


if __name__ == "__main__":
    main()