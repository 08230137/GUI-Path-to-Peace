import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    add_counselling_request, get_user_requests,
    add_mood_entry, get_mood_entries
)

BG = "#F5F1F7"
PURPLE = "#76558F"
DARK = "#3D3147"
WHITE = "#FFFFFF"
GREEN = "#4D8B68"
RED = "#B85C5C"
YELLOW = "#B38B2E"

class UserDashboard:
    def __init__(self, root, user, show_login):
        self.root = root
        self.user = user
        self.show_login = show_login

        self.window = tk.Toplevel(root)
        self.window.title("Path to Peace - User Dashboard")
        self.window.geometry("1100x700")
        self.window.configure(bg=BG)
        self.window.minsize(950, 620)
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        self.build()

    def build(self):
        sidebar = tk.Frame(self.window, bg=PURPLE, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="🌿", font=("Segoe UI", 35),
            bg=PURPLE, fg=WHITE
        ).pack(pady=(35, 5))

        tk.Label(
            sidebar, text="Path to Peace",
            font=("Segoe UI", 17, "bold"),
            bg=PURPLE, fg=WHITE
        ).pack()

        tk.Button(
            sidebar, text="🏠  Dashboard",
            command=self.show_home,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=25, pady=12
        ).pack(fill="x", pady=(35, 2))

        tk.Button(
            sidebar, text="📝  Book Counselling",
            command=self.show_booking,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=25, pady=12
        ).pack(fill="x")

        tk.Button(
            sidebar, text="😊  Mood Tracker",
            command=self.show_mood,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=25, pady=12
        ).pack(fill="x")

        tk.Button(
            sidebar, text="📚  Resources",
            command=self.show_resources,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=25, pady=12
        ).pack(fill="x")

        tk.Button(
            sidebar, text="☎  Emergency Help",
            command=self.show_emergency,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=25, pady=12
        ).pack(fill="x")

        tk.Button(
            sidebar, text="Logout",
            command=self.logout,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=25, pady=12
        ).pack(side="bottom", fill="x", pady=20)

        self.content = tk.Frame(self.window, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def title(self, heading, subtitle=""):
        tk.Label(
            self.content, text=heading,
            font=("Segoe UI", 25, "bold"),
            bg=BG, fg=DARK
        ).pack(anchor="w", padx=35, pady=(30, 2))

        if subtitle:
            tk.Label(
                self.content, text=subtitle,
                font=("Segoe UI", 10),
                bg=BG, fg="#777777"
            ).pack(anchor="w", padx=35, pady=(0, 20))

    def card(self, parent, text, value, color=PURPLE):
        frame = tk.Frame(parent, bg=WHITE, padx=20, pady=18)
        frame.pack(side="left", fill="both", expand=True, padx=6)
        tk.Label(frame, text=text, bg=WHITE, fg="#777777",
                 font=("Segoe UI", 10)).pack(anchor="w")
        tk.Label(frame, text=value, bg=WHITE, fg=color,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(5, 0))
        return frame

    def show_home(self):
        self.clear_content()
        self.title(
            f"Welcome, {self.user['full_name']} 🌿",
            "Your private space to check in, seek support and find helpful resources."
        )

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", padx=30, pady=10)

        requests = get_user_requests(self.user["id"])
        pending = len([r for r in requests if r[5] == "Pending"])
        accepted = len([r for r in requests if r[5] == "Accepted"])

        self.card(cards, "MY REQUESTS", str(len(requests)))
        self.card(cards, "PENDING", str(pending), YELLOW)
        self.card(cards, "ACCEPTED", str(accepted), GREEN)

        welcome = tk.Frame(self.content, bg=WHITE, padx=25, pady=25)
        welcome.pack(fill="x", padx=36, pady=20)

        tk.Label(
            welcome, text="A gentle reminder",
            font=("Segoe UI", 16, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w")

        tk.Label(
            welcome,
            text="You do not have to deal with everything alone. "
                 "If you would like to talk to a counsellor, you can send a private request.",
            wraplength=700, justify="left",
            font=("Segoe UI", 11),
            bg=WHITE, fg="#555555"
        ).pack(anchor="w", pady=10)

        tk.Button(
            welcome, text="Request Counselling",
            command=self.show_booking,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18, pady=9
        ).pack(anchor="w", pady=5)

        self.show_recent_requests()

    def show_recent_requests(self):
        box = tk.Frame(self.content, bg=WHITE, padx=20, pady=15)
        box.pack(fill="both", expand=True, padx=36, pady=(0, 20))

        tk.Label(
            box, text="Recent Counselling Requests",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", pady=(0, 10))

        columns = ("ID", "Concern", "Date", "Time", "Status")
        tree = ttk.Treeview(box, columns=columns, show="headings", height=7)

        for col in columns:
            tree.heading(col, text=col)

        tree.column("ID", width=50, anchor="center")
        tree.column("Concern", width=330)
        tree.column("Date", width=110, anchor="center")
        tree.column("Time", width=100, anchor="center")
        tree.column("Status", width=110, anchor="center")

        for row in get_user_requests(self.user["id"]):
            tree.insert("", "end", values=(row[0], row[2], row[3], row[4], row[5]))

        tree.pack(fill="both", expand=True)

    def show_booking(self):
        self.clear_content()
        self.title(
            "Book a Counselling Session",
            "Share only what you feel comfortable sharing."
        )

        form = tk.Frame(self.content, bg=WHITE, padx=30, pady=25)
        form.pack(fill="x", padx=36, pady=10)

        tk.Label(form, text="Name shown to counsellor",
                 bg=WHITE, fg=DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w")

        anonymous_var = tk.BooleanVar(value=False)
        self.name_entry = ttk.Entry(form)
        self.name_entry.insert(0, self.user["full_name"])
        self.name_entry.pack(fill="x", pady=(5, 15))

        tk.Checkbutton(
            form, text="Submit anonymously",
            variable=anonymous_var,
            bg=WHITE, fg=DARK,
            activebackground=WHITE,
            command=lambda: self.toggle_anonymous(anonymous_var)
        ).pack(anchor="w", pady=(0, 15))

        tk.Label(form, text="What would you like support with?",
                 bg=WHITE, fg=DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w")

        concern = tk.Text(form, height=7, font=("Segoe UI", 10))
        concern.pack(fill="x", pady=(5, 15))

        row = tk.Frame(form, bg=WHITE)
        row.pack(fill="x")

        left = tk.Frame(row, bg=WHITE)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(left, text="Preferred date (e.g. 2026-10-05)",
                 bg=WHITE, fg=DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        date_entry = ttk.Entry(left)
        date_entry.pack(fill="x", pady=5)

        right = tk.Frame(row, bg=WHITE)
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))
        tk.Label(right, text="Preferred time",
                 bg=WHITE, fg=DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        time_entry = ttk.Entry(right)
        time_entry.pack(fill="x", pady=5)

        def submit():
            display_name = self.name_entry.get().strip()
            message = concern.get("1.0", "end").strip()
            date = date_entry.get().strip()
            time = time_entry.get().strip()

            if not message:
                messagebox.showwarning("Request", "Please describe what you need support with.")
                return

            if not display_name:
                display_name = "Anonymous"

            add_counselling_request(
                self.user["id"], display_name, message, date, time
            )
            messagebox.showinfo(
                "Request Submitted",
                "Your counselling request has been submitted and is now pending review."
            )
            self.show_home()

        tk.Button(
            form, text="SUBMIT COUNSELLING REQUEST",
            command=submit, bg=PURPLE, fg=WHITE,
            relief="flat", font=("Segoe UI", 10, "bold"),
            padx=18, pady=10
        ).pack(anchor="w", pady=(15, 0))

    def toggle_anonymous(self, var):
        if var.get():
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, "Anonymous")
        else:
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, self.user["full_name"])

    def show_mood(self):
        self.clear_content()
        self.title(
            "Mood Tracker",
            "A simple check-in tool for emotional awareness."
        )

        form = tk.Frame(self.content, bg=WHITE, padx=25, pady=25)
        form.pack(fill="x", padx=36, pady=10)

        tk.Label(
            form, text="How are you feeling today?",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", pady=(0, 12))

        mood_var = tk.StringVar(value="😊 Good")
        moods = ["😊 Great", "🙂 Good", "😐 Okay", "😔 Low", "😟 Stressed"]

        combo = ttk.Combobox(
            form, textvariable=mood_var,
            values=moods, state="readonly", width=30
        )
        combo.pack(anchor="w")

        tk.Label(
            form, text="Optional note",
            bg=WHITE, fg=DARK,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(15, 5))

        note = tk.Text(form, height=5)
        note.pack(fill="x")

        def save():
            add_mood_entry(
                self.user["id"],
                mood_var.get(),
                note.get("1.0", "end").strip()
            )
            messagebox.showinfo("Mood Tracker", "Your mood check-in was saved.")
            self.show_mood()

        tk.Button(
            form, text="SAVE CHECK-IN",
            command=save, bg=PURPLE, fg=WHITE,
            relief="flat", font=("Segoe UI", 10, "bold"),
            padx=15, pady=8
        ).pack(anchor="w", pady=15)

        history = tk.Frame(self.content, bg=WHITE, padx=25, pady=20)
        history.pack(fill="both", expand=True, padx=36, pady=(5, 20))

        tk.Label(
            history, text="Recent Check-ins",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", pady=(0, 10))

        for mood, note_text, created in get_mood_entries(self.user["id"]):
            row = tk.Frame(history, bg="#FAF8FB", padx=10, pady=8)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=mood, bg="#FAF8FB",
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(row, text=created, bg="#FAF8FB",
                     fg="#777777").pack(side="right")
            if note_text:
                tk.Label(row, text=note_text, bg="#FAF8FB",
                         fg="#555555").pack(side="left", padx=15)

    def show_resources(self):
        self.clear_content()
        self.title(
            "Resources",
            "Small steps and useful reminders for student well-being."
        )

        resources = [
            ("Study Balance", "Break large tasks into smaller steps and give yourself short breaks."),
            ("Sleep & Rest", "A regular sleep routine can help you manage study pressure."),
            ("Talk to Someone", "You can reach out to a trusted friend, teacher, family member or counsellor."),
            ("Self-Care", "Take time for food, water, movement, hobbies and activities that help you relax."),
        ]

        for heading, text in resources:
            card = tk.Frame(self.content, bg=WHITE, padx=25, pady=18)
            card.pack(fill="x", padx=36, pady=6)
            tk.Label(card, text=heading, font=("Segoe UI", 14, "bold"),
                     bg=WHITE, fg=PURPLE).pack(anchor="w")
            tk.Label(card, text=text, font=("Segoe UI", 10),
                     bg=WHITE, fg="#555555", wraplength=700,
                     justify="left").pack(anchor="w", pady=(5, 0))

    def show_emergency(self):
        self.clear_content()
        self.title(
            "Emergency Support",
            "If you are in immediate danger, contact local emergency services or a trusted person."
        )

        card = tk.Frame(self.content, bg=WHITE, padx=30, pady=30)
        card.pack(fill="x", padx=36, pady=15)

        tk.Label(
            card, text="☎ Emergency / Immediate Help",
            font=("Segoe UI", 17, "bold"),
            bg=WHITE, fg=RED
        ).pack(anchor="w")

        tk.Label(
            card,
            text="If you feel unsafe or believe you may hurt yourself or someone else, "
                 "seek immediate help from emergency services, a healthcare professional, "
                 "a trusted adult, or someone nearby.",
            font=("Segoe UI", 11), bg=WHITE, fg="#555555",
            wraplength=720, justify="left"
        ).pack(anchor="w", pady=15)

        tk.Label(
            card,
            text="Project emergency contact: +975 98 765 432",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE, fg=RED
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Replace this demo number with the verified contact approved by your college/project.",
            font=("Segoe UI", 9), bg=WHITE, fg="#888888"
        ).pack(anchor="w", pady=8)

    def logout(self):
        self.window.destroy()
        self.show_login()
