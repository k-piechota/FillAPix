from json import JSONEncoder


class GameData:
    def __init__(self, board, name):
        self.name = name
        self.board = board
        self.current_state = [[0 for i in range(self.board.columns)] for j in range(self.board.rows)]

    def update(self, column, row):
        self.current_state[row][column] = 1

    def finished(self):
        return True if self.current_state == self.board.filled_board else False

    def get_board(self):
        return self.board


class GameDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
