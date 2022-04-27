from Board import Board

class GameControl(object):
    def __init__(self):
        self.is_piece_selected = False
        self.selected_piece = None
        self.board = Board()
        self.color_to_move = 0
        self.loaded = False

    def select_tile(self, row, column):
        if(self.board.grid[row][column] == None and not(self.is_piece_selected)):
            self.is_piece_selected = False
            self.selected_piece = None

        elif(not(self.is_piece_selected)):
            if(self.board.grid[row][column].color != self.color_to_move):
                return None
            self.is_piece_selected = True
            self.selected_piece = self.board.grid[row][column]

        elif(self.selected_piece.row == row and self.selected_piece.column == column):
            self.is_piece_selected = False
            self.selected_piece = None

        elif([row, column] in self.selected_piece.get_valid_moves()):
            self.selected_piece.move(row, column)
            self.color_to_move = abs(self.color_to_move - 1)
            self.is_piece_selected = False
            self.selected_piece = None
            self.board.update_valid_moves()

        elif(self.board.grid[row][column] != None and self.board.grid[row][column].color == self.selected_piece.color):
            self.is_piece_selected = True
            self.selected_piece = self.board.grid[row][column]

        return self.selected_piece

    def is_game_over(self):
        if(self.board.no_valid_moves(self.color_to_move)):
            if(self.in_check()):
                return [True, self.color_to_move]
            else:
                return [True, -1]
        return [False, -1]

    def in_check(self):
        return self.board.kings_in_check()[self.color_to_move]

    def load_game(self):
        self.board = Board()
        past_game = open("RecentGame.txt", 'r')
        past_game_moves = past_game.read().split('\n')[:-1]

        if past_game_moves == []:
            return False

        cols = "ABCDEFGH"
        for i in range(len(past_game_moves)):
            past_game_moves[i] = past_game_moves[i][-5:]

        self.color_to_move = 0

        for past_move in past_game_moves:

            past_move_origin = past_move[:2]
            past_move_destination = past_move[-2:]

            origin_row = int(past_move_origin[1]) - 1
            origin_column = cols.find(past_move_origin[0])

            row = int(past_move_destination[1]) - 1
            column = cols.find(past_move_destination[0])

            self.board.grid[origin_row][origin_column].move(row, column)
            self.color_to_move = abs(self.color_to_move - 1)

            self.loaded = True

    def store_history(self):
        storage = open("RecentGame.txt", 'w')
        cols = "ABCDEFGH" 

        for i in range(len(self.board.moves_made)):
            storage.write(str(self.board.moves_made[i][0]) + " " + 
            str(self.board.moves_made[i][1]) + "\t" + 
            str(cols[self.board.moves_made[i][3]]) + 
            str(self.board.moves_made[i][2] + 1) + " " + 
            str(cols[self.board.moves_made[i][5]]) + 
            str(self.board.moves_made[i][4] + 1))
            storage.write("\n")
        
        storage.close()
