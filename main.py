import tkinter as tk
import threading
import time
import json
import os
import sys

from qr_generator import generate_qr
from printer import print_qr


def resource_path(relative):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, relative)


with open(resource_path("config.json")) as f:
    config = json.load(f)

QR_LENGTH = config["qr_length"]
COOLDOWN = config["cooldown_seconds"]
PRINT_ENABLED = config["printer_enabled"]
OUTPUT_FOLDER = config["output_folder"]

running = False
last_text = ""
last_input_time = 0


def start():
    global running
    running = True
    status.set("Status: Running")
    entry.focus()


def stop():
    global running
    running = False
    status.set("Status: Stopped")


def on_key_release(event=None):
    global last_input_time
    last_input_time = time.time()


def processing_loop():
    global last_text

    while True:
        time.sleep(0.2)

        if not running:
            continue

        text = entry.get().strip()
        if not text:
            continue

        if time.time() - last_input_time < COOLDOWN:
            continue

        if len(text) != QR_LENGTH:
            status.set(f"Status: Invalid length (need {QR_LENGTH})")
            entry.delete(0, tk.END)
            continue

        if text == last_text:
            status.set("Status: Duplicate ignored")
            entry.delete(0, tk.END)
            continue

        try:
            qr_path = generate_qr(text, OUTPUT_FOLDER)

            if PRINT_ENABLED:
                print_qr(qr_path)

            last_text = text
            status.set("Status: QR Generated")
            entry.delete(0, tk.END)

        except Exception as e:
            status.set(f"Error: {e}")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Industrial QR Generator")
root.geometry("420x280")

tk.Label(root, text="Industrial QR Generator",
         font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Scan barcode or type text below:").pack()

entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack(pady=10)
entry.bind("<KeyRelease>", on_key_release)

status = tk.StringVar(value="Status: Stopped")
tk.Label(root, textvariable=status, fg="blue").pack(pady=5)

tk.Button(root, text="Start", bg="green", fg="white",
          font=("Arial", 12), command=start).pack(fill="x", padx=50, pady=5)

tk.Button(root, text="Stop", bg="red", fg="white",
          font=("Arial", 12), command=stop).pack(fill="x", padx=50)

threading.Thread(target=processing_loop, daemon=True).start()
root.mainloop()
