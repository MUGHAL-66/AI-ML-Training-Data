"""A compact number guessing game for the desktop, built with standard Tkinter."""

import random
import tkinter as tk
from tkinter import ttk


class NumberGuessingGame:
    # Set to False to remove the development-only secret-number label.
    DEBUG_MODE = True

    COLORS = {
        "background": "#0B1020", "card": "#151B2E", "panel": "#1D2740",
        "input": "#10172A", "border": "#2A3652", "accent": "#7C5CFC",
        "blue": "#4F8CFF", "success": "#22C55E", "warning": "#F97316",
        "text": "#F8FAFC", "muted": "#94A3B8", "track": "#27334D",
    }
    DIFFICULTIES = {"EASY": 10, "MEDIUM": 7, "HARD": 5}

    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.configure(bg=self.COLORS["background"])
        self._center_window(650, 700)
        self.root.resizable(False, False)

        self.difficulty = "MEDIUM"
        self.guess_text = tk.StringVar()
        self.attempts_text = tk.StringVar()
        self.max_attempts = self.DIFFICULTIES[self.difficulty]
        self.attempts = 0
        self.secret_number = 0
        self.finished = False
        self.debug_text = tk.StringVar()

        self.create_widgets()
        self.new_game(show_welcome=True)
        self.root.bind("<Return>", self._on_enter)

    def _center_window(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        c = self.COLORS
        # One centered card keeps the complete game compact and aligned.
        self.card = tk.Frame(self.root, bg=c["card"], highlightthickness=1,
                             highlightbackground=c["border"])
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=530, height=650)
        content = tk.Frame(self.card, bg=c["card"])
        content.pack(fill="both", expand=True, padx=34, pady=25)

        tk.Label(content, text="🎯  NUMBER GUESSING GAME", bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 19, "bold")).pack(pady=(2, 5))
        tk.Label(content, text="Guess the hidden number between 1 and 100", bg=c["card"],
                 fg=c["muted"], font=("Segoe UI", 10)).pack(pady=(0, 17))

        tk.Label(content, text="DIFFICULTY", bg=c["card"], fg=c["muted"],
                 font=("Segoe UI", 8, "bold")).pack(pady=(0, 8))
        choices = tk.Frame(content, bg=c["card"])
        choices.pack()
        self.difficulty_buttons = {}
        for name in self.DIFFICULTIES:
            button = tk.Button(choices, text=name, command=lambda level=name: self.set_difficulty(level),
                               relief="flat", bd=0, cursor="hand2", width=10, pady=8,
                               font=("Segoe UI", 9, "bold"), fg=c["muted"],
                               bg=c["panel"], activeforeground=c["text"], activebackground=c["panel"])
            button.pack(side="left", padx=4)
            self.difficulty_buttons[name] = button

        self.level_label = tk.Label(content, text="MEDIUM", bg=c["card"], fg=c["blue"],
                                    font=("Segoe UI", 9, "bold"))
        self.level_label.pack(pady=(14, 2))
        self.attempts_text_label = tk.Label(content, textvariable=self.attempts_text, bg=c["card"],
                                            fg=c["text"], font=("Segoe UI", 11, "bold"))
        self.attempts_text_label.pack(pady=(0, 13))

        # Input and action are grouped as one interaction.
        self.entry = tk.Entry(content, textvariable=self.guess_text, justify="center",
                              bg=c["input"], fg=c["text"], insertbackground=c["text"],
                              relief="flat", highlightthickness=1,
                              highlightbackground=c["border"], highlightcolor=c["accent"],
                              font=("Segoe UI", 15))
        self.entry.pack(fill="x", ipady=10)
        self.entry.insert(0, "Enter your guess")
        self.entry.config(fg="#71809D")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)

        self.guess_button = tk.Button(content, text="GUESS NUMBER", command=self.check_guess,
                                      relief="flat", bd=0, cursor="hand2", bg=c["accent"],
                                      activebackground="#6D4DE8", fg="white", activeforeground="white",
                                      font=("Segoe UI", 10, "bold"), pady=11)
        self.guess_button.pack(fill="x", pady=(10, 12))

        # Fixed-height panel with separate title/detail labels prevents layout jumps.
        self.feedback_panel = tk.Frame(content, bg=c["panel"], height=76,
                                       highlightthickness=1, highlightbackground=c["border"])
        self.feedback_panel.pack(fill="x", pady=(0, 15))
        self.feedback_panel.pack_propagate(False)
        self.feedback_title = tk.Label(self.feedback_panel, text="READY WHEN YOU ARE",
                                       bg=c["panel"], fg=c["blue"],
                                       font=("Segoe UI", 11, "bold"))
        self.feedback_title.pack(pady=(14, 2))
        self.feedback_detail = tk.Label(self.feedback_panel, text="Enter a number to begin.",
                                        bg=c["panel"], fg=c["muted"],
                                        font=("Segoe UI", 9))
        self.feedback_detail.pack()

        stat_row = tk.Frame(content, bg=c["card"])
        stat_row.pack(fill="x")
        tk.Label(stat_row, text="ATTEMPTS", bg=c["card"], fg=c["muted"],
                 font=("Segoe UI", 8, "bold")).pack(side="left")
        self.attempts_value = tk.Label(stat_row, text="0 / 7", bg=c["card"], fg=c["text"],
                                       font=("Segoe UI", 10, "bold"))
        self.attempts_value.pack(side="right")

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Game.Horizontal.TProgressbar", troughcolor=c["track"],
                        background=c["blue"], bordercolor=c["track"],
                        lightcolor=c["blue"], darkcolor=c["blue"], thickness=8)
        self.progress = ttk.Progressbar(content, style="Game.Horizontal.TProgressbar",
                                        maximum=100, mode="determinate")
        self.progress.pack(fill="x", pady=(8, 0))

        actions = tk.Frame(content, bg=c["card"])
        actions.pack(pady=(18, 0))
        self.again_button = tk.Button(actions, text="↻  PLAY AGAIN", command=self.new_game,
                                      relief="flat", bd=0, cursor="hand2", bg=c["panel"],
                                      activebackground="#293651", fg=c["text"],
                                      activeforeground=c["text"], font=("Segoe UI", 9, "bold"),
                                      padx=17, pady=9)
        self.again_button.pack(side="left", padx=5)
        tk.Button(actions, text="✕  EXIT", command=self.root.destroy, relief="flat", bd=0,
                  cursor="hand2", bg="#222A3D", activebackground="#303A52", fg=c["muted"],
                  activeforeground=c["text"], font=("Segoe UI", 9, "bold"),
                  padx=17, pady=9).pack(side="left", padx=5)

        if self.DEBUG_MODE:
            tk.Label(content, textvariable=self.debug_text, bg=c["card"], fg="#64748B",
                     font=("Consolas", 8)).pack(pady=(8, 0))

    def set_difficulty(self, level):
        self.difficulty = level
        self.new_game(show_welcome=True)

    def new_game(self, show_welcome=False):
        self.max_attempts = self.DIFFICULTIES[self.difficulty]
        self.secret_number = random.randint(1, 100)
        if self.DEBUG_MODE:
            self.debug_text.set(f"DEBUG: Secret Number = {self.secret_number}")
        self.attempts = 0
        self.finished = False
        self.guess_text.set("")
        self.entry.config(state="normal", fg=self.COLORS["text"])
        self.guess_button.config(state="normal", bg=self.COLORS["accent"])
        self.level_label.config(text=self.difficulty)
        for level, button in self.difficulty_buttons.items():
            selected = level == self.difficulty
            button.config(bg=self.COLORS["accent"] if selected else self.COLORS["panel"],
                          fg=self.COLORS["text"] if selected else self.COLORS["muted"])
        if show_welcome:
            self.set_feedback("NEW ROUND", "Make your first guess.", self.COLORS["blue"])
        else:
            self.set_feedback("READY WHEN YOU ARE", "Enter a number to begin.", self.COLORS["blue"])
        self.update_progress()
        self.entry.focus_set()

    def check_guess(self):
        if self.finished:
            return
        raw = self.guess_text.get().strip()
        if not raw or raw == "Enter your guess":
            self.set_feedback("GUESS NEEDED", "Enter a number from 1 to 100.", self.COLORS["warning"])
            self.entry.focus_set()
            return
        try:
            guess = int(raw)
        except ValueError:
            self.set_feedback("INVALID INPUT", "Use a whole number, such as 42.", self.COLORS["warning"])
            self.entry.focus_set()
            return
        if not 1 <= guess <= 100:
            self.set_feedback("OUT OF RANGE", "Choose a number between 1 and 100.", self.COLORS["warning"])
            self.entry.focus_set()
            return

        self.attempts += 1
        self.update_progress()
        if guess == self.secret_number:
            self.finished = True
            self.set_feedback("🎉 YOU WON!", f"The number was {self.secret_number} · Found in {self.attempts} "
                               f"{'attempt' if self.attempts == 1 else 'attempts'}.", self.COLORS["success"])
            self._finish_game()
        elif self.attempts == self.max_attempts:
            self.game_over()
        elif guess < self.secret_number:
            self.set_feedback("⬆ TOO LOW", "Try a higher number", self.COLORS["blue"])
        else:
            self.set_feedback("⬇ TOO HIGH", "Try a lower number", self.COLORS["warning"])

        self.guess_text.set("")
        if not self.finished:
            self.entry.focus_set()

    def set_feedback(self, title, detail, color):
        """Update the persistent feedback area without changing its dimensions."""
        self.feedback_title.config(text=title, fg=color)
        self.feedback_detail.config(text=detail)

    def update_progress(self):
        self.attempts_text.set(f"Attempts: {self.attempts} / {self.max_attempts}")
        self.attempts_value.config(text=f"{self.attempts} / {self.max_attempts}")
        remaining_percent = (self.max_attempts - self.attempts) / self.max_attempts * 100
        self.progress.configure(value=remaining_percent)

    def game_over(self):
        self.finished = True
        self.set_feedback("GAME OVER", f"The number was {self.secret_number}.", self.COLORS["warning"])
        self._finish_game()

    def _finish_game(self):
        self.entry.config(state="disabled")
        self.guess_button.config(state="disabled", bg="#41445A")
        self.again_button.focus_set()

    def _on_enter(self, _event=None):
        self.check_guess()
        return "break"

    def _clear_placeholder(self, _event=None):
        if self.guess_text.get() == "Enter your guess":
            self.guess_text.set("")
            self.entry.config(fg=self.COLORS["text"])

    def _restore_placeholder(self, _event=None):
        if not self.guess_text.get() and str(self.entry.cget("state")) != "disabled":
            self.guess_text.set("Enter your guess")
            self.entry.config(fg="#71809D")


def main():
    """Launch the game; give a clear message if Tk cannot create a desktop window."""
    try:
        root = tk.Tk()
        NumberGuessingGame(root)
        root.mainloop()
    except tk.TclError as exc:
        print(f"Unable to start the desktop window: {exc}")


if __name__ == "__main__":
    main()
