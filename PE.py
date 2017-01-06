import sys
from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainWindow()
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # fix unhandled exception
        #ex.display_error(value)
        print(str(value))
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = my_exception_hook
    sys.exit(app.exec_())
