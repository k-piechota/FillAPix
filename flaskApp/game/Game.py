from PyQt5.QtWidgets import QWidget, QMessageBox

from PyQt5.QtGui import QPainter, QBrush

from PyQt5.QtCore import Qt


class Game(QWidget):

    def __init__(self, board):
        super().__init__()

        self.board = board
        self.rows = self.board.rows
        self.columns = self.board.columns

        self.to_draw = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.title = "Fill -a- pix"

        self.top = 150
        self.left = 150
        self.width = 600
        self.height = 600

        self.row_size = self.height / self.rows
        self.column_size = self.width / self.columns
        self._init_window()

    def _init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)

        for i in range(self.rows):
            for k in range(self.columns):
                if self.to_draw[i][k]:
                    painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
                    painter.drawRect(k*self.column_size, i*self.row_size, self.column_size, self.row_size)

        for i in range(self.columns + 1):
            painter.drawLine(i * self.column_size, 0, i * self.column_size, self.height)

        for i in range(self.rows + 1):
            painter.drawLine(0, i * self.row_size, self.width, i * self.row_size)

        for i in range(self.rows):
            for k in range(self.columns):
                painter.drawText(k * self.column_size + (self.column_size/2), i * self.row_size + self.row_size / 2,
                                 str(self.board.complete_board[i][k]))

    def get_cell(self, x, y):
        return int(x / self.column_size), int(y / self.row_size)

    def check_if_correct(self, x, y):
        if self.board.is_painted(x, y):

            if not self.to_draw[y][x]:
                self.to_draw[y][x] = 1
                self.update()
                if self.to_draw == self.board.filled_board:
                    self.show_winner_dialog()
                    self.close()
        else:
            self.show_mistake_dialog()

    def show_mistake_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText('To pole nie jest zamalowane')
        msg.setWindowTitle("Error")
        msg.exec_()

    def show_winner_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Zamalowales wszystkie pola, wygrales')
        msg.setWindowTitle("Wygrales")
        msg.exec_()

    def mousePressEvent(self, event):
        self.check_if_correct(*self.get_cell(event.x(), event.y()))
