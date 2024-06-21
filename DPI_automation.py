import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def increase_dpi(image_path, output_path, dpi=1200):
    try:
        with Image.open(image_path) as img:
            img.save(output_path, dpi=(dpi, dpi))
        print(f"Saved {output_path} with {dpi} DPI")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def select_folder_and_process_images():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder = os.path.join(folder_selected, "output")
        os.makedirs(output_folder, exist_ok=True)
        for root, _, files in os.walk(folder_selected):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    image_path = os.path.join(root, file)
                    relative_path = os.path.relpath(image_path, folder_selected)
                    output_path = os.path.join(output_folder, relative_path)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    increase_dpi(image_path, output_path)
    else:
        print("No folder selected")

if __name__ == "__main__":
    select_folder_and_process_images()
