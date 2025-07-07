# Aengus Patterson, July 2025
# MIT License
# Converts from one format to another with a Tkinter GUI

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font
import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


#prompts the user to enter a file format to be exported to
def open_format_dialog():
    def set_box(fmt):
        entry.delete(0, tk.END)
        entry.insert(0, fmt)

    def confirm():
        chosen_format = entry.get().strip().lower()
        if chosen_format:
            format_var.set(chosen_format)
            set_format(chosen_format)
        dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Select Output Format")
    dialog.geometry("400x250")

    tk.Label(dialog, text="Enter or select a picture format:").pack(pady=5)

    entry = tk.Entry(dialog)
    entry.pack(pady=5)
    entry.focus()

    # Common format buttons
    preset_frame = tk.Frame(dialog)
    preset_frame.pack(pady=5)

    for idx, fmt in enumerate(["png", "jpg", "webp", "gif", "bmp", "pdf"]):
        tk.Button(preset_frame, text=fmt, width=5, command=lambda f=fmt: set_box(f)).grid(row=0, column=idx, padx=2)
    
    note_font = font.Font(family="Helvetica", size=9, slant="italic")
    
    supported_formats = "Supported: avif, blp, bmp, dds, dib, eps, gif, heic, icns, ico,\nim, jpg/jpeg, jpeg 2000, mpo, msp, pcx, pfm,\npng, ppm, qoi, sgi, spider, tga, tiff, webp, and xbm.\nSee Python's Pillow and Pillow-HEIF for more information."
    tk.Label(dialog, text=supported_formats, font=note_font, fg="gray").pack(pady=6)

    tk.Button(dialog, text="OK", command=confirm, bg="#4CAF50", fg="white").pack(pady=10)

#prompts the user to select files to be converted
def select_input_files():
    input_label.config(text="Select input files...")
    root.update()
    files = filedialog.askopenfilenames()
    input_label.config(text=f"{len(files)} file(s) selected.")
    global input_files
    input_files = files

#prompts for an output folder
def select_output_folder():
    output_label.config(text="Select output folder...")
    root.update()
    folder = filedialog.askdirectory()
    output_label.config(text=folder or "No folder selected.")
    global output_folder
    output_folder = folder

#sets the format for the images and updates the format label text
def set_format(fmt):
    format_var.set(fmt)
    format_label.config(text="Current selected output format: " + fmt)

def convert_files():
    #check if the user has selected which files to input
    try:
        if not input_files:
            messagebox.showerror("Error", "No input files selected.")
            return
    except:
        messagebox.showerror("Error", "No input files selected.")
        return

    #check if the user has selected an output folder
    try:
        if not output_folder:
            messagebox.showerror("Error", "No output folder selected.")
            return
    except: 
        messagebox.showerror("Error", "No output folder selected.")
        return

    file_format = format_var.get()
    if not file_format:
        messagebox.showerror("Error", "No output format selected.")
        return

    try:
        quality = int(quality_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid quality value.")
        return

    try:
        rotation = int(rotation_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid rotation value.")
        return

    lossless = quality == 100

    for path in input_files:
        try:
            img = Image.open(path)
            img = img.rotate(rotation, expand=True)
            base_name = os.path.splitext(os.path.basename(path))[0]
            out_path = os.path.join(output_folder, f"{base_name}.{file_format}")
            img.save(out_path, method=6 if file_format == "webp" else None, lossless=lossless, quality=quality)
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to process {path}:\n{e}")

    messagebox.showinfo("Done", "Conversion completed!")

# GUI Setup
root = tk.Tk()
root.geometry("600x500")
root.title("Aengus\'s converter")

#global var for file format
format_var = tk.StringVar(value="png")

#intro paragraph
note_font = font.Font(family="Helvetica", size=9, slant="italic")
tk.Label(root, text="Aengus\'s converter (v1.0, MIT license) is a simple image converter made in python. Learn more at \nhttps://aenguspatterson.com/pages/projects/A-Simple-Offline-File-Converter/ ", font=note_font).pack(pady=5)

# --- Quality Input ---
quality_frame = tk.Frame(root)
quality_frame.pack(pady=5, anchor="w", padx=10)

tk.Label(quality_frame, text="Quality (100 = lossless):", width=30, anchor="w").pack(side=tk.LEFT)
quality_entry = tk.Entry(quality_frame, width=17)
quality_entry.insert(0, "100")
quality_entry.pack(side=tk.LEFT, padx=10)

# --- Rotation Input ---
rotation_frame = tk.Frame(root)
rotation_frame.pack(pady=5, anchor="w", padx=10)

tk.Label(rotation_frame, text="Rotation angle (deg counterclockwise):", width=30, anchor="w").pack(side=tk.LEFT)
rotation_entry = tk.Entry(rotation_frame, width=17)
rotation_entry.insert(0, "0")
rotation_entry.pack(side=tk.LEFT, padx=10)


# --- Format Selection ---
format_frame = tk.Frame(root)
format_frame.pack(pady=5, anchor="w", padx=10)

format_label = tk.Label(format_frame, text="Current selected output format: " + format_var.get(), width=30, anchor="w")
format_label.pack(side=tk.LEFT)

tk.Button(format_frame, text="Choose Format", command=open_format_dialog, bg="#4CAF50", fg="white", width=17).pack(side=tk.LEFT, padx=10)

# --- Input Files ---
input_frame = tk.Frame(root)
input_frame.pack(pady=5, anchor="w", padx=10)

input_label = tk.Label(input_frame, text="No input files selected.", width=30, anchor="w")
input_label.pack(side=tk.LEFT)

tk.Button(input_frame, text="Select input file(s)", command=select_input_files, bg="#4CAF50", fg="white", width=17).pack(side=tk.LEFT, padx=10)

# --- Output Folder ---
output_frame = tk.Frame(root)
output_frame.pack(pady=5, anchor="w", padx=10)

output_label = tk.Label(output_frame, text="No output folder selected.", width=30, anchor="w", )
output_label.pack(side=tk.LEFT)

tk.Button(output_frame, text="Select output folder", command=select_output_folder, bg="#4CAF50", fg="white", width=17).pack(side=tk.LEFT, padx=10)


#initiate the conversion
tk.Button(root, text="Convert!", command=convert_files, bg="#4C4EAF", fg="white", width=47).pack(side=tk.LEFT, pady=10, padx=10)

root.mainloop()
