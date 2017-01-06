import os
import sys


def get_real_path(filename):
    """Нужен для поиска файлов внутри сборки .exe
    смотри https://pythonhosted.org/PyInstaller/runtime-information.html#using-file-and-sys-meipass
    """
    # _MEIPASS - параметр, указывающий путь к распакованному содержимому .exe
    if hasattr(sys, '_MEIPASS'):
        filename = os.path.join(sys._MEIPASS, filename)
    return filename