import pyglet
from GameControl import GameControl
from AI import AI

class AIControl(GameControl):
    def __init__(self, AI_enabled):
        super().__init__()
        self.AI_color = 0
        self.AI = AI(self.board, self.AI_color, self)
        self.AI_enabled = AI_enabled
        self.AI_refreshed = False
    
    def select_tile(self, row, column, promote_choice = None):
        c = promote_choice
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
            self.selected_piece.move(row, column, choice = c)
            self.color_to_move = abs(self.color_to_move - 1)
            self.is_piece_selected = False
            self.selected_piece = None
            self.board.update_valid_moves()
            # if(not(self.is_game_over()[0]) and self.AI_enabled):
            #     # self.updateAI()
            #     pyglet.clock.schedule_once(self.updateAI, .001)
            #     # print('something')

        elif(self.board.grid[row][column] != None and self.board.grid[row][column].color == self.selected_piece.color):
            self.is_piece_selected = True
            self.selected_piece = self.board.grid[row][column]
            
        return self.selected_piece
    
    def updateAI(self, dt):
        if self.color_to_move == self.AI_color and not self.is_game_over():
            AI_move = self.AI.get_move()
            selected_piece = AI_move[0]
            selected_move = AI_move[1]
            if(selected_piece == None):
                return
            self.select_tile(selected_piece.row, selected_piece.column)
            self.select_tile(selected_move[0], selected_move[1], promote_choice = self.AI.choice)
            self.AI_refreshed = False
            self.board.update_valid_moves()
        else:
            return