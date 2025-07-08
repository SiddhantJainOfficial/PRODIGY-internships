import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

app = tk.Tk()
app.title("Task 2 - Siddhant Jain")
app.geometry("1000x720")
app.configure(bg="#e6ecf0")

# Panels
input_panel = None
output_panel = None
image_path = None
original_image = None
encrypted_data = None
encryption_key = None

def load_image():
    global image_path, input_panel, output_panel, original_image
    file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not file:
        messagebox.showinfo("Notice", "No image selected.")
        return
    image_path = file
    original_image = Image.open(file)
    preview = ImageTk.PhotoImage(original_image.resize((400, 300)))
    
    if input_panel is None:
        input_panel = tk.Label(image=preview, bg="#ffffff", borderwidth=2, relief="groove")
        input_panel.image = preview
        input_panel.grid(row=1, column=0, padx=20, pady=10)
        
        output_panel = tk.Label(image=preview, bg="#ffffff", borderwidth=2, relief="groove")
        output_panel.image = preview
        output_panel.grid(row=1, column=1, padx=20, pady=10)
    else:
        input_panel.configure(image=preview)
        input_panel.image = preview
        output_panel.configure(image=preview)
        output_panel.image = preview

def perform_encryption():
    global encrypted_data, encryption_key, image_path, output_panel
    if not image_path:
        messagebox.showwarning("Error", "Please load an image first.")
        return
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = img.astype(float) / 255.0
    encryption_key = np.random.normal(0, 0.1, img.shape) + np.finfo(float).eps
    encrypted_data = img / encryption_key
    cv2.imwrite("encrypted_temp.jpg", encrypted_data * 255)

    img_display = Image.open("encrypted_temp.jpg")
    display = ImageTk.PhotoImage(img_display.resize((400, 300)))
    output_panel.configure(image=display)
    output_panel.image = display
    messagebox.showinfo("Done", "Encryption successful.")

def perform_decryption():
    global encrypted_data, encryption_key, output_panel
    if encrypted_data is None or encryption_key is None:
        messagebox.showerror("Error", "Nothing to decrypt.")
        return
    result = encrypted_data * encryption_key
    result *= 255.0
    cv2.imwrite("decrypted_temp.jpg", result)
    img_display = Image.open("decrypted_temp.jpg")
    display = ImageTk.PhotoImage(img_display.resize((400, 300)))
    output_panel.configure(image=display)
    output_panel.image = display
    messagebox.showinfo("Success", "Decryption completed.")

def restore_image():
    global original_image, output_panel
    if original_image:
        preview = ImageTk.PhotoImage(original_image.resize((400, 300)))
        output_panel.configure(image=preview)
        output_panel.image = preview
        messagebox.showinfo("Reset", "Image view reset.")
    else:
        messagebox.showwarning("Warning", "No image loaded.")

def export_snapshot():
    if original_image:
        file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
        if file:
            original_image.save(file)
            messagebox.showinfo("Saved", "Snapshot saved successfully.")
    else:
        messagebox.showwarning("Warning", "No content to export.")

def quit_app():
    if messagebox.askyesno("Exit", "Close this application?"):
        app.destroy()

# Header
tk.Label(app, text="SPOOFING Image Tool", font=("Helvetica", 28, "bold"), bg="#e6ecf0", fg="#2c3e50").grid(row=0, column=0, columnspan=2, pady=10)

# Controls Frame
controls = tk.Frame(app, bg="#e6ecf0")
controls.grid(row=2, column=0, columnspan=2, pady=20)

tk.Button(controls, text="Import Image", command=load_image, font=("Helvetica", 14), bg="#b2bec3", fg="#2d3436", width=15).grid(row=0, column=0, padx=10)
tk.Button(controls, text="Encrypt", command=perform_encryption, font=("Helvetica", 14), bg="#74b9ff", fg="white", width=12).grid(row=0, column=1, padx=10)
tk.Button(controls, text="Decrypt", command=perform_decryption, font=("Helvetica", 14), bg="#00cec9", fg="white", width=12).grid(row=0, column=2, padx=10)
tk.Button(controls, text="Reset View", command=restore_image, font=("Helvetica", 14), bg="#ffeaa7", fg="black", width=12).grid(row=0, column=3, padx=10)
tk.Button(controls, text="Save Copy", command=export_snapshot, font=("Helvetica", 14), bg="#55efc4", fg="black", width=12).grid(row=0, column=4, padx=10)
tk.Button(controls, text="Exit", command=quit_app, font=("Helvetica", 14), bg="#d63031", fg="white", width=10).grid(row=0, column=5, padx=10)

app.protocol("WM_DELETE_WINDOW", quit_app)
app.mainloop()
