import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 

def caesar_cipher(text, shift, mode):
    result = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift if mode == 'encrypt' else ord(char) - shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result

def encrypt_decrypt():
    text = input_text.get("1.0", "end-1c")
    try:
        shift = int(shift_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Shift must be an integer.")
        return

    mode = mode_var.get()
    if mode not in ['encrypt', 'decrypt']:
        messagebox.showerror("Error", "Please choose 'encrypt' or 'decrypt'.")
        return

    result = caesar_cipher(text, shift, mode)
    output_text.delete("1.0", "end")
    output_text.insert("end", result)

def on_enter(event=None):
    action_button.configure(bg="#7c4dff")

def on_leave(event=None):
    action_button.configure(bg="#9575cd")

root = tk.Tk()
root.title("Caesar Cipher - SiddhantJain")
root.configure(background="#ede7f6")
root.geometry("520x460")
root.resizable(False, False)

style = ttk.Style()
style.configure("Custom.TFrame", background="#ede7f6")
style.configure("Custom.TLabel", background="#ede7f6", foreground="#4a148c", font=("Georgia", 12))
style.configure("Custom.TButton", font=("Georgia", 12, "bold"))

main_frame = ttk.Frame(root, padding="25 20 25 20", style="Custom.TFrame")
main_frame.pack(expand=True, fill="both")

ttk.Label(main_frame, text="Message:", style="Custom.TLabel").grid(row=0, column=0, sticky="w")
input_text = tk.Text(main_frame, height=5, width=50, bg="#f3e5f5", fg="#4a148c", font=("Georgia", 11))
input_text.grid(row=1, column=0, columnspan=2, pady=(0, 15))

ttk.Label(main_frame, text="Shift Value:", style="Custom.TLabel").grid(row=2, column=0, sticky="w")
shift_entry = ttk.Entry(main_frame, width=10, font=("Georgia", 11))
shift_entry.grid(row=2, column=1, sticky="w", pady=5)

ttk.Label(main_frame, text="Mode:", style="Custom.TLabel").grid(row=3, column=0, sticky="w")
mode_var = tk.StringVar(value="encrypt")
mode_combobox = ttk.Combobox(main_frame, textvariable=mode_var, values=["encrypt", "decrypt"], width=10, font=("Georgia", 11))
mode_combobox.grid(row=3, column=1, sticky="w", pady=5)

action_button = tk.Button(main_frame, text="Execute", command=encrypt_decrypt,
                          bg="#9575cd", fg="white", font=("Georgia", 12, "bold"), relief="flat")
action_button.grid(row=4, column=0, columnspan=2, pady=15)
action_button.bind("<Enter>", on_enter)
action_button.bind("<Leave>", on_leave)

ttk.Label(main_frame, text="Output:", style="Custom.TLabel").grid(row=5, column=0, sticky="w")
output_text = tk.Text(main_frame, height=5, width=50, bg="#f3e5f5", fg="#4a148c", font=("Georgia", 11))
output_text.grid(row=6, column=0, columnspan=2, pady=(0, 10))

root.mainloop()
