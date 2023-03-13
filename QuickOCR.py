from tkinter import *
import pytesseract
from pynput.mouse import Listener

import os
import random
import string

from PIL import ImageGrab, Image


class LanguageSelection:
    """language selection window"""

    def __init__(self, lang):
        """
        constructor
        :param lang: language
        """
        self._lang = lang[0:3]  # set language
        # create instance
        self._lang_selection_window = Tk()
        self._lang_selection_window.title("Quick OCR")  # add a title
        self._lang_selection_window.resizable(False, False)  # disable resizing the GUI by passing in False/False
        self._lang_selection_window.geometry('200x50')  # set window size

        # set icon
        self._lang_selection_window.iconphoto(False, PhotoImage(file='logo/quick_ocr_logo.png'))

        # create a dropdown menu
        self._language_drop_down = StringVar()
        self._language_drop_down.set(lang)
        _drop_down_menu = OptionMenu(
            self._lang_selection_window,
            self._language_drop_down,
            "chinese",
            "english",
            "french",
            "deutsch",
            "italian",
            "japanese",
            "polish",
            "russian",
            "spanish",
            "ukrainian",
        )
        _drop_down_menu.grid(column=0, row=0, pady=10)
        self._language_drop_down.trace('w', self.change_dropdown)  # link function to change dropdown

        _ocr_button = Button(self._lang_selection_window, text="OCR", command=self.btn_click, width=10)
        _ocr_button.grid(column=1, row=0, pady=10)

    def mainloop(self):
        """start tkinter window"""
        self._lang_selection_window.mainloop()

    def get_lang(self):
        """get language"""
        return self._lang

    def change_dropdown(self, *args):
        """event listener for dropdown menu on change"""
        self._lang = self._language_drop_down.get()[0:3]

    def btn_click(self):
        """event listener for button click"""
        self._lang_selection_window.destroy()


class AreaSelection:
    """area selection window"""

    def __init__(self, lang):
        """
        constructor
        :param lang: language
        """
        self.lang = lang
        self._text = ""
        self.root = Tk()
        self.clicked_x = 0
        self.clicked_y = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.draw_selection_area = False

        # Get the current screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Sets geometric string argument as string value, e.g. 800x600
        self.root.geometry(str(self.screen_width) + 'x' + str(self.screen_height))

        self.root.overrideredirect(True)  # Remove window border
        self.root.wait_visibility(self.root)  # Remove window from taskbar
        self.root.wm_attributes("-alpha", 0.3)  # Set windows transparent

        self.canvas = Canvas(self.root, width=self.screen_width, height=self.screen_height)  # Crate canvas
        self.canvas.config(cursor="cross")  # Change mouse pointer to cross
        self.canvas.pack()

    def mainloop(self):
        """start tkinter window"""

        # collect events until released
        with Listener(on_move=self.on_move, on_click=self.on_click) as listener:
            self.root.mainloop()  # Start tkinter window
            listener.join()

    def on_click(self, x, y, button, pressed):
        """
        event listener for mouse click
        :param x: x coordinate
        :param y: y coordinate
        :param button: mouse button
        :param pressed: pressed or released
        :return:
        """
        if button == button.left:

            # Left button pressed then continue
            if pressed:
                self.draw_selection_area = True
                self.clicked_x = x
                self.clicked_y = y
            else:
                self.draw_selection_area = False
                self.root.wm_attributes('-alpha', 0)
                self.root.quit()  # Remove tkinter window
                self.ocr_image(x, y)

        if not pressed:
            return False  # Stop listener

    # Start and End mouse position
    def on_move(self, x, y):
        if self.draw_selection_area:

            # draw rectangle on canvas as mouse moves and remove alpha from selection area
            self.canvas.delete("all")  # Remove previous rectangle
            self.canvas.create_rectangle(
                self.clicked_x, self.clicked_y, x, y, outline='red', width=1, fill='red')

    def ocr_image(self, x, y):
        """ocr image"""

        # swap coordinates if user drags from bottom right to top left
        if self.clicked_x > x:
            self.clicked_x, x = x, self.clicked_x
        if self.clicked_y > y:
            self.clicked_y, y = y, self.clicked_y

        img = ImageGrab.grab(bbox=(self.clicked_x, self.clicked_y, x, y))  # Take the screenshot

        # random tmp image name
        random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
        path = f'/tmp/{random_string}.png'

        img.save(path)
        img = Image.open(path)
        text = pytesseract.image_to_string(img, lang=self.lang)  # Run tesseract OCR on image
        self._text = text

        # delete screenshot
        os.remove(path)

    def get_text(self):
        """get text"""
        return self._text
