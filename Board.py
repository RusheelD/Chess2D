import pyglet
from Pieces import *

class Board(object):
    
    def __init__(self):
        pieces_images = pyglet.image.load('Pieces-Images.png')

        Black_King_Image = pieces_images.get_region(0, 0, 200, 200)
        White_King_Image = pieces_images.get_region(0, 200, 200, 200)
        Black_Queen_Image = pieces_images.get_region(200, 0, 200, 200)
        White_Queen_Image = pieces_images.get_region(200, 200, 200, 200)
        Black_Bishop_Image = pieces_images.get_region(400, 0, 200, 200)
        White_Bishop_Image = pieces_images.get_region(400, 200, 200, 200)
        Black_Knight_Image = pieces_images.get_region(600, 0, 200, 200)
        White_Knight_Image = pieces_images.get_region(600, 200, 200, 200)
        Black_Rook_Image = pieces_images.get_region(800, 0, 200, 200)
        White_Rook_Image = pieces_images.get_region(800, 200, 200, 200)
        Black_Pawn_Image = pieces_images.get_region(1000, 0, 200, 200)
        White_Pawn_Image = pieces_images.get_region(1000, 200, 200, 200)

        self.black_images = [Black_Pawn_Image, Black_Rook_Image, Black_Knight_Image, 
        Black_Bishop_Image, Black_Queen_Image, Black_King_Image]

        self.white_images = [White_Pawn_Image, White_Rook_Image, White_Knight_Image, 
        White_Bishop_Image, White_Queen_Image, White_King_Image]

        self.current_turn = 1
        self.moves_made = []
        self.pieces = [Rook(self.white_images[1], 0, 0, 0, self), Knight(self.white_images[2], 0, 1, 0, self), 
        Bishop(self.white_images[3], 0, 2, 0, self), Queen(self.white_images[4], 0, 3, 0, self), 
        King(self.white_images[5], 0, 4, 0, self), Bishop(self.white_images[3], 0, 5, 0, self), 
        Knight(self.white_images[2], 0, 6, 0, self), Rook(self.white_images[1], 0, 7, 0, self), 
        Pawn(self.white_images[0], 1, 0, 0, self), Pawn(self.white_images[0], 1, 1, 0, self), 
        Pawn(self.white_images[0], 1, 2, 0, self), Pawn(self.white_images[0], 1, 3, 0, self), 
        Pawn(self.white_images[0], 1, 4, 0, self), Pawn(self.white_images[0], 1, 5, 0, self), 
        Pawn(self.white_images[0], 1, 6, 0, self), Pawn(self.white_images[0], 1, 7, 0, self), 
        Pawn(self.black_images[0], 6, 0, 1, self), Pawn(self.black_images[0], 6, 1, 1, self), 
        Pawn(self.black_images[0], 6, 2, 1, self), Pawn(self.black_images[0], 6, 3, 1, self), 
        Pawn(self.black_images[0], 6, 4, 1, self), Pawn(self.black_images[0], 6, 5, 1, self), 
        Pawn(self.black_images[0], 6, 6, 1, self), Pawn(self.black_images[0], 6, 7, 1, self), 
        Rook(self.black_images[1], 7, 0, 1, self), Knight(self.black_images[2], 7, 1, 1, self), 
        Bishop(self.black_images[3], 7, 2, 1, self), Queen(self.black_images[4], 7, 3, 1, self), 
        King(self.black_images[5], 7, 4, 1, self), Bishop(self.black_images[3], 7, 5, 1, self), 
        Knight(self.black_images[2], 7, 6, 1, self), Rook(self.black_images[1], 7, 7, 1, self)]
        self.grid = [[None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None]]
        self.refresh_pieces()

    def __str__(self):
        string = ""
        for row in self.grid:
            for piece in row:
                string += str(piece)
                string += "\t"
                string += "\t" if piece == None else ""
            string += "\n"
        return string
    
    def refresh_pieces(self):
        for piece in self.pieces:
            self.grid[piece.row][piece.column] = piece

    def copy(self, board):
        self.grid = board.grid

    def get_white_king_pos(self):
        return King.White_King_Pos
    
    def get_black_king_pos(self):
        return King.Black_King_Pos

    def update_valid_moves(self):
        white_pos = self.get_white_king_pos()
        black_pos = self.get_black_king_pos()
        self.grid[white_pos[0]][white_pos[1]] = King(self.white_images[5], white_pos[0], white_pos[1], 0, self)
        self.grid[black_pos[0]][black_pos[1]] = King(self.black_images[5], black_pos[0], black_pos[1], 1, self)
        self.get(white_pos).steps_taken = King.White_King_Moves
        self.get(black_pos).steps_taken = King.Black_King_Moves
        for row in self.grid:
            for piece in row:
                if(piece != None):
                    piece.update_valid_moves()
        self.refresh_pieces()

    def get(self, pos):
        return self.grid[pos[0]][pos[1]]

    def white_in_check(self):
        for row in self.grid:
            for piece in row:
                if(piece != None and piece.color == 1 and King.White_King_Pos in piece.get_attack_moves()):
                    return True

    def black_in_check(self):
        for row in self.grid:
            for piece in row:
                if(piece != None and piece.color == 0 and King.Black_King_Pos in piece.get_attack_moves()):
                    return True

    def kings_in_check(self):
        checks = [self.white_in_check(), self.black_in_check()]
        return checks

    def get_invalid_moves(self, piece):
        invalid_moves = []
        for move in piece.valid_moves:
            temp = self.grid[move[0]][move[1]]
            origin = [piece.row, piece.column]
            piece.move(move[0], move[1], checking = True)
            if(self.kings_in_check()[piece.color]):
                invalid_moves.append(move)
            piece.undo_move(origin[0], origin[1], temp)
            self.kings_in_check()[piece.color]
        self.refresh_pieces()
        return invalid_moves

    def all_valid_moves(self, color_to_check):
        moves = []
        for row in self.grid:
            for piece in row:
                if(piece != None and piece.color == color_to_check):
                    moves += piece.get_valid_moves()
        return moves

    def all_attack_moves(self, color_to_check):
            moves = []
            for row in self.grid:
                for piece in row:
                    if(piece != None and piece.color == color_to_check):
                        moves += piece.get_attack_moves()
            return moves
            
    def no_valid_moves(self, color_to_move):
        for row in self.grid:
            for piece in row:
                if(piece != None and piece.color == color_to_move and len(piece.get_valid_moves()) > 0):
                    return False   
        return True
    
