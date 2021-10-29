import pyglet
from pieces import *
from Promote import Promote
from End import End

window = pyglet.window.Window(800, 800)
window.set_caption("Chess Game")
window.set_location(300, 50)
pieces = pyglet.image.load('1200px-Chess_Pieces_Sprite.svg.png')

Black_King_Image = pieces.get_region(0, 0, 200, 200)
White_King_Image = pieces.get_region(0, 200, 200, 200)
Black_Queen_Image = pieces.get_region(200, 0, 200, 200)
White_Queen_Image = pieces.get_region(200, 200, 200, 200)
Black_Bishop_Image = pieces.get_region(400, 0, 200, 200)
White_Bishop_Image = pieces.get_region(400, 200, 200, 200)
Black_Knight_Image = pieces.get_region(600, 0, 200, 200)
White_Knight_Image = pieces.get_region(600, 200, 200, 200)
Black_Rook_Image = pieces.get_region(800, 0, 200, 200)
White_Rook_Image = pieces.get_region(800, 200, 200, 200)
Black_Pawn_Image = pieces.get_region(1000, 0, 200, 200)
White_Pawn_Image = pieces.get_region(1000, 200, 200, 200)

Black_Piece_Images = [Black_Pawn_Image, Black_Rook_Image, Black_Knight_Image, 
Black_Bishop_Image, Black_Queen_Image, Black_King_Image]

White_Piece_Images = [White_Pawn_Image, White_Rook_Image, White_Knight_Image, 
White_Bishop_Image, White_Queen_Image, White_King_Image]

background_white = pyglet.image.SolidColorImagePattern((255, 255, 255, 255)).create_image(100, 100)
background_gray = pyglet.image.SolidColorImagePattern((75, 75, 75, 255)).create_image(100, 100)
background_select = pyglet.image.SolidColorImagePattern((0, 175, 0, 255)).create_image(100, 100)
background_option_dark = pyglet.image.SolidColorImagePattern((175, 175, 0, 255)).create_image(100, 100)
background_option_light = pyglet.image.SolidColorImagePattern((225, 225, 0, 255)).create_image(100, 100)
background_check = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(100, 100)
background_checkmate = pyglet.image.SolidColorImagePattern((150, 0, 0, 255)).create_image(100, 100)
background_stalemate = pyglet.image.SolidColorImagePattern((0, 0, 255, 255)).create_image(100, 100)

move = [False, 8, 8, 0, [0, 0, False], 0, 0, False]

board = Board(Black_Piece_Images, White_Piece_Images)
count = [0]
move_history = []

def check_checks():
    checks = [False, False]
    for row in board.grid:
        for piece in row:
            if piece != None and piece.color == 1 and type(piece) != King and King.White_King_Pos in piece.get_valid_moves():
                checks[0] = True
                
    for row in board.grid:
        for piece in row:
            if piece != None and piece.color == 0 and type(piece) != King and King.Black_King_Pos in piece.get_valid_moves():
                checks[1] = True
    
    return checks

def call_draw(dt):
    window.dispatch_event('on_draw')    

@window.event
def on_draw():
    window.clear()
    checks = check_checks()
    no_moves = check_no_valid_moves()
    checkmate = (checks[0] or checks[1]) and no_moves
    stalemate = no_moves and not(checkmate)

    if(checkmate and count[0] >= 1):
        End().checkmate(move[3])
    if(stalemate and count[0] >= 1):
        End().stalemate()

    for r in range(len(board.grid)):
        for col in range(len(board.grid[r])):
            row = abs(7 * move[3] - r)
            column = abs(7 * move[3] - col)
            piece = board.grid[row][column]

            if(move[0] and board.grid[move[1]][move[2]] != None):
                if([row, column] == [move[1], move[2]]):
                    background_select.blit(100 * col, 100 * r)
                elif([row, column] in board.grid[move[1]][move[2]].get_valid_moves() and row%2 == column%2):
                    background_option_dark.blit(100 * col, 100 * r)
                elif([row, column] in board.grid[move[1]][move[2]].get_valid_moves()):
                    background_option_light.blit(100 * col, 100 * r)
                elif(r%2 == col%2):
                    background_gray.blit(100 * col, 100 * r)
                else:
                    background_white.blit(100 * col, 100 * r)
            elif(r%2 == col%2):
                background_gray.blit(100 * col, 100 * r)
            else:
                background_white.blit(100 * col, 100 * r)

            if(checks[0] and [row, column] == King.White_King_Pos) or (checks[1] and [row, column] == King.Black_King_Pos):
                if(no_moves):
                    background_checkmate.blit(100 * col, 100 * r)
                else:
                    background_check.blit(100 * col, 100 * r)
                
            if(stalemate and ((not(checks[0]) and [row, column] == King.White_King_Pos) or (not(checks[1]) and [row, column] == King.Black_King_Pos))):
                background_stalemate.blit(100 * col, 100 * r)

            if piece != None:
                temp_sprite = pyglet.sprite.Sprite(piece.image, col * 100, r * 100)
                temp_sprite.scale = 0.5
                temp_sprite.draw()
    
    if(checkmate or stalemate):
        count[0] += 1
    if(move[6] < move[5]):
        move[6] = move[5]
        move[3] = abs(move[3] - 1)
        window.dispatch_event('on_draw')
        move[3] = abs(move[3] - 1)
        pyglet.clock.schedule_once(call_draw, .5)
    
    
def check_no_valid_moves():
    for pieces_row in board.grid:
        for piece in pieces_row:
            if piece != None and piece.color == move[3]:
                for piece_move in piece.get_valid_moves():
                    row = piece_move[0]
                    column = piece_move[1]
                    tempX = move[1]
                    tempY = move[2]
                    move[1] = piece.row
                    move[2] = piece.column
                    valid = make_move(row, column, False, True)
                    if(valid[0]):
                        undo_move(row, column, valid[1], valid[2], valid[3])
                    move[1] = tempX
                    move[2] = tempY
                    if valid[0] == True:
                        return False
    return True

def undo_move(row, column, promote_enable, temp, temp2):
    if(not(promote_enable)):
        board.grid[move[1]][move[2]] = board.grid[row][column]
        board.grid[move[1]][move[2]].row = move[1]
        board.grid[move[1]][move[2]].column = move[2]
        board.grid[row][column] = temp
    else:
        if board.grid[row][column].color == 0:
            board.grid[move[1]][move[2]] = Pawn(White_Pawn_Image, move[1], move[2], move[3], board)
            board.grid[row][column] = temp
        else:
            board.grid[move[1]][move[2]] = Pawn(Black_Pawn_Image, move[1], move[2], move[3], board)
            board.grid[row][column] = temp

    if(type(board.grid[move[1]][move[2]]) == Pawn and temp == None) and (abs(move[1] - row) == 1 and abs(move[2] - column) == 1):
            board.grid[move[1]][column] = temp2

    if(type(board.grid[move[1]][move[2]]) == King):
        if(move[3] == 0):
            King.White_King_Moves -= 1
            King.White_King_Pos = [move[1], move[2]]
        elif(move[3] == 1):
            King.Black_King_Moves -= 1
            King.Black_King_Pos = [move[1], move[2]]

def make_move(row, column, promote_enable, check):
    if(board.grid[row][column] == None):

        temp2 = None

        if(type(board.grid[move[1]][move[2]]) == King and abs(column - move[2]) == 2):
            if(row == 0 and King.White_King_Moves == 0 and not(check_checks()[0])):
                if(column == 2 and type(board.grid[0][0]) == Rook):
                    board.grid[0][3] = board.grid[0][0]
                    board.grid[0][3].row = 0
                    board.grid[0][3].column = 3
                    board.grid[0][0] = None
                elif(column == 6 and type(board.grid[0][7]) == Rook):
                    board.grid[0][5] = board.grid[0][7]
                    board.grid[0][5].row = 0
                    board.grid[0][5].column = 5
                    board.grid[0][7] = None
            elif(row == 7 and King.Black_King_Moves == 0 and not(check_checks()[1])):
                if(column == 2 and type(board.grid[7][0]) == Rook):
                    board.grid[7][3] = board.grid[7][0]
                    board.grid[7][3].row = 7
                    board.grid[7][3].column = 3
                    board.grid[7][0] = None
                elif(column == 6 and type(board.grid[7][7]) == Rook):
                    board.grid[7][5] = board.grid[7][7] 
                    board.grid[7][5].row = 7
                    board.grid[7][5].column = 5
                    board.grid[7][7] = None
            elif(check_checks()[0] or check_checks()[1]):
                return [False, promote_enable, None, temp2]
        
        if(type(board.grid[move[1]][move[2]]) == King):
            if(move[3] == 0):
                King.White_King_Moves += 1
                King.White_King_Pos = [row, column]
            elif(move[3] == 1):
                King.Black_King_Moves += 1
                King.Black_King_Pos = [row, column]

        if(type(board.grid[move[1]][move[2]]) == Pawn):
            if(abs(move[1] - row) == 1 and abs(move[2] - column) == 1):
                if(move[4][0] == 1 and move[4][1] == column):
                    temp2 = board.grid[move[1]][column]
                    board.grid[move[1]][column] = None
                else:
                    temp2 = board.grid[move[1]][column]
                    move[4][2] = True
            if(abs(move[1] - row) == 2):
                move[4] = [2, column, False]

        if(type(board.grid[move[1]][move[2]]) == Pawn and (row == 7 * abs(move[3] - 1)) and not(check)):
            promote_enable = True
            if move[3] == 0:
                board.grid[move[1]][move[2]] = None
                choice = Promote().promote(move[3])
                if(choice == "Queen"):
                    board.grid[row][column] = Queen(White_Queen_Image, row, column, move[3], board)
                elif(choice == "Rook"):
                    board.grid[row][column] = Rook(White_Rook_Image, row, column, move[3], board)
                elif(choice == "Bishop"):
                    board.grid[row][column] = Bishop(White_Bishop_Image, row, column, move[3], board)
                elif(choice == "Knight"):
                    board.grid[row][column] = Knight(White_Knight_Image, row, column, move[3], board)
                
            else:
                board.grid[move[1]][move[2]] = None
                choice = Promote().promote(move[3])
                if(choice == "Queen"):
                    board.grid[row][column] = Queen(Black_Queen_Image, row, column, move[3], board)
                elif(choice == "Rook"):
                    board.grid[row][column] = Rook(Black_Rook_Image, row, column, move[3], board)
                elif(choice == "Bishop"):
                    board.grid[row][column] = Bishop(Black_Bishop_Image, row, column, move[3], board)
                elif(choice == "Knight"):
                    board.grid[row][column] = Knight(Black_Knight_Image, row, column, move[3], board)
                
        if(not(promote_enable)):
            board.grid[row][column] = board.grid[move[1]][move[2]]
            board.grid[row][column].row = row
            board.grid[row][column].column = column
            board.grid[move[1]][move[2]] = None

        if(check_checks()[move[3]]) or move[4][2]:
            undo_move(row, column, promote_enable, None, temp2)
            return [False, promote_enable, None, temp2]

        if(not(check)):
            move[0] = False
            if(move[3] == 0):
                move[3] = 1
            else:
                move[3] = 0
            move[4][0] = move[4][0] // 2
            move[4][2] = False
        return [True, promote_enable, None, temp2]
        
    elif(board.grid[row][column].color != move[3]):

        if(type(board.grid[move[1]][move[2]]) == King):
            if(move[3] == 0):
                King.White_King_Moves += 1
                King.White_King_Pos = [row, column]
            elif(move[3] == 1):
                King.Black_King_Moves += 1
                King.Black_King_Pos = [row, column]

        if(type(board.grid[move[1]][move[2]]) == Pawn and (row == 7 * abs(move[3] - 1)) and not(check)):
            promote_enable = True
            if move[3] == 0:
                temp = board.grid[row][column]
                board.grid[move[1]][move[2]] = None
                choice = Promote().promote(move[3])
                if(choice == "Queen"):
                    board.grid[row][column] = Queen(White_Queen_Image, row, column, move[3], board)
                elif(choice == "Rook"):
                    board.grid[row][column] = Rook(White_Rook_Image, row, column, move[3], board)
                elif(choice == "Bishop"):
                    board.grid[row][column] = Bishop(White_Bishop_Image, row, column, move[3], board)
                elif(choice == "Knight"):
                    board.grid[row][column] = Knight(White_Knight_Image, row, column, move[3], board)
                
            else:
                temp = board.grid[row][column]
                board.grid[move[1]][move[2]] = None
                
                choice = Promote().promote(move[3])
                if(choice == "Queen"):
                    board.grid[row][column] = Queen(Black_Queen_Image, row, column, move[3], board)
                elif(choice == "Rook"):
                    board.grid[row][column] = Rook(Black_Rook_Image, row, column, move[3], board)
                elif(choice == "Bishop"):
                    board.grid[row][column] = Bishop(Black_Bishop_Image, row, column, move[3], board)
                elif(choice == "Knight"):
                    board.grid[row][column] = Knight(Black_Knight_Image, row, column, move[3], board)
                
                
        if(not(promote_enable)):
            temp = board.grid[row][column]
            board.grid[row][column] = board.grid[move[1]][move[2]]
            board.grid[row][column].row = row
            board.grid[row][column].column = column
            board.grid[move[1]][move[2]] = None

        if(check_checks()[move[3]]):
            undo_move(row, column, promote_enable, temp, None)
            return [False, promote_enable, temp, None]
        
        if(not(check)):
            move[0] = False
            if(move[3] == 0):
                move[3] = 1
            else:
                move[3] = 0
            move[4][0] = move[4][0] // 2
            move[4][2] = False
        return [True, promote_enable, temp, None]

@window.event
def on_key_press(symbol, modifiers):
    if(symbol == pyglet.window.key.L and not(move[7])):
        load_game()

@window.event
def on_mouse_press(x, y, button, modifiers):

    r = int(y / 100)
    row = abs(7 * move[3] - r)
    col = int(x / 100)
    column = abs(7 * move[3] - col)
    promote_enable = False

    if(move[0] == True and (row == move[1] and column == move[2])):
        move[0] = False
        return

    if(not(move[0])):
        if(board.grid[row][column] != None and board.grid[row][column].color == move[3]):
                move[0] = True
                move[1] = row
                move[2] = column
                #print(board.grid[row][column].get_valid_moves())

    else:
        if(board.grid[move[1]][move[2]] != None and ([row, column] in board.grid[move[1]][move[2]].get_valid_moves())):
            move_result = make_move(row, column, promote_enable, False)
            if(move_result[0]):
                move[5] += 1
                move_history.append([str(board.grid[row][column]), row, column, move[5], move[1], move[2]])
                

def store_history():
    storage = open("RecentGame.txt", 'w')
    cols = "ABCDEFGH" 

    for i in range(len(move_history)):
        if(i < 1 or (i >=1 and move_history[i][0] != move_history[i-1][0])):
            storage.write(str((move_history[i][3] + 1) // 2) + " " + str(move_history[i][0]) + "\t" + str(cols[move_history[i][5]]) + str(move_history[i][4] + 1) + " " + str(cols[move_history[i][2]]) + str(move_history[i][1] + 1))
            storage.write("\n")
    
    storage.close()

def load_game():
    past_game = open("RecentGame.txt", 'r')
    past_game_moves = past_game.read().split('\n')[:-1]
    cols = "ABCDEFGH"
    for i in range(len(past_game_moves)):
        past_game_moves[i] = past_game_moves[i][-5:]

    move_temp_1 = move[1]
    move_temp_2 = move[2]

    move[3] = 1

    for past_move in past_game_moves:
        move[3] = abs(move[3] - 1)
        past_move_origin = past_move[:2]
        past_move_destination = past_move[-2:]

        move[1] = int(past_move_origin[1]) - 1
        move[2] = cols.find(past_move_origin[0])

        pyglet.clock.schedule_once(call_draw, .1)

        make_move(int(past_move_destination[1]) - 1, cols.find(past_move_destination[0]), False, False)
        move[5] += 1
        move[6] += 1

        pyglet.clock.schedule_once(call_draw, .5)

        move_history.append([str(board.grid[int(past_move_destination[1]) - 1][cols.find(past_move_destination[0])]), int(past_move_destination[1]) - 1, cols.find(past_move_destination[0]), move[5], move[1], move[2]])

    move[7] = True

    move[1] = move_temp_1
    move[2] = move_temp_2 

@window.event
def on_close():
    pyglet.app.exit()


#pyglet.clock.schedule_interval(call_draw, 1)
pyglet.app.run()
store_history()