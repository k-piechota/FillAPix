from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox
from game import Board, Game


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.pushButton_2 = QPushButton('Graj', self)
        self.label = QLabel('Brak pliku', self)
        self.pushButton = QPushButton('Wybierz plik', self)
        self.filename = ''

        self.label_columns = QLabel('Liczba kolumn:', self)
        self.textbox_columns = QLineEdit(self)
        self.label_rows = QLabel('Liczba wierszy:', self)
        self.textbox_rows = QLineEdit(self)

        self.top = 150
        self.left = 150
        self.width = 550
        self.height = 100

        self.setup()

    def setup(self):
        self.setWindowTitle('Menu')
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.pushButton.setGeometry(QtCore.QRect(310, 60, 75, 23))
        self.label.setGeometry(QtCore.QRect(20, 60, 290, 21))
        self.pushButton_2.setGeometry(QtCore.QRect(410, 60, 75, 23))
        self.pushButton.clicked.connect(self.on_click)
        self.pushButton_2.clicked.connect(self.on_click_play)

        self.label_columns.move(20, 25)
        self.textbox_columns.move(100, 30)
        self.textbox_columns.resize(30, 20)

        self.label_rows.move(150, 25)
        self.textbox_rows.move(230, 30)
        self.textbox_rows.resize(30, 20)

    def on_click(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Image file', QtCore.QDir.rootPath(),
                                                                 '*.jpg *.png')
        self.label.setText(self.filename)

    def on_click_play(self):
        columns = 0
        rows = 0

        try:
            columns = int(self.textbox_columns.text())
            rows = int(self.textbox_columns.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Liczba kolumn i wierszy muszą być liczbami całkowitymi')
            msg.setWindowTitle("Error")
            msg.exec_()

        if self.filename and self.filename != 'Brak pliku' and columns > 0 and rows > 0:
            board = Board.Board(int(self.textbox_rows.text()), int(self.textbox_columns.text()), self.filename)
            self.ui = Game.Game(board)
            self.ui.show()
            self.hide()
