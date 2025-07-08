import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import secrets
import string
import pyperclip

# --- Evaluation Logic ---
def evaluate_password(pwd):
    categories = {
        "lower": sum(1 for c in pwd if c.islower()),
        "upper": sum(1 for c in pwd if c.isupper()),
        "digits": sum(1 for c in pwd if c.isdigit()),
        "spaces": pwd.count(" "),
        "specials": sum(1 for c in pwd if c in string.punctuation)
    }

    score = sum(1 for count in categories.values() if count > 0)

    if score <= 1:
        comment = "Extremely weak! Consider using mixed characters."
    elif score == 2:
        comment = "Not great. Add more variety."
    elif score == 3:
        comment = "Decent, but you can improve it."
    elif score == 4:
        comment = "Good job! Password is strong."
    else:
        comment = "Excellent! This is a very strong password."

    feedback = (
        f"Composition:\n"
        f"- Lowercase: {categories['lower']}\n"
        f"- Uppercase: {categories['upper']}\n"
        f"- Digits: {categories['digits']}\n"
        f"- Spaces: {categories['spaces']}\n"
        f"- Symbols: {categories['specials']}\n"
        f"\nStrength Level: {score}/5\n\n"
        f"Feedback: {comment}"
    )
    return feedback, score


def analyze():
    pwd = pwd_input.get()
    result, rating = evaluate_password(pwd)
    display_box.config(state="normal")
    display_box.delete("1.0", "end")
    display_box.insert("end", result)
    display_box.config(state="disabled")
    set_progress(rating * 20)


def generate_new():
    chars = string.ascii_letters + string.digits + string.punctuation
    new_pwd = ''.join(secrets.choice(chars) for _ in range(14))
    pwd_input.delete(0, "end")
    pwd_input.insert("end", new_pwd)


def copy_to_clipboard():
    val = pwd_input.get()
    if val:
        pyperclip.copy(val)
        messagebox.showinfo("Copied", "Password has been copied.")
    else:
        messagebox.showwarning("Empty Field", "No password found to copy.")


def clear_all():
    pwd_input.delete(0, "end")
    display_box.config(state="normal")
    display_box.delete("1.0", "end")
    display_box.config(state="disabled")
    strength_bar["value"] = 0


def set_progress(val):
    strength_bar["value"] = 0
    animate_bar(val, 0)


def close_window():
    if messagebox.askyesno("Exit", "Exit the Pass4Life?"):
        root.destroy()


root = tk.Tk()
root.title("Task3 - Siddhant Jain")
root.geometry("700x450")
root.configure(bg="#f4f6f7")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", background="#f4f6f7")
style.configure("TFrame", background="#f4f6f7")
style.configure("green.Horizontal.TProgressbar", troughcolor='#dfe6e9', background='#00b894')


main_frame = ttk.Frame(root)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

title = ttk.Label(main_frame, text="🔐 Pass4Life: Your Lockmate", font=("Segoe UI", 20, "bold"), anchor="center")
title.pack(pady=(0, 10))

input_frame = ttk.Frame(main_frame)
input_frame.pack(fill="x", pady=10)

ttk.Label(input_frame, text="Enter or Generate a Password:", font=("Segoe UI", 12)).pack(anchor="w", padx=5)
pwd_input = tk.Entry(input_frame, show="*", font=("Consolas", 14), width=40)
pwd_input.pack(padx=5, pady=5)

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Check Strength", command=analyze).grid(row=0, column=0, padx=6)
ttk.Button(button_frame, text="Generate New", command=generate_new).grid(row=0, column=1, padx=6)
ttk.Button(button_frame, text="Copy", command=copy_to_clipboard).grid(row=0, column=2, padx=6)
ttk.Button(button_frame, text="Clear", command=clear_all).grid(row=0, column=3, padx=6)
ttk.Button(button_frame, text="Exit", command=close_window).grid(row=0, column=4, padx=6)

display_box = tk.Text(main_frame, height=10, state='disabled', font=("Courier New", 10), wrap="word", bg="#ecf0f1")
display_box.pack(pady=15, fill="x", padx=5)

bar_canvas = tk.Canvas(main_frame, width=500, height=22, bg="#dfe6e9", bd=0, highlightthickness=0)
bar_canvas.pack(pady=8)
bar_fill = bar_canvas.create_rectangle(0, 0, 0, 22, fill="red", width=0)

def set_progress(strength_percent):
    animate_rgb_bar(strength_percent, 0)

def animate_rgb_bar(target, current):
    if current <= target:
        bar_canvas.coords(bar_fill, 0, 0, current * 5, 22)
        color = get_rgb_color(current)
        bar_canvas.itemconfig(bar_fill, fill=color)
        root.after(10, animate_rgb_bar, target, current + 1)

def get_rgb_color(value):
    
    if value < 50:
        r = 255
        g = int((value / 50) * 255)
    else:
        r = int((1 - ((value - 50) / 50)) * 255)
        g = 255
    return f'#{r:02x}{g:02x}00'


root.protocol("WM_DELETE_WINDOW", close_window)
pwd_input.bind("<KeyRelease>", lambda e: analyze())

root.mainloop()
