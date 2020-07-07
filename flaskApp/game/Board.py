from PIL import Image
import PIL


class Board:
    def __init__(self, rows, columns, image):
        self.rows = rows
        self.columns = columns
        self.filled_board = self._create_board(image)
        self.complete_board = self._create_complete_playable_board()

    def _create_board(self, image):
        with Image.open(image, 'r') as img:
            img = img.resize((self.columns, self.rows), PIL.Image.ANTIALIAS)

            fn = lambda x: 0 if x > 200 else 1
            img = img.convert('L').point(fn, mode='1')

            pixels = list(img.getdata())

            new_pixels = []
            for i in range(self.rows):
                lista = []
                for k in range(self.columns):
                    lista.append(pixels[self.columns * i + k])
                new_pixels.append(lista)
            return new_pixels

    def _create_complete_playable_board(self):
        new_board = []

        for i in range(self.rows):
            lista = []
            for k in range(self.columns):
                lista.append(self._sum_neighbors(i, k))
            new_board.append(lista)
        return new_board

    def _sum_neighbors(self, x, y):
        s = 0
        for i in range(max(0, x - 1), x + 2 if x + 2 < self.rows else self.rows):
            for j in range(max(0, y - 1), y + 2 if y + 2 < self.columns else self.columns):
                s += self.filled_board[i][j]
        return s

    def is_painted(self, x, y):
        return True if self.filled_board[y][x] == 1 else False
