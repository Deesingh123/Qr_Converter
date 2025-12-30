import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

OUTPUT_DIR = "output"

def generate_qr(qr_data: str, track_id: str):
    """
    Generates QR code with Track ID printed below the QR.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    qr_width, qr_height = qr_img.size

    # Reduce space below QR
    text_height = 22
    final_img = Image.new(
        "RGB",
        (qr_width, qr_height + text_height),
        "white"
    )
    final_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(final_img)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # ONLY TRACK ID (no label)
    text = track_id
    text_width = draw.textlength(text, font=font)

    x = (qr_width - text_width) // 2
    y = qr_height-text_height + 2

    draw.text((x, y), text, fill="black", font=font)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{track_id}_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    final_img.save(filepath)

    return filepath
