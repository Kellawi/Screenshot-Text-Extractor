# 🧠 Screenshot Text Extractor

> Quickly capture text from anywhere on your screen using powerful OCR technology!

---

## 📖 Overview

**Screenshot Text Extractor** is a lightweight tool that lets you **select any part of your screen** and **extract the text inside** using **OCR (Optical Character Recognition)**.

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

/ScreenshotTextExtractor/ 
    ├── main.py # Main Python application.
    ├── requirements.txt # List of required Python modules. 
    ├── icon.ico # Icon for the executable. 
    ├── /tesseract/ # Local Tesseract OCR engine. 
    │ └── tesseract.exe

---

## 🛠 How to Set Up and Run

### 1. Install Python Modules

Make sure you have **Python 3.x** installed.  
Then open a terminal (or Command Prompt) in the project folder and run:

```bash
pip install -r requirements.txt
```
This will install all necessary modules.

### 2. Run the Application
After installing, start the app by running:

```bash
python main.py
```
✅ You can now:

- Press Ctrl+Shift+S to capture a screen region.

- Extract text automatically.

- Copy or view the text in the history panel.

## 🔨 How to Build a Standalone EXE
You can turn this project into a single .exe file — no Python or Tesseract installation required!

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build the EXE
From your project directory, run:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --add-data "tesseract;tesseract" main.py
```
### Explanation:

- **--onefile** → Combines all code and assets into a single .exe

- **--windowed** → Hides the console window (GUI only)

- **--icon=icon.ico** → Adds your custom icon

- **--add-data** → Bundles the local tesseract/ folder

### ✅ Your executable will be saved in:

```bash
/dist/main.exe
```

Just double-click it on any Windows machine!

### 📌 This app works with anything Tesseract can recognize:

- English

- Numbers

- Symbols

### 💬 Why Use This?
- 🚀 Ultra lightweight and fast

- 🔒 Fully offline (no internet needed)

- 🛡️ No tracking or data collection

- 🎯 Perfect for quick daily use, devs, writers, students

### 🤝 Credits
### Author: Bashar Kellawi

### AI Assistant: ChatGPT (OpenAI)
