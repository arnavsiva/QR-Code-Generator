import qrcode
import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageTk
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer

def preview_qr():
    website = entry.get().strip()
    if not website.startswith(("http://", "https://")):
        messagebox.showerror("Invalid URL", "Please enter a valid URL starting with 'http://' or 'https://'.")
        return

    box_size = int(size_entry.get()) if size_entry.get().isdigit() else 10
    border_size = int(border_entry.get()) if border_entry.get().isdigit() else 4
    transparent = transparent_var.get()
    qr_style = qr_style_var.get()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border_size,
    )
    qr.add_data(website)
    qr.make(fit=True)

    module_drawer = {
        "Squares": SquareModuleDrawer(),
        "Rounded Squares": GappedSquareModuleDrawer(),
        "Dots": CircleModuleDrawer()
    }[qr_style]

    if transparent:
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawer, embeded_image_path=None).convert("RGBA")
        img = make_transparent(img)
    else:
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawer, fill_color="black", back_color=bg_color)

    display_qr(img)

    root.last_qr_image = img
    root.transparent = transparent

def save_qr():
    if not hasattr(root, "last_qr_image"):
        messagebox.showerror("Error", "Preview the QR Code first before saving.")
        return

    website = entry.get().strip()
    website_name = website.replace("http://", "").replace("https://", "").split("/")[0]
    filename = f"{website_name}_qrcode.png"

    img = root.last_qr_image

    if root.transparent:
        img.save(filename, format="PNG")
    else:
        img.save(filename)

    messagebox.showinfo("Success", f"QR Code saved as {filename}.")

def make_transparent(img):
    img = img.convert("RGBA")
    pixels = img.getdata()

    new_pixels = []
    for pixel in pixels:
        if pixel[:3] == (255, 255, 255):
            new_pixels.append((255, 255, 255, 0))
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    return img

def display_qr(img):
    img = img.resize((200, 200))
    qr_img = ImageTk.PhotoImage(img)

    if hasattr(root, "qr_label"):
        root.qr_label.destroy()

    root.qr_label = tk.Label(root, image=qr_img)
    root.qr_label.image = qr_img
    root.qr_label.pack(pady=10)

def choose_bg_color():
    global bg_color
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        bg_color = color

def reset_ui():
    entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)
    border_entry.delete(0, tk.END)
    size_entry.insert(0, "10")
    border_entry.insert(0, "4")
    transparent_var.set(0)
    qr_style_var.set("Squares")

    if hasattr(root, "qr_label"):
        root.qr_label.destroy()

    if hasattr(root, "last_qr_image"):
        del root.last_qr_image

root = tk.Tk()
root.title("Custom QR Code Generator")

tk.Label(root, text="Enter Website URL:", font=("Arial", 12)).pack(pady=5)
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

tk.Label(root, text="Box Size (QR Code Size):", font=("Arial", 10)).pack(pady=2)
size_entry = tk.Entry(root, width=10, font=("Arial", 10))
size_entry.insert(0, "10")
size_entry.pack(pady=2)

tk.Label(root, text="Border Size:", font=("Arial", 10)).pack(pady=2)
border_entry = tk.Entry(root, width=10, font=("Arial", 10))
border_entry.insert(0, "4")
border_entry.pack(pady=2)

bg_color = "white"
bg_button = tk.Button(root, text="Choose Background Color", command=choose_bg_color, font=("Arial", 10))
bg_button.pack(pady=5)

transparent_var = tk.IntVar()
transparent_checkbox = tk.Checkbutton(root, text="Transparent Background", variable=transparent_var, font=("Arial", 10))
transparent_checkbox.pack(pady=5)

tk.Label(root, text="Select QR Code Style:", font=("Arial", 10)).pack(pady=2)
qr_style_var = tk.StringVar(value="Squares")
qr_style_dropdown = tk.OptionMenu(root, qr_style_var, "Squares", "Rounded Squares", "Dots")
qr_style_dropdown.pack(pady=5)

preview_button = tk.Button(root, text="Preview QR Code", command=preview_qr, font=("Arial", 12))
preview_button.pack(pady=10)

save_button = tk.Button(root, text="Save QR Code", command=save_qr, font=("Arial", 12))
save_button.pack(pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_ui, font=("Arial", 10))
reset_button.pack(pady=5)

root.mainloop()
