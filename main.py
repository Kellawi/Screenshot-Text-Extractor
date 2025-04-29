"""
Author: Bashar Kellawi
Helped by: AI Assistant (ChatGPT, OpenAI)
Date: 2025-04-28
Description: 
    This script provides a screen English text extractor tool using OCR (Optical Character Recognition). 
    Users can select a portion of their screen, extract text from it, and manage history. 
    Includes hotkey support (Ctrl+Shift+S) and a tray icon for quick access.

Requirements:
    - Python 3.x
    - Modules: tkinter, ttkbootstrap, pyautogui, pytesseract, pystray, keyboard, pillow, screeninfo, pyperclip
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button
from datetime import datetime
import pytesseract
import pyperclip
import pyautogui
from PIL import Image, ImageTk
import tempfile
import os
from screeninfo import get_monitors
import threading
import keyboard
import pystray
from pystray import MenuItem as item
import sys

# Set the path to the Tesseract executable
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
tesseract_path = os.path.join(base_path, "tesseract", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

class OCRSnipTool:
    def __init__(self, root):
        """Initialize the main OCR tool window and start listeners."""
        self.root = root
        self.root.title("Screen Text Extractor")
        self.style = Style(theme='darkly')  # Set dark theme
        self.root.geometry("900x700")

        self.current_text = tk.StringVar()
        self.history_texts = []  # Store extracted text history

        self.build_gui()

        # Start hotkey listener and tray icon in background threads
        threading.Thread(target=self.start_hotkey_listener, daemon=True).start()
        threading.Thread(target=self.create_tray_icon, daemon=True).start()

    def build_gui(self):
        """Build the main graphical user interface."""
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)

        title = tk.Label(self.frame, text="🧠 Screen Text Extractor", font=("Segoe UI", 20, "bold"), fg="#00ffd0", bg="#1e1e1e")
        title.pack(pady=(0, 20))

        self.capture_btn = Button(self.frame, text="📸 Capture Screen Text", bootstyle="success-outline", command=self.capture_screen)
        self.capture_btn.pack(pady=10, ipadx=10, ipady=5)

        output_lbl = tk.Label(self.frame, text="📝 Extracted Text", font=("Segoe UI", 14, "bold"), fg="white", bg="#1e1e1e")
        output_lbl.pack(anchor='w', padx=5)

        self.output_text = scrolledtext.ScrolledText(self.frame, wrap='word', height=8, font=("Consolas", 12), bg="#2e2e2e", fg="#00ff88", insertbackground='white')
        self.output_text.pack(fill='x', padx=5, pady=(0, 10))

        self.copy_btn = Button(self.frame, text="📋 Copy to Clipboard", bootstyle="info", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=(0, 20), ipadx=8, ipady=4)

        history_lbl = tk.Label(self.frame, text="🕘 History", font=("Segoe UI", 14, "bold"), fg="#ffc400", bg="#1e1e1e")
        history_lbl.pack(anchor='w', padx=5)

        self.history_box = scrolledtext.ScrolledText(self.frame, wrap='word', height=12, font=("Consolas", 10), bg="#252525", fg="lightgray", insertbackground='white')
        self.history_box.pack(fill='both', padx=5, pady=(0, 10), expand=True)
        self.history_box.config(state='disabled')

    def capture_screen(self):
        """Initiate screen capture with selection."""
        snip_window = tk.Toplevel()
        snip_window.attributes('-fullscreen', True)
        snip_window.attributes('-alpha', 0.3)
        snip_window.configure(bg='black')
        snip_window.lift()
        snip_window.attributes("-topmost", True)

        canvas = tk.Canvas(snip_window, cursor="cross", bg='black')
        canvas.pack(fill='both', expand=True)

        rect = None
        start_x = start_y = end_x = end_y = 0

        def cancel_snip(event=None):
            """Cancel the snipping operation."""
            snip_window.destroy()

        def on_mouse_down(event):
            """Start drawing the rectangle."""
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x_root, event.y_root
            rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

        def on_mouse_move(event):
            """Update the selection rectangle as mouse moves."""
            if rect:
                canvas.coords(rect, start_x, start_y, event.x_root, event.y_root)

        def on_mouse_up(event):
            """Finalize the selection and process the snip."""
            nonlocal end_x, end_y
            end_x, end_y = event.x_root, event.y_root
            snip_window.destroy()

            # Determine screen boundaries
            all_monitors = get_monitors()
            min_x = min(m.x for m in all_monitors)
            min_y = min(m.y for m in all_monitors)
            max_x = max(m.x + m.width for m in all_monitors)
            max_y = max(m.y + m.height for m in all_monitors)

            # Capture full screen
            full_img = pyautogui.screenshot(region=(min_x, min_y, max_x - min_x, max_y - min_y))

            # Crop to the selected area
            x1, y1 = min(start_x, end_x) - min_x, min(start_y, end_y) - min_y
            x2, y2 = max(start_x, end_x) - min_x, max(start_y, end_y) - min_y

            cropped = full_img.crop((x1, y1, x2, y2))

            # Show preview and start OCR
            self.show_preview_and_extract(cropped)

        # Bind mouse events
        canvas.bind("<ButtonPress-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_move)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)
        snip_window.bind("<Escape>", cancel_snip)

    def show_preview_and_extract(self, image):
        """Show a preview of the cropped image and extract text."""
        preview = tk.Toplevel(self.root)
        preview.title("Preview Snip")
        preview.geometry("400x300")
        preview.configure(bg="#1e1e1e")

        img_copy = image.copy()
        img_copy.thumbnail((380, 280))
        img_tk = ImageTk.PhotoImage(img_copy)

        panel = tk.Label(preview, image=img_tk, bg="#1e1e1e")
        panel.image = img_tk
        panel.pack(padx=10, pady=10)

        def extract_text():
            """Run OCR on the selected image and update the UI."""
            preview.destroy()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp:
                image.save(temp.name)
                temp_path = temp.name

            # Extract text using Tesseract
            text = pytesseract.image_to_string(Image.open(temp_path))

            # Save previous output to history
            if self.output_text.get("1.0", 'end-1c').strip():
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                history_entry = f"[{timestamp}]\n{self.output_text.get('1.0', 'end-1c').strip()}\n{'-'*60}\n"
                self.history_box.config(state='normal')
                self.history_box.insert('end', history_entry)
                self.history_box.config(state='disabled')

            # Update output
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, text.strip())

            # Automatically copy to clipboard
            pyperclip.copy(text.strip())

            # Cleanup temp file
            os.remove(temp_path)

        confirm = Button(preview, text="🔍 Run OCR", command=extract_text, bootstyle="success-outline")
        confirm.pack(pady=10)

    def copy_to_clipboard(self):
        """Copy current extracted text to clipboard."""
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)

    def start_hotkey_listener(self):
        """Listen for hotkey (Ctrl+Shift+S) to trigger screen capture."""
        keyboard.add_hotkey('ctrl+shift+s', self.capture_screen)

    def create_tray_icon(self):
        """Create a system tray icon with options."""
        def quit_app():
            """Quit the application safely."""
            self.root.quit()
            os._exit(0)

        icon_image = Image.new('RGB', (64, 64), color='black')
        menu = (item('Capture (Ctrl+Shift+S)', self.capture_screen), item('Quit', quit_app))
        tray = pystray.Icon("OCRTool", icon_image, "OCR Snip Tool", menu)
        tray.run()

if __name__ == "__main__":
    # Launch the app
    root = tk.Tk()
    app = OCRSnipTool(root)
    root.mainloop()
