from QuickOCR import LanguageSelection, AreaSelection
import pyperclip
LANG = "english"  # default language


def main():

    # create instance
    quick_ocr = LanguageSelection(LANG)
    quick_ocr.mainloop()

    area_selection = AreaSelection(quick_ocr.get_lang())
    area_selection.mainloop()

    # copy text to clipboard
    pyperclip.copy(area_selection.get_text())


if __name__ == '__main__':
    main()
