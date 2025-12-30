import tkinter as tk
import threading
import time
import json
import os
import sys

from qr_generator import generate_qr
from printer import print_qr


# ---------------- RESOURCE PATH (for EXE support) ---------------- #
def resource_path(relative):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, relative)


# ---------------- LOAD CONFIG ---------------- #
with open(resource_path("config.json")) as f:
    config = json.load(f)

QR_LENGTH = config["qr_length"]
COOLDOWN = config["cooldown_seconds"]
PRINT_ENABLED = config["printer_enabled"]
OUTPUT_FOLDER = config["output_folder"]

running = False
last_text = ""
last_input_time = 0


# ---------------- CONTROL FUNCTIONS ---------------- #
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

        # cooldown (scanner finished typing)
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
            qr_path = generate_qr(text, text)

            if PRINT_ENABLED:
                print_qr(qr_path)

            last_text = text
            status.set("Status: QR Generated Successfully")
            entry.delete(0, tk.END)

        except Exception as e:
            status.set(f"Error: {e}")


# ======================= GUI ======================= #
root = tk.Tk()
root.title("Industrial QR Generator")
root.geometry("900x520")
root.configure(bg="#f2f4f6")
root.resizable(True, True)


# ---------------- HEADER ---------------- #
tk.Label(
    root,
    text="QR Generator",
    font=("Segoe UI", 22, "bold"),
    fg="#1f2933",
    bg="#f2f4f6"
).pack(pady=20)


tk.Label(
    root,
    text="Scan barcode or type text below:",
    font=("Segoe UI", 12),
    fg="#374151",
    bg="#f2f4f6"
).pack()


# ---------------- INPUT ---------------- #
entry = tk.Entry(
    root,
    font=("Consolas", 20),
    width=32,
    relief="solid",
    bd=1
)
entry.pack(pady=16)
entry.bind("<KeyRelease>", on_key_release)


# ---------------- STATUS ---------------- #
status = tk.StringVar(value="Status: Stopped")
tk.Label(
    root,
    textvariable=status,
    fg="#2563eb",
    bg="#f2f4f6",
    font=("Segoe UI", 12, "bold")
).pack(pady=10)


# ---------------- BUTTONS ---------------- #
tk.Button(
    root,
    text="START",
    bg="#15803d",
    fg="white",
    font=("Segoe UI", 14, "bold"),
    height=2,
    activebackground="#166534",
    command=start
).pack(fill="x", padx=160, pady=(20, 10))


tk.Button(
    root,
    text="STOP",
    bg="#b91c1c",
    fg="white",
    font=("Segoe UI", 14, "bold"),
    height=2,
    activebackground="#7f1d1d",
    command=stop
).pack(fill="x", padx=160)


# ---------------- FOOTER ---------------- #
footer = tk.Frame(root, bg="#1f2933", height=38)
footer.pack(side="bottom", fill="x")

tk.Label(
    footer,
    text="Powered by DSAi",
    fg="#e5e7eb",
    bg="#1f2933",
    font=("Segoe UI", 12)
).pack(pady=8)


# ---------------- THREAD ---------------- #
threading.Thread(target=processing_loop, daemon=True).start()
root.mainloop()
