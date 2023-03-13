<img src="./logo/quick_ocr_logo.svg" width="120px" alt="QuickOCR Logo">

# QuickOCR
A simple OCR tool implemented in Python using tesseract that allows you to copy text from a selected area of the screen to the clipboard.

## Prerequisites
`pip3 install pyperclip pynput pytesseract tk pynput`

## Installation
I suggest to store the project files in `~/bin/quick-ocr/`.
Make sure that the `main.py` file is executable (`chmod +x main.py`).
Then you can assign a shortcut in the settings as follows: `~/bin/quick-ocr/main.py` (with a custom shortcut like `Win + Shift + T`).

## MacOS
You need to give the script permission to access the screen. You can do this by going to `System Preferences > Security & Privacy > Privacy > Accessibility` and adding the script to the list.

## Note
It may be necessary to install tkinter on your system. For example, on Ubuntu you can do this with `sudo apt install tk`.