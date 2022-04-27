import pyglet
from AIControl import AIControl
from End import End

class UI(object):
    def __init__(self):
        self.background_white = pyglet.image.SolidColorImagePattern((255, 255, 255, 255)).create_image(100, 100)
        self.background_gray = pyglet.image.SolidColorImagePattern((75, 75, 75, 255)).create_image(100, 100)
        self.background_select = pyglet.image.SolidColorImagePattern((0, 175, 0, 255)).create_image(100, 100)
        self.background_option_dark = pyglet.image.SolidColorImagePattern((175, 175, 0, 255)).create_image(100, 100)
        self.background_option_light = pyglet.image.SolidColorImagePattern((225, 225, 0, 255)).create_image(100, 100)
        self.background_check = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(100, 100)
        self.background_checkmate = pyglet.image.SolidColorImagePattern((150, 0, 0, 255)).create_image(100, 100)
        self.background_stalemate = pyglet.image.SolidColorImagePattern((0, 0, 255, 255)).create_image(100, 100)

        self.window = pyglet.window.Window(800, 800)
        self.window.set_caption("Chess Game")
        self.window.set_location(300, 50)
        self.window.push_handlers(self)

        self.turn_count = 0

        self.game_over_frames = 0

        self.end_signaled = False

        self.game = AIControl(True)
    
    def call_draw(self, dt):
        game_over = self.game.is_game_over()
        stalemate = game_over[0] and game_over[1] == -1
        checkmate = game_over[0] and not(stalemate)

        if(checkmate and self.game_over_frames >= 2) and not(self.end_signaled):
            self.end_signaled = True
            End().checkmate(game_over[1])
        if(stalemate and self.game_over_frames >= 2) and not(self.end_signaled):
            self.end_signaled = True
            End().stalemate()
        
        self.window.dispatch_event('on_draw')

    def on_draw(self):
        self.window.clear()
        in_check = self.game.in_check()
        game_over = self.game.is_game_over()
        stalemate = game_over[0] and game_over[1] == -1
        checkmate = game_over[0] and not(stalemate)
        

        for r in range(len(self.game.board.grid)):
            for col in range(len(self.game.board.grid[r])):
                row = r
                column = col
                piece = self.game.board.grid[row][column]

                if(self.game.is_piece_selected and self.game.selected_piece != None):
                    if([row, column] == [self.game.selected_piece.row, self.game.selected_piece.column]):
                        self.background_select.blit(100 * col, 100 * r)
                    elif([row, column] in self.game.board.grid[self.game.selected_piece.row][self.game.selected_piece.column].get_valid_moves() and row%2 == column%2):
                        self.background_option_dark.blit(100 * col, 100 * r)
                    elif([row, column] in self.game.board.grid[self.game.selected_piece.row][self.game.selected_piece.column].get_valid_moves()):
                        self.background_option_light.blit(100 * col, 100 * r)
                    elif(r%2 == col%2):
                        self.background_gray.blit(100 * col, 100 * r)
                    else:
                        self.background_white.blit(100 * col, 100 * r)
                elif(r%2 == col%2):
                    self.background_gray.blit(100 * col, 100 * r)
                else:
                    self.background_white.blit(100 * col, 100 * r)
                
                if(game_over[0]):
                    if((game_over[1] == 0 and [row, column] == self.game.board.get_white_king_pos()) or (game_over[1] == 1 and [row, column] == self.game.board.get_black_king_pos())):
                        self.background_checkmate.blit(100 * col, 100 * r)
                    elif(stalemate and ([row, column] == self.game.board.get_white_king_pos() or [row, column] == self.game.board.get_black_king_pos())):
                        self.background_stalemate.blit(100 * col, 100 * r)
                elif(in_check and ((self.game.color_to_move == 0 and [row, column] == self.game.board.get_white_king_pos()) or (self.game.color_to_move == 1 and [row, column] == self.game.board.get_black_king_pos()))):
                    self.background_check.blit(100 * col, 100 * r)

                if piece != None:
                    temp_sprite = pyglet.sprite.Sprite(piece.image, col * 100, r * 100)
                    temp_sprite.scale = 0.5
                    temp_sprite.draw()
        
        if(self.turn_count < len(self.game.board.moves_made)):
            self.turn_count = len(self.game.board.moves_made)
            self.game.color_to_move = abs(self.game.color_to_move - 1)
            self.window.dispatch_event('on_draw')
            self.game.color_to_move = abs(self.game.color_to_move - 1)
            pyglet.clock.schedule_once(self.call_draw, .25)

        if(self.game.AI_refreshed == False):
            self.game.AI_refreshed = True
            pyglet.clock.schedule_once(self.call_draw, .1)
            
        if(checkmate or stalemate):
            self.game_over_frames += 1
            if(self.game_over_frames == 2):
                pyglet.clock.schedule_once(self.call_draw, .1)
        else:
            self.game_over_frames = 0      
                
    def on_key_press(self, symbol, modifiers):
        if(symbol == pyglet.window.key.L and not(self.game.loaded)):
            self.game.load_game()
            self.turn_count = len(self.game.board.moves_made)
            self.game_over_frames = 2
            pyglet.clock.schedule_once(self.call_draw, .1)
        else:
            return pyglet.event.EVENT_HANDLED
        
    def on_mouse_press(self, x, y, button, modifiers):

        r = int(y / 100)
        row = r #abs(7 * self.game.color_to_move - r)
        col = int(x / 100)
        column = col #abs(7 * self.game.color_to_move - col)

        self.game.select_tile(row, column)

    def on_close(self):
        pyglet.app.exit()