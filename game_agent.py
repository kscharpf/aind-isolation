"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def distance_to_player(game, p1, p2):
    p1pos = game.get_player_location(p1)
    p2pos = game.get_player_location(p2)

    return float((p1pos[0] - p2pos[0])**2 + (p1pos[1] - p2pos[1])**2)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    return 1.*len(game.get_legal_moves(player)) - 2. * len(game.get_legal_moves(game.get_opponent(player)))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    return distance_to_player(game, player, game.get_opponent(player))
        
PositionValue = {
        (0,0):-50.,
        (0,1):-40.,
        (0,2):-30.,
        (0,3):-30.,
        (0,4):-30.,
        (0,5):-40.,
        (0,6):-50.,
        (6,1):-40.,
        (6,2):-30.,
        (6,3):-30.,
        (6,4):-30.,
        (6,5):-40.,
        (6,6):-50.,
        (1,0):-40.,
        (2,0):-30.,
        (3,0):-30.,
        (4,0):-30.,
        (5,0):-40.,
        (6,0):-50.,
        (1,6):-40.,
        (2,6):-30.,
        (3,6):-30.,
        (4,6):-30.,
        (5,6):-40.,
        (6,6):-50.,
        (1,1):-20.,
        (1,2):0.,
        (1,3):0.,
        (1,4):0.,
        (1,5):-20.,
        (2,1):0.,
        (3,1):0.,
        (4,1):0.,
        (5,1):-20.,
        (5,2):0.,
        (5,3):0.,
        (5,4):0.,
        (5,5):-20.,
        (2,5):0.,
        (3,5):0.,
        (4,5):0.,
        (2,2):10.,
        (2,3):15.,
        (2,4):10.,
        (3,2):15.,
        (4,2):10.,
        (4,3):15.,
        (4,4):10.,
        (3,4):10.,
        (3,3):20.}


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    player_loc = game.get_player_location(player)
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    return PositionValue[game.get_player_location(player)] * len(game.get_legal_moves(player)) -  \
           PositionValue[game.get_player_location(game.get_opponent(player))] * len(game.get_legal_moves(game.get_opponent(player)))

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=open_move_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.name=""
    def __repr__(self):
        return "IsolationPlayer:{}".format(self.name)


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax_maxvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, game.active_player)

        bestV = float("-inf")
        moves = game.get_legal_moves(game.active_player)
        for m in moves:
            game2 = game.forecast_move(m)
            v = self.minimax_minvalue(game2, depth-1)
            if v > bestV:
                bestV = v
        return bestV
#
    def minimax_minvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            return self.score(game, game.inactive_player)

        bestV = float("inf")
        moves = game.get_legal_moves(game.active_player)
        for m in moves:
            game2 = game.forecast_move(m)
            v = self.minimax_maxvalue(game2, depth-1)
            if v <= bestV:
                bestV = v

        return bestV

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)
        moves = game.get_legal_moves(game.active_player)
        if moves:
            best_move = moves[random.randint(0,len(moves)-1)]
        bestVal = float("-inf")
        for m in moves:
            game2 = game.forecast_move(m)
            val = self.minimax_minvalue(game2, depth-1)
            if val > bestVal:
                bestVal = val
                best_move = m
        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)
        best_val = float("-inf")

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
                #if depth > 6:
                    #print("break")
                    #break
                if best_move == (-1,-1):
                    break

        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        if best_move == (-1,-1):
            moves = game.get_legal_moves(game.active_player)
            if moves:
                best_move = moves[random.randint(0,len(moves)-1)]
        return best_move

    def alphabeta_maxvalue(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, game.active_player)

        bestV = float("-inf")
        moves = game.get_legal_moves(game.active_player)
        for m in moves:
            game2 = game.forecast_move(m)
            v = self.alphabeta_minvalue(game2, depth-1, alpha, beta)
            if v > bestV:
                bestV = v
            if bestV >= beta:
                return bestV
            alpha = max(alpha, bestV)
        return bestV
#
    def alphabeta_minvalue(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            return self.score(game, game.inactive_player)

        bestV = float("inf")
        moves = game.get_legal_moves(game.active_player)
        for m in moves:
            game2 = game.forecast_move(m)
            v = self.alphabeta_maxvalue(game2, depth-1, alpha, beta)
            if v < bestV:
                bestV = v
            if bestV <= alpha:
                return bestV
            beta = min(beta, bestV)
        return bestV

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)
        moves = game.get_legal_moves(game.active_player)
        if moves:
            best_move = moves[0]
        bestVal = float("-inf")
        for m in moves:
            game2 = game.forecast_move(m)
            val = self.alphabeta_minvalue(game2, depth-1, alpha, beta)
            if val > bestVal:
                bestVal = val
                best_move = m
            if val >= beta:
                return m
            alpha = max(alpha, val)
        return best_move
