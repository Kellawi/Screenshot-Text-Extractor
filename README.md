# 🧠 Screen Text Extractor

> Quickly capture text from anywhere on your screen using powerful OCR technology!

---

## 📖 Overview

**Screen Text Extractor** is a lightweight tool that lets you **select any part of your screen** and **extract the text inside** using **OCR (Optical Character Recognition)**.

✨ Built for simplicity and speed: just a click or a hotkey, and your text is ready to be copied, saved, or used.

**Good news:**  
- It works for **English** and **many other languages** depending on what Tesseract detects!
- You **don't need to install Tesseract separately** — everything is bundled inside the app.

---

## 🎯 Key Features

- 🖱️ **Select and Capture** any screen area with a simple mouse drag.
- 🔠 **Extract Text** instantly from the selected region.
- 📋 **Copy to Clipboard** with one click.
- 🕘 **View History** of previous extractions.
- ⚡ **Hotkey Support** (`Ctrl+Shift+S`) for instant capture.
- 🛎️ **System Tray Icon** for quick access and control.
- 📦 **One EXE File** — no Python installation or Tesseract setup needed!

---

## 📂 Project Structure

/ScreenTextExtractor/ ├── main.py # Main Python application ├── requirements.txt # List of required Python modules ├── icon.ico # Icon for the executable ├── /tesseract/ # Local Tesseract OCR engine │ └── tesseract.exe


---

## 🛠 How to Set Up and Run

### 1. Install Python Modules

Make sure you have **Python 3.x** installed.  
Then open a terminal (or Command Prompt) in the project folder and run:

```bash
pip install -r requirements.txt
