import sys
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(title="Server",is_server=True)
    window.show()
    sys.exit(app.exec_())
