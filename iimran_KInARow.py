'''
<iimran>_KInARow.py
Authors: Imran, Ibrahim


An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type
import time
import random

AUTHORS = 'Ibrahim Imran'
UWNETIDS = ['iimran'] # The first UWNetID here should
# match the one in the file name, e.g., janiesmith99_KInARow.py.
# Behavior: Generates all legal moves
# Exceptions: None
# Returns: All legal moves
# Parameter: Game State
def get_every_move(state):
    moves = []
    board = state.board
    k_rows = len(board)
    k_cols = len(board[0])

    for row in range(k_rows):
        for col in range(k_cols):
            if board[row][col] == ' ': #designates an empty square
                new_state = State(old=state)
                new_state.board[row][col] = state.whose_move
                new_state.whose_move = helperForOtherPlayer(state.whose_move) #using helper method
                moves.append(((row, col), new_state))

    return moves


# Behavior: Check for win
# Exceptions: None
# Returns:None if no win, play if win
# Paramters: state, and k_vallue
def win_checker(state, k_value):

    board = state.board
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range (cols):
            play = board[r][c]
            if play not in ['X', 'O']:
                continue

    # Check down
            if r + k_value <= rows:
                if all(board[r+i][c] == play for i in range (k_value)):
                    return play
    # Check right
            if c + k_value <= cols:
                if all(board[r][c+i] == play for i in range(k_value)):
                    return play
    # Check diagonal down-right
            if r + k_value <= rows and c + k_value <= cols:
                if all(board[r + i][c + i] == play for i in range(k_value)):
                    return play

    # Check diagonal down-left
            if r + k_value <= rows and c - k_value + 1 >= 0:
                if all(board[r + i][c - i] == play for i in range(k_value)):
                    return play

    return None





# Behvaior: Checks if board is full/draw condition
# Exceptions: None
# Returns: True if full, False if not
# Parameter: Game state
def full_board(state):
    for row in state.board:
        if ' ' in row:
            return False
    return True



# Behavior: helper method for checking for other player
# Exceptions: None
# Returns: New player selection
# Parameter: Player
def helperForOtherPlayer(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'




# Create your own type of agent by subclassing KAgent:


class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        super().__init__(twin)
        self.twin=twin
        self.nickname = 'Asimovs Robot'
        if twin: self.nickname += '2'
        self.long_name = 'Asimovs Advanced Robot'
        if twin: self.long_name += ' II'
        self.persona = 'analytical'

        self.opponent_nickname = ""
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = None
        self.time_limit = 1.0

        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1

        self.move_count = 0
        self.last_evaluation = 0
        self.current_game_type = None
        self.playing_mode = KAgent.DEMO
        self.eval_fn = self.static_eval

    def introduce(self):
        intro = '\nBonjour! My name is Asimovs Robot.\n'+\
            '"I am really smart, and know all the positions, so I should win all the time!\n'+\
            'My creator is Ibrahim Imran\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1,
        utterances_matter=True):

        if utterances_matter:
            pass



        self.current_game_type = game_type
        self.playing = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_limit = expected_time_per_move
        return "OK"

   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):

        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0


        if special_static_eval_fn is not None:
            self.eval_fn = special_static_eval_fn
        else:
            self.eval_fn = self.static_eval


        empty = sum(row.count(' ') for row in current_state.board)
        if empty > 20:
            depth = min(3, max_ply)
        else:
            depth = min(4, max_ply)


        moves = get_every_move(current_state)
        if not moves:
            return [[None, current_state], "No moves available"]

        start = time.time()
        hard_time = time_limit if time_limit is not None else 1000

        best_move = None
        best_state = None

        best_value = float('-inf') if self.playing == 'X' else float('inf')

        alpha = float('-inf')
        beta = float('inf')

        for move, new_state in moves:
            # move check

            if time.time() - start > hard_time * 0.9:
                break

            if use_alpha_beta:
                result = self.minimax(new_state, depth - 1, hard_time, alpha, beta)
            else:
                result = self.minimax(new_state, depth - 1, hard_time, None, None)

            val = result[0]

            # now update ur best move
            if self.playing == 'X':
                if val > best_value:
                    best_value = val
                    best_move = move
                    best_state = new_state
                alpha = max(alpha, val)
            else:
                if val < best_value:
                    best_value = val
                    best_move = move
                    best_state = new_state
                beta = min(beta, val)

        if best_move is None:
            best_move, best_state = random.choice(moves)
            best_value = 0


        self.move_count += 1
        self.last_evaluation = best_value

        utterance = self.create_utterance(current_remark)

        if self.playing_mode == KAgent.AUTOGRADER:
            return [[best_move, best_state, self.alpha_beta_cutoffs_this_turn, self.num_static_evals_this_turn, -1, -1], utterance]
        else:
            return [[best_move, best_state], utterance]



    #Behvaior: utterance method
    #Exceptions: none
    #Returns; utterances
    #Parameters; self, and opponent_ remark

    def create_utterance(self, opponent_remark):
        if opponent_remark and "So... how did you do that?" in opponent_remark:
            return f"I ran my analysis on all of these {self.num_static_evals_this_turn} positions with {self.alpha_beta_cutoffs_this_turn} alpha-beta cutoffs."

        if opponent_remark and "any thoughts so far? Lock in bro!" in opponent_remark:
            return f"We've made {self.move_count} moves. Let the game rage on!!!"

        # Regular utterances
        if self.move_count <= 2:
            return "Let the carnage begin!!"
        else:
            return f"Move {self.move_count} - bee-bop, running algorithms to beat u :)."

    # The main adversarial search function:
    #Behavior : implement minimax
    #Exceptions: none
    #Parameters: state, depth_remaining, pruning, alpha, beta, timelimit
    def minimax(self, state, depth_remaining, time_limit=None, alpha=None, beta=None):

        pruning = (alpha is not None and beta is not None)

        # win checker
        winner = win_checker(state, self.current_game_type.k)
        if winner == 'X':
            return [10000]
        elif winner == 'O':
            return [-10000]


        # Base case of depth 0
        if depth_remaining == 0:
            self.num_static_evals_this_turn += 1
            return [self.eval_fn(state, self.current_game_type)]

        # get all moves:
        moves = get_every_move(state)
        if not moves:
            self.num_static_evals_this_turn += 1
            return [self.eval_fn(state, self.current_game_type)]

        best_move = None

        # for max player
        if state.whose_move == 'X':
            maxValue = float('-inf')
            for move, new_state in moves:
                result = self.minimax(new_state, depth_remaining - 1, time_limit, alpha, beta)
                val = result[0]

                if val > maxValue:
                    maxValue = val
                    best_move = move

                if pruning and alpha is not None and beta is not None:
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break

            return [maxValue, best_move]

        else:
            # for min value
            minValue = float('inf')
            for move, new_state in moves:
                result = self.minimax(new_state, depth_remaining - 1, time_limit, alpha, beta)
                val = result[0]

                if val < minValue:
                    minValue = val
                    best_move = move

                if pruning and alpha is not None and beta is not None:
                    beta = min(beta, val)
                    if beta <= alpha:
                        self.alpha_beta_cutoffs_this_turn += 1
                        break

            return [minValue, best_move]

        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def static_eval(self, state, game_type=None):

        if game_type is None:
            game_type = self.current_game_type

        if not game_type:
            return 0

        board = state.board
        k = game_type.k

        #win checker
        Winner = win_checker(state,k)
        if Winner == 'X':
            return 10000
        elif Winner == 'O':
            return -10000

        #check for full board
        if full_board(state):
            return 0

        #evals:
        score = 0
        rows = len(board)
        cols = len(board[0])

        for r in range(rows):
            for c in range(cols):

                if r + k <= rows:
                    line = [board[r+i][c] for i in range(k)]
                    score += self.eval_line(line,k)

                if c + k <= cols:
                    line = [board[r][c + i] for i in range(k)]
                    score += self.eval_line(line, k)

                if r + k <= rows and c + k <= cols:
                    line = [board[r + i][c + i] for i in range(k)]
                    score += self.eval_line(line, k)

                if r + k <= rows and c - k + 1 >= 0:
                    line = [board[r + i][c - i] for i in range(k)]
                    score += self.eval_line(line, k)
        return score


    #Behavior: Checks a single line
    #Exceptions: None
    #Returns: counts and scores
    #Parameters; self, line and k
    def eval_line(self,line, k):
        numberOfX = line.count('X')
        numberOfO = line.count('O')
        empties = line.count(' ')

        if '-' in line:
            return 0

        if numberOfX > 0 and numberOfO > 0:
            return 0

        if numberOfX > 0:
            if numberOfX == k:
                return 10000
            elif numberOfX == k - 1 and empties == 1:
                return 100
            elif numberOfX == k - 2 and empties == 2:
                return 10
            else:
                return numberOfX

        if numberOfO > 0:
            if numberOfO == k:
                return -10000
            elif numberOfO == k - 1 and empties == 1:
                    return -100
            elif numberOfO == k - 2 and empties == 2:
                    return -10
            else:
                return -numberOfO

        return 0









                # OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances



