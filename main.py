#!/usr/bin/env python3
from QuickOCR import LanguageSelection, AreaSelection
import pyperclip
LANG = "english"  # default language


def main():

    # create instance and start GUI
    selection_window = LanguageSelection(LANG)
    selection_window.mainloop()

    if selection_window.runOCR:

        # create instance and start GUI
        area_selection = AreaSelection(selection_window.get_lang())
        area_selection.mainloop()

        # copy text to clipboard
        pyperclip.copy(area_selection.get_text())


if __name__ == '__main__':
    main()
