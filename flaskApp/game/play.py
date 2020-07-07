import sys
from PyQt5.QtWidgets import QApplication
from game.Menu import Menu


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec())
