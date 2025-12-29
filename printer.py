import win32print
import win32ui
from PIL import Image, ImageWin

def has_real_printer():
    try:
        printer = win32print.GetDefaultPrinter().lower()
        virtual = ["pdf", "onenote", "xps"]
        return not any(v in printer for v in virtual)
    except:
        return False

def print_qr(image_path):
    if not has_real_printer():
        print("⚠ No physical printer detected. Skipping print.")
        return

    printer_name = win32print.GetDefaultPrinter()
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    img = Image.open(image_path)
    dib = ImageWin.Dib(img)

    hdc.StartDoc("QR Print")
    hdc.StartPage()
    dib.draw(hdc.GetHandleOutput(), (0, 0, img.width, img.height))
    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()
