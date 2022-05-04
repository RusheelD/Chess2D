from Board import Board
from GameControl import GameControl

class MultiGameControl(GameControl):
    def __init__(self):
        self.is_piece_selected = False
        self.selected_piece = None
        self.is_piece_selected_white = False
        self.selected_piece_white = None
        self.white_move = None
        self.black_move = None
        self.is_piece_selected_black = False
        self.selected_piece_black = None
        self.main_board = Board()
        self.white_board = Board()
        self.black_board = Board()
        self.color_to_move = 0
        self.loaded = False

    def select_tile(self, row, column, board: Board=None):
        if(self.main_board.grid[row][column] == None and not(self.is_piece_selected)):
            self.is_piece_selected = False
            self.selected_piece = None

        elif(not(self.is_piece_selected)):
            if(self.main_board.grid[row][column].color != self.color_to_move):
                return None
            self.is_piece_selected = True
            self.selected_piece = self.main_board.grid[row][column]

        elif(self.selected_piece.row == row and self.selected_piece.column == column):
            self.is_piece_selected = False
            self.selected_piece = None

        elif([row, column] in self.selected_piece.get_valid_moves()):
            self.selected_piece.move(row, column)
            self.color_to_move = abs(self.color_to_move - 1)
            self.is_piece_selected = False
            self.selected_piece = None
            self.main_board.update_valid_moves()

        elif(self.main_board.grid[row][column] != None and self.main_board.grid[row][column].color == self.selected_piece.color):
            self.is_piece_selected = True
            self.selected_piece = self.main_board.grid[row][column]

        return self.selected_piece