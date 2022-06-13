import random

from Pieces import King, Pawn

class AI(object):
    def __init__(self, board, color, control):
        self.board = board
        self.color = color
        self.piece_selected = False
        self.selected_piece = None
        self.selected_move = None
        self.pieces = []
        self.stuck_pieces = []
        self.update_pieces()
        self.choice = "Queen"
        self.control = control

    def select_piece(self):

        self.choice = None
        self.selected_move = None
        self.update_pieces()
        self.stuck_pieces = []

        if(self.board.current_turn <= 4):
            self.selected_piece = self.get_best_piece() #self.get_best_open_piece()
        elif(self.board.current_turn > 4):
            self.selected_piece = self.get_best_piece()
        else:
            self.selected_piece = random.choice(self.pieces)
            while(self.selected_piece.get_valid_moves() == []):
                self.stuck_pieces.append(self.selected_piece)
                if(self.stuck_pieces == self.pieces):
                    return None
                self.selected_piece = random.choice(self.pieces)
                        
        self.piece_selected = True
        return self.selected_piece

    def select_move(self):
        self.selected_move = self.get_best_move(self.selected_piece)[0]
        self.selected_piece = None
        self.piece_selected = False
        return self.selected_move

    def get_move(self):
        piece_move = self.select_piece()
        return piece_move

    def get_best_open_piece(self):
        best_moves = 0
        best_piece = None
        for piece in self.pieces:
            moves = self.get_best_open_move(piece)[1]
            if(moves > best_moves):
                best_moves = moves
                best_piece = piece
        return best_piece

    def get_best_piece(self):
        best_score = float('-inf')
        #best_piece = None
        best_pieces = []
        for piece in self.pieces:
            move_attributes = self.get_best_move(piece)
            move_score = move_attributes[0]
            attributes = move_attributes[1]
            score = move_score[2]
            move = move_score[0]
            if(score > best_score):
                best_pieces.clear()
                best_score = score
                best_pieces.append([[piece, move], attributes])
            elif(score == best_score):
                best_pieces.append([[piece, move], attributes])
        choice = random.choice(best_pieces)
        # print(choice, best_score)
        return choice[0]
    
    def get_best_open_move(self, piece):
        moves = piece.get_valid_moves()
        move_to_choose = [[], 0, 0]
        for move in moves:
            temp = self.board.grid[move[0]][move[1]]
            origin = [piece.row, piece.column]

            piece.move(move[0], move[1], checking = True)
            available_moves = self.board.all_valid_moves(self.color)
            piece.undo_move(origin[0], origin[1], temp)
            self.board.kings_in_check()[self.color]

            if(len(available_moves) > move_to_choose[1]):
                move_to_choose = [move, len(available_moves)]
                
        return move_to_choose

    def get_best_move(self, piece):
        if(piece == None):
            return [[], 0, 0]
        moves = piece.get_valid_moves()
        move_to_choose = [[], -1, float('-inf')]
        attributes = []
        for i in range(15):
            attributes.append(float('-inf'))
        for move in moves:
            temp = self.board.grid[move[0]][move[1]]

            if(temp != None and temp.color == self.color):
                continue

            origin = [piece.row, piece.column]
            score = 0
            openness = 0
            protection = 0
            overall_threat = 0
            self_threat = 0
            move_to_check = 0
            danger = 0
            attack = 0
            limitation = 0
            limit_king = 0
            stalemate = 0
            checkmate = 0
            made_before = 0
            in_threat = 0
            promote = 0
            develop = 0
            opposing_king_pos = self.board.get_white_king_pos() if self.color == 1 else self.board.get_black_king_pos()


            self_pre_attacking_moves = self.board.all_attack_moves(self.color)

            opposing_pre_attack_moves = self.board.all_attack_moves(abs(self.color - 1))

            opposing_pre_available_moves = self.board.all_valid_moves(abs(self.color - 1))
            
            opposing_pre_king_moves = self.board.get(opposing_king_pos).get_valid_moves()

            piece.move(move[0], move[1], checking = True)

            no_moves = self.board.no_valid_moves(abs(self.color - 1))

            available_moves = self.board.all_valid_moves(self.color)

            opposing_post_available_moves = self.board.all_valid_moves(abs(self.color - 1))

            opposing_post_king_moves = self.board.get(opposing_king_pos).get_valid_moves()

            setting_check = self.board.kings_in_check()[abs(self.color - 1)]

            self_post_attack_moves = self.board.all_attack_moves(self.color)

            piece_post_attack_moves = piece.get_attack_moves()

            opposing_post_attack_moves = self.board.all_attack_moves(abs(self.color - 1))

            piece.undo_move(origin[0], origin[1], temp)
            self.board.kings_in_check()[self.color]


            openness = ((4 // self.board.current_turn) + 1) * len(available_moves)

            limitation = (len(opposing_pre_available_moves) - len(opposing_post_available_moves)) / (len(opposing_pre_available_moves) + 0.25)
            
            limit_king = (len(opposing_pre_king_moves) - len(opposing_post_king_moves)) / (len(opposing_pre_king_moves) + 0.25)

            if(piece.steps_taken <= 3):
                develop += self.board.current_turn / (25 * piece.steps_taken + 1)

            if(type(piece) == Pawn):
                if(move[0] == 7 * abs(self.color - 1)):
                    promote += 75
                elif(move[0] == abs(7 * abs(self.color - 1) - 1)):
                    promote += 25

            for move_made in self.board.moves_made[-10:]:
                if piece == move_made[1] and (move == move_made[-2:] or move == move_made[-4:-2]):
                    made_before += (15 / abs(move_made[0] - self.board.current_turn))

            if(no_moves):
                if(setting_check):
                    checkmate += 150
                else:
                    stalemate += 150

            if(type(piece) != King):
                for attack_move in self_pre_attacking_moves:
                    protection += 1 if move == attack_move else 0
            for attack_move in self_post_attack_moves:
                p = self.board.get(attack_move)
                if(p != None and p.color == abs(self.color - 1) and type(p) != King):
                    overall_threat += 1
            for attack_move in piece_post_attack_moves:
                p = self.board.get(attack_move)
                if(p != None and p.color == abs(self.color - 1) and type(p) != King):
                    self_threat += 1

            for attack_move in opposing_pre_attack_moves:
                if([piece.row, piece.column] == attack_move):
                    in_threat += piece.value
                
            if(in_threat == 1 and [piece.row, piece.column] in opposing_pre_king_moves and protection > 0):
                in_threat = 0
                
            if(move in opposing_post_attack_moves):
                for attack_move in opposing_post_attack_moves:
                    if attack_move == move:
                        danger += 1
            elif(in_threat > 0):
                danger = (-1 * in_threat) / 8 - (2 + piece.value)

            if(setting_check and not(move) in opposing_post_attack_moves):
                move_to_check = 5
            elif(setting_check):
                move_to_check = 2

            if(temp != None and temp.color != piece.color):
                if(danger > 0):
                    if(temp.value > piece.value):
                        attack = 2.5 * temp.value
                    elif(temp.value == piece.value):
                        if danger - protection > 0:
                            attack = 2.5 * temp.value - piece.value
                        elif danger - protection == 0:
                            attack = 2.5 * temp.value
                        else:
                            attack = 4 * temp.value
                    else:
                        attack = temp.value - (piece.value - 1)
                else:
                    attack = 8 * temp.value

            if(danger > 0):
                danger = 5 + piece.value
            
            if(danger < 0):
                temp_danger = 0
                for attack_move in opposing_post_attack_moves:
                    p = self.board.get(attack_move)
                    if(p != None and p.color == self.color):
                        temp_danger = 5 + p.value
                    if(temp_danger > 5 + piece.value):
                        danger = temp_danger
                        break

            if(in_threat and made_before > 0):
                made_before /= 4.5
                
            score = (1/(5 * self.board.current_turn) * openness + 1/4 * (1/3 * protection + overall_threat) + 
            1/3 * self_threat + in_threat + 1.5 * move_to_check + 3 * limitation + 5 * limit_king + 10 * attack - 
            8 * danger + develop + promote + 10 * (checkmate - stalemate) - made_before)

            if(score > move_to_choose[2]):
                move_to_choose = [move, len(available_moves), score]
                attributes = [openness, protection, overall_threat, self_threat, in_threat, move_to_check, 
                limitation, limit_king, attack, danger, develop, promote, checkmate, stalemate, made_before]

        return [move_to_choose, attributes]

    def update_pieces(self):
        self.pieces.clear()
        for row in self.board.grid:
            for piece in row:
                if piece != None and piece.color == self.color:
                    self.pieces.append(piece)
    