import threading
from scapy.all import sniff, IP, Raw
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task5 - Siddhant Jain")
        self.root.configure(bg="#ffe6f9")
        self.running = False
        self.sniffer_thread = None
        self.captured_packets = set()

        self.header = tk.Label(
            root,
            text="Packet Sniffer",
            font=("Helvetica", 16, "bold"),
            bg="#ffe6f9",
            fg="#80005c"
        )
        self.header.pack(pady=(10, 5))

        self.text_frame = tk.Frame(root, bg="#ffe6f9")
        self.text_frame.pack(padx=10, pady=(0, 10), expand=True, fill="both")

        self.text_box = tk.Text(
            self.text_frame,
            bg="#2b002b",
            fg="#fce4f9",
            font=("Consolas", 10),
            insertbackground="#ffffff",
            borderwidth=2,
            relief="sunken",
            wrap="word"
        )
        self.text_box.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.text_frame,
            orient="vertical",
            command=self.text_box.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.text_box.configure(yscrollcommand=self.scrollbar.set)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar", background="#ffb3e6", troughcolor="#ffe6f9", arrowcolor="#80005c")

        self.button = tk.Button(
            root,
            text="Start Sniffing",
            command=self.toggle_sniffing,
            bg="#b30086",
            fg="white",
            font=("Helvetica", 12, "bold"),
            activebackground="#80005c",
            padx=10,
            pady=5
        )
        self.button.pack(pady=(0, 15))

    def toggle_sniffing(self):
        if not self.running:
            self.running = True
            self.button.config(text="Stop Sniffing", bg="#e6005c", activebackground="#99003d")
            self.sniffer_thread = threading.Thread(target=self.start_sniffing, daemon=True)
            self.sniffer_thread.start()
        else:
            self.running = False
            self.button.config(text="Start Sniffing", bg="#b30086", activebackground="#80005c")

    def start_sniffing(self):
        sniff(prn=self.packet_callback, store=False, stop_filter=lambda x: not self.running)

    def packet_callback(self, packet):
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
            proto = packet[IP].proto
            payload = packet[Raw].load if Raw in packet else b''

            unique_key = f"{src}->{dst}|{proto}|{payload[:20]}"
            if unique_key in self.captured_packets:
                return
            self.captured_packets.add(unique_key)

            info = (
                f"Source IP: {src}\n"
                f"Destination IP: {dst}\n"
                f"Protocol: {proto}\n"
                f"Payload: {payload}\n"
                f"{'-'*80}\n"
            )
            self.text_box.insert(tk.END, info)
            self.text_box.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x650")
    app = PacketSnifferApp(root)
    root.mainloop()
