import sys
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(title="Client", is_server=False)
    window.show()
    sys.exit(app.exec_())
