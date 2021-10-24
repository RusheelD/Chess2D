
class Piece(object):

    def __init__(self, image, row, column, color, board):
        self.image = image
        self.row = row
        self.column = column
        self.color = color
        self.board = board
    
    def get_valid_moves(self):
        self.valid_moves = "Not yet implemented"
        return self.valid_moves

class Board(object):
    def __init__(self, black_images, white_images):
        self.grid = [[Rook(white_images[1], 0, 0, 0, self), Knight(white_images[2], 0, 1, 0, self), 
        Bishop(white_images[3], 0, 2, 0, self), Queen(white_images[4], 0, 3, 0, self), 
        King(white_images[5], 0, 4, 0, self), Bishop(white_images[3], 0, 5, 0, self), 
        Knight(white_images[2], 0, 6, 0, self), Rook(white_images[1], 0, 7, 0, self)], 
        [Pawn(white_images[0], 1, 0, 0, self), Pawn(white_images[0], 1, 1, 0, self), 
        Pawn(white_images[0], 1, 2, 0, self), Pawn(white_images[0], 1, 3, 0, self), 
        Pawn(white_images[0], 1, 4, 0, self), Pawn(white_images[0], 1, 5, 0, self), 
        Pawn(white_images[0], 1, 6, 0, self), Pawn(white_images[0], 1, 7, 0, self)], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None], 
        [Pawn(black_images[0], 6, 0, 1, self), Pawn(black_images[0], 6, 1, 1, self), 
        Pawn(black_images[0], 6, 2, 1, self), Pawn(black_images[0], 6, 3, 1, self), 
        Pawn(black_images[0], 6, 4, 1, self), Pawn(black_images[0], 6, 5, 1, self), 
        Pawn(black_images[0], 6, 6, 1, self), Pawn(black_images[0], 6, 7, 1, self)], 
        [Rook(black_images[1], 7, 0, 1, self), Knight(black_images[2], 7, 1, 1, self), 
        Bishop(black_images[3], 7, 2, 1, self), Queen(black_images[4], 7, 3, 1, self), 
        King(black_images[5], 7, 4, 1, self), Bishop(black_images[3], 7, 5, 1, self), 
        Knight(black_images[2], 7, 6, 1, self), Rook(black_images[1], 7, 7, 1, self)]]

class Pawn(Piece):
    def get_valid_moves(self):

        self.valid_moves = []
        
        if((self.color == 0 and self.row == 1) or (self.color == 1 and self.row == 6)):
            move_distance = 2
        else:
            move_distance = 1

        if(self.color == 0):
            multiplier = 1
        else:
            multiplier = -1

        for i in range(1, move_distance + 1):
            if(self.row != 7 and self.row != 0 and self.board.grid[self.row + (i * multiplier)][self.column] == None):
                self.valid_moves.append([self.row + (i * multiplier), self.column])
            elif(self.board.grid[self.row + (i * multiplier)][self.column] != None):
                break
        
        if(self.row != 7 and self.row != 0):
            if(self.column != 7):
                DR = self.board.grid[self.row + (1 * multiplier)][self.column + 1]
                AR = self.board.grid[self.row][self.column + 1]
            else:
                DR = None
                AR = None

            if(self.column != 0):
                DL = self.board.grid[self.row + (1 * multiplier)][self.column - 1]
                AL = self.board.grid[self.row][self.column - 1]
            else:
                DL = None
                AL = None
        else:
            DR = None
            DL = None

        if(DR != None and DR.color != self.color):
            self.valid_moves.append([self.row + (1 * multiplier), self.column + 1])
        if(DL != None and DL.color != self.color):
            self.valid_moves.append([self.row + (1 * multiplier), self.column - 1])

        en_pass_init = self.row == 4 - self.color
        if(en_pass_init):
            if(AL != None and type(AL) == type(self)):
                self.valid_moves.append([self.row + (1 * multiplier), self.column - 1])
            if(AR != None and type(AR) == type(self)):
                self.valid_moves.append([self.row + (1 * multiplier), self.column + 1])
        
        return self.valid_moves

class Rook(Piece):   
    def get_valid_moves(self):

        self.valid_moves = []

        for i in range(self.column + 1, 8):
            check = self.board.grid[self.row][i]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row, i])
                break
            self.valid_moves.append([self.row, i])

        for i in range(self.column - 1, -1, -1):
            check = self.board.grid[self.row][i]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row, i])
                break
            self.valid_moves.append([self.row, i])

        for i in range(self.row + 1, 8):
            check = self.board.grid[i][self.column]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([i, self.column])
                break
            self.valid_moves.append([i, self.column])

        for i in range(self.row - 1, -1, -1):
            check = self.board.grid[i][self.column]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([i, self.column])
                break
            self.valid_moves.append([i, self.column])
        
        return self.valid_moves

class Bishop(Piece):
    def get_valid_moves(self):

        self.valid_moves = []

        min_row = self.row
        max_row = 7 - self.row
        min_col = self.column
        max_col = 7 - self.column

        max_UR = min(max_row, max_col)
        max_UL = min(max_row, min_col)
        max_DR = min(min_row, max_col)
        max_DL = min(min_row, min_col)

        for n in range(1, max_UR + 1):
            check = self.board.grid[self.row + n][self.column + n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row + n, self.column + n])
                break
            self.valid_moves.append([self.row + n, self.column + n])

        for n in range(1, max_UL + 1):
            check = self.board.grid[self.row + n][self.column - n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row + n, self.column - n])
                break
            self.valid_moves.append([self.row + n, self.column - n])

        for n in range(1, max_DR + 1):
            check = self.board.grid[self.row - n][self.column + n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row - n, self.column + n])
                break
            self.valid_moves.append([self.row - n, self.column + n])

        for n in range(1, max_DL + 1):
            check = self.board.grid[self.row - n][self.column - n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row - n, self.column - n])
                break
            self.valid_moves.append([self.row - n, self.column - n])

        return self.valid_moves

class Knight(Piece):
    def get_valid_moves(self):

        self.valid_moves = []

        potential_moves = [[self.row + 2, self.column + 1], [self.row + 1, self.column + 2], 
        [self.row - 2, self.column - 1], [self.row - 1, self.column - 2], 
        [self.row + 2, self.column - 1], [self.row + 1, self.column - 2], 
        [self.row - 2, self.column + 1], [self.row - 1, self.column + 2]]

        remove = []

        for i in range(len(potential_moves)):
            move = potential_moves[i]
            if(not(0 <= move[0] <= 7 and 0 <= move[1] <= 7)):
                remove.append(move)
        
        for i in range(len(potential_moves)):
            move = potential_moves[i]
            try:
                check = self.board.grid[move[0]][move[1]]
            except IndexError:
                check = None
            if(check != None and check.color == self.color):
                    remove.append(move)
                
        for move in remove:
            try:
                potential_moves.remove(move)
            except ValueError:
                continue
        
        self.valid_moves = potential_moves

        return self.valid_moves


class Queen(Piece):
    def get_valid_moves(self):
        self.valid_moves = []

        min_row = self.row
        max_row = 7 - self.row
        min_col = self.column
        max_col = 7 - self.column

        max_UR = min(max_row, max_col)
        max_UL = min(max_row, min_col)
        max_DR = min(min_row, max_col)
        max_DL = min(min_row, min_col)

        for n in range(1, max_UR + 1):
            check = self.board.grid[self.row + n][self.column + n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row + n, self.column + n])
                break
            self.valid_moves.append([self.row + n, self.column + n])

        for n in range(1, max_UL + 1):
            check = self.board.grid[self.row + n][self.column - n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row + n, self.column - n])
                break
            self.valid_moves.append([self.row + n, self.column - n])

        for n in range(1, max_DR + 1):
            check = self.board.grid[self.row - n][self.column + n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row - n, self.column + n])
                break
            self.valid_moves.append([self.row - n, self.column + n])

        for n in range(1, max_DL + 1):
            check = self.board.grid[self.row - n][self.column - n]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row - n, self.column - n])
                break
            self.valid_moves.append([self.row - n, self.column - n])

        for i in range(self.column + 1, 8):
            check = self.board.grid[self.row][i]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row, i])
                break
            self.valid_moves.append([self.row, i])

        for i in range(self.column - 1, -1, -1):
            check = self.board.grid[self.row][i]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([self.row, i])
                break
            self.valid_moves.append([self.row, i])

        for i in range(self.row + 1, 8):
            check = self.board.grid[i][self.column]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([i, self.column])
                break
            self.valid_moves.append([i, self.column])

        for i in range(self.row - 1, -1, -1):
            check = self.board.grid[i][self.column]
            if(check != None):
                if(check.color != self.color):
                    self.valid_moves.append([i, self.column])
                break
            self.valid_moves.append([i, self.column])
        
        return self.valid_moves

class King(Piece):
    White_King_Moves = 0
    Black_King_Moves = 0
    White_King_Pos = [0, 4]
    Black_King_Pos = [7, 4]
    def get_valid_moves(self):

        self.valid_moves = []

        min_row = self.row
        max_row = 7 - self.row
        min_col = self.column
        max_col = 7 - self.column

        if(min_row >= 1):
            if(min_col >= 1):
                piece = self.board.grid[self.row - 1][self.column - 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row - 1, self.column - 1])
                else:
                    self.valid_moves.append([self.row - 1, self.column - 1])

                piece = self.board.grid[self.row - 1][self.column]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row - 1, self.column])
                else:
                    self.valid_moves.append([self.row - 1, self.column])

                piece = self.board.grid[self.row][self.column - 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row, self.column - 1])
                else:
                    self.valid_moves.append([self.row, self.column - 1])

            if(max_col >= 1):
                piece = self.board.grid[self.row - 1][self.column + 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row - 1, self.column + 1])
                else:
                    self.valid_moves.append([self.row - 1, self.column + 1])

                piece = self.board.grid[self.row - 1][self.column]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row - 1, self.column])
                else:
                    self.valid_moves.append([self.row - 1, self.column])

                piece = self.board.grid[self.row][self.column + 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row, self.column + 1])
                else:
                    self.valid_moves.append([self.row, self.column + 1])

        if(max_row >= 1):
            if(min_col >= 1):
                piece = self.board.grid[self.row + 1][self.column - 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row + 1, self.column - 1])
                else:
                    self.valid_moves.append([self.row + 1, self.column - 1])

                piece = self.board.grid[self.row + 1][self.column]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row + 1, self.column])
                else:
                    self.valid_moves.append([self.row + 1, self.column])

                piece = self.board.grid[self.row][self.column - 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row, self.column - 1])
                else:
                    self.valid_moves.append([self.row, self.column - 1])

            if(max_col >= 1):
                piece = self.board.grid[self.row + 1][self.column + 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row + 1, self.column + 1])
                else:
                    self.valid_moves.append([self.row + 1, self.column + 1])

                piece = self.board.grid[self.row + 1][self.column]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row + 1, self.column])
                else:
                    self.valid_moves.append([self.row + 1, self.column])

                piece = self.board.grid[self.row][self.column + 1]
                if(piece != None):
                    if(piece.color != self.color):
                        self.valid_moves.append([self.row, self.column + 1])
                else:
                    self.valid_moves.append([self.row, self.column + 1])

        if(self.column == 4):
            if(self.color == 0 and self.row == 0 and King.White_King_Moves == 0):
                if(self.board.grid[0][1] == None and self.board.grid[0][2] == None and self.board.grid[0][3] == None):
                    self.valid_moves.append([0, 2])
                if(self.board.grid[0][5] == None and self.board.grid[0][6] == None):
                    self.valid_moves.append([0, 6])
            if(self.color == 1 and self.row == 7 and King.Black_King_Moves == 0):
                if(self.board.grid[7][1] == None and self.board.grid[7][2] == None and self.board.grid[7][3] == None):
                    self.valid_moves.append([7, 2])
                if(self.board.grid[7][5] == None and self.board.grid[7][6] == None):
                    self.valid_moves.append([7, 6])

        for row in self.board.grid:
            for piece in row:
                if piece != None and piece.color != self.color:
                    if type(piece) != King:
                        remove = []
                        for move in self.valid_moves:
                            if type(piece) == Pawn and move[1] == piece.column:
                                continue
                            if move in piece.get_valid_moves():
                                remove.append(move)
                        for move in remove:
                            try:
                                self.valid_moves.remove(move)
                            except ValueError:
                                continue
                    else:
                        remove = []
                        for move in self.valid_moves:
                            if(abs(move[0] - piece.row) <= 1 and abs(move[1] - piece.column) <= 1):
                                remove.append(move)
                        for move in remove:
                            try:
                                self.valid_moves.remove(move)
                            except ValueError:
                                continue
                     
        for move in self.valid_moves:
            if self.column == 4:
                if self.color == 0:
                    if move == [0, 2] and not([0, 3] in self.valid_moves):
                        try:
                            self.valid_moves.remove(move)
                        except ValueError:
                            continue
                    if move == [0, 6] and not([0, 5] in self.valid_moves):
                        try:
                            self.valid_moves.remove(move)
                        except ValueError:
                            continue
                if self.color == 1:
                    if move == [7, 2] and not([7, 3] in self.valid_moves):
                        try:
                            self.valid_moves.remove(move)
                        except ValueError:
                            continue
                    if move == [7, 6] and not([7, 5] in self.valid_moves):
                        try:
                            self.valid_moves.remove(move)
                        except ValueError:
                            continue
        return self.valid_moves