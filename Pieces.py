from Promote import Promote

class Piece(object):

    def __init__(self, image, row, column, color, board):
        speeds = {King: 5, Queen: 4, Rook: 3, Bishop: 2, Knight: 2, Pawn: 0}
        self.image = image
        self.row = row
        self.column = column
        self.color = color
        self.board = board
        self.valid_moves = []
        self.steps_taken = 0
        self.turns_moved = []
        self.temp2 = None
        self.speed = speeds[type(self)]

    def update_valid_moves(self):
        self.valid_moves = self.get_valid_moves()
    
    def get_valid_moves(self):
        self.valid_moves = self.calculate_valid_moves()
        self.remove_invalid_moves()
        return self.valid_moves

    def calculate_valid_moves(self):
        self.valid_moves = []
        return self.valid_moves

    def get_attack_moves(self):
        return self.calculate_valid_moves()

    def remove_invalid_moves(self):
        invalid_moves = self.board.get_invalid_moves(self)

        for move in invalid_moves:
            try:
                self.valid_moves.remove(move)
            except ValueError:
                continue
    
    def move(self, row, column, checking = False):
        self.board.grid[self.row][self.column] = None
        self.board.grid[row][column] = self
        origin_row = self.row
        origin_column = self.column
        self.row = row
        self.column = column
        if(checking == False):
            self.steps_taken += 1
            self.board.moves_made.append([self.board.current_turn, self, origin_row, origin_column, row, column])
            self.turns_moved.append(self.board.current_turn)
            self.board.current_turn += self.color

    def undo_move(self, row, column, temp):
        self.board.grid[row][column] = self
        self.board.grid[self.row][self.column] = temp
        self.row = row
        self.column = column

    def __str__(self):
        printStr = ""
        if self.color == 0:
            printStr += "White "
        else:
            printStr += "Black "

        printStr += str(self.__class__)[15:-2]
        return printStr

class Pawn(Piece):
    def move(self, row, column, checking = False):

        if(self.column != column and self.board.grid[row][column] == None):
            if(checking):
                self.temp2 = [self.board.grid[self.row][column], self.row, column]
            self.board.grid[self.row][column] = None
            super().move(row, column, checking)

        elif((row == 7 * abs(self.color - 1)) and not(checking)):
            if(self.color == 0):
                images = self.board.white_images
            else:
                images = self.board.black_images

            self.board.grid[self.row][self.column] = None
            choice = Promote().promote(self.color)
            if(choice == "Queen"):
                self.board.grid[row][column] = Queen(images[4], row, column, self.color, self.board)
            elif(choice == "Rook"):
                self.board.grid[row][column] = Rook(images[1], row, column, self.color, self.board)
            elif(choice == "Bishop"):
                self.board.grid[row][column] = Bishop(images[3], row, column, self.color, self.board)
            elif(choice == "Knight"):
                self.board.grid[row][column] = Knight(images[2], row, column, self.color, self.board)
        else:
            super().move(row, column, checking)

    def undo_move(self, row, column, temp):
        if self.temp2 != None:
            self.board.grid[self.temp2[1]][self.temp2[2]] = self.temp2[0]
            self.temp2 = None
        super().undo_move(row, column, temp)
        
    def get_attack_moves(self):
        self.attack_moves = []

        if(self.color == 0):
            multiplier = 1
        else:
            multiplier = -1

        if(self.row != 7 and self.row != 0):
            if(self.column != 7):
                DR = self.board.grid[self.row + (1 * multiplier)][self.column + 1]
            else:
                DR = None

            if(self.column != 0):
                DL = self.board.grid[self.row + (1 * multiplier)][self.column - 1]
            else:
                DL = None
        else:
            DR = None
            DL = None

        if(DR != None and DR.color != self.color):
            self.attack_moves.append([self.row + (1 * multiplier), self.column + 1])
        if(DL != None and DL.color != self.color):
            self.attack_moves.append([self.row + (1 * multiplier), self.column - 1])

        return self.attack_moves

    def calculate_valid_moves(self):

        self.valid_moves = []
        
        if(self.steps_taken == 0):
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
            if(AL != None and type(AL) == type(self) and AL.color != self.color and AL == self.board.moves_made[-1][1] and AL.steps_taken == 1):
                self.valid_moves.append([self.row + (1 * multiplier), self.column - 1])
            if(AR != None and type(AR) == type(self) and AR.color != self.color and AR == self.board.moves_made[-1][1] and AR.steps_taken == 1):
                self.valid_moves.append([self.row + (1 * multiplier), self.column + 1])
        
        return self.valid_moves

class Rook(Piece):   
    def calculate_valid_moves(self):

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
    def calculate_valid_moves(self):

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
    def calculate_valid_moves(self):

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
    def calculate_valid_moves(self):
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

    def white_in_check(self):
        for row in self.board.grid:
            for piece in row:
                if(piece != None and piece.color == 1 and King.White_King_Pos in piece.get_attack_moves()):
                    return True

    def black_in_check(self):
        for row in self.board.grid:
            for piece in row:
                if(piece != None and piece.color == 0 and King.Black_King_Pos in piece.get_attack_moves()):
                    return True

    def move(self, row, column, checking = False):
        if(abs(column - self.column) == 2):
            if(row == 0 and King.White_King_Moves == 0 and not(self.white_in_check())):
                if(column == 2 and type(self.board.grid[0][0]) == Rook and self.board.grid[0][0].steps_taken == 0):
                    self.board.grid[0][0].move(0, 3, checking)
                    if(not(checking)):
                        self.board.moves_made = self.board.moves_made[:-1]
                        self.board.current_turn -= self.color
                    super().move(row, column, checking)
                    King.White_King_Moves += 1
                    King.White_King_Pos = [self.row, self.column]
                elif(column == 6 and type(self.board.grid[0][7]) == Rook and self.board.grid[0][7].steps_taken == 0):
                    self.board.grid[0][7].move(0, 5, checking)
                    if(not(checking)):
                        self.board.moves_made = self.board.moves_made[:-1]
                        self.board.current_turn -= self.color
                    super().move(row, column, checking)
                    King.White_King_Moves += 1
                    King.White_King_Pos = [self.row, self.column]
            elif(row == 7 and King.Black_King_Moves == 0 and not(self.black_in_check())):
                if(column == 2 and type(self.board.grid[7][0]) == Rook and self.board.grid[7][0].steps_taken == 0):
                    self.board.grid[7][0].move(7, 3, checking)
                    if(not(checking)):
                        self.board.moves_made = self.board.moves_made[:-1]
                        self.board.current_turn -= self.color
                    super().move(row, column, checking)
                    King.Black_King_Moves += 1
                    King.Black_King_Pos = [self.row, self.column]
                elif(column == 6 and type(self.board.grid[7][7]) == Rook and self.board.grid[7][7].steps_taken == 0):
                    self.board.grid[7][7].move(7, 5, checking)
                    if(not(checking)):
                        self.board.moves_made = self.board.moves_made[:-1]
                        self.board.current_turn -= self.color
                    super().move(row, column, checking)
                    King.Black_King_Moves += 1
                    King.Black_King_Pos = [self.row, self.column]
        else:
            super().move(row, column, checking)
            if(self.color == 0):
                King.White_King_Moves += 1
                King.White_King_Pos = [self.row, self.column]
            else:
                King.Black_King_Moves += 1
                King.Black_King_Pos = [self.row, self.column]

    def undo_move(self, row, column, temp):
        if(abs(column - self.column) == 2):
            if(row == 0):
                if(self.column == 2):
                    self.board.grid[0][3].undo_move(0, 0, None)
                    super().undo_move(row, column, temp)
                    King.White_King_Moves -= 1
                    King.White_King_Pos = [self.row, self.column]
                elif(self.column == 6):
                    self.board.grid[0][5].undo_move(0, 7, None)
                    super().undo_move(row, column, temp)
                    King.White_King_Moves -= 1
                    King.White_King_Pos = [self.row, self.column]
            elif(row == 7):
                if(self.column == 2):
                    self.board.grid[7][3].undo_move(7, 0, None)
                    super().undo_move(row, column, temp)
                    King.Black_King_Moves -= 1
                    King.Black_King_Pos = [self.row, self.column]
                elif(self.column == 6):
                    self.board.grid[7][5].undo_move(7, 7, None)
                    super().undo_move(row, column, temp)
                    King.Black_King_Moves -= 1
                    King.Black_King_Pos = [self.row, self.column]
        else:
            super().undo_move(row, column, temp)
            if(self.color == 0):
                King.White_King_Moves -= 1
                King.White_King_Pos = [self.row, self.column]
            else:
                King.Black_King_Moves -= 1
                King.Black_King_Pos = [self.row, self.column]

    def calculate_valid_moves(self):

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
                            if move in piece.get_attack_moves():
                                remove.append(move)
                            if abs(move[1] - self.column) == 2 and [self.row, self.column] in piece.get_attack_moves():
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