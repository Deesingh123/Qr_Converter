import os
import qrcode
from datetime import datetime

def generate_qr(text, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_text = text.replace(" ", "_")
    filename = f"{safe_text}_{timestamp}.png"
    path = os.path.join(output_folder, filename)

    img = qrcode.make(text)
    img.save(path)

    return path
