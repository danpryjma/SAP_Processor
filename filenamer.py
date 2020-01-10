import datetime
from tkinter import Tk, filedialog


class FileName:

    """
    Returns the necessary strings for naming files
    with dates and path selection for saving files.
    """

    @staticmethod
    def date():
        now = datetime.datetime.now()
        return f'{now:%Y.%m.%d-}'

    @staticmethod
    def path():
        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory(title='Please select the folder where you\
                                              would like to save the file') + '/'
        return path

    @staticmethod
    def txt_file():
        root = Tk()
        root.withdraw()
        return filedialog.askopenfilename(title='Please select the TXT file downloaded from SAP to process',
                                          filetypes=[('Text Files', ['.txt'])])
