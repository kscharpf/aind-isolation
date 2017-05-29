"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

score_cache = {}

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

def is_not_reflectable(newPosition, player1Pos):
    return abs(newPosition[0] - player1Pos[0]) != abs(newPosition[1] - player1Pos[1])

def does_reflect(newPosition, player2Pos):
    return abs(newPosition[0] - player2Pos[0]) == abs(newPosition[1] - player2Pos[1])

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

    if game.move_count == 0:
        if game.get_player_location(player) == (game.height//2, game.width//2):
            return float(999)
    elif game.move_count % 2 == 1:
        if is_not_reflectable(game.get_player_location(player), game.get_player_location(game.get_opponent(player))): 
            return float(999)
    elif game.move_count % 2 == 0:
        if does_reflect(game.get_player_location(player), game.get_player_location(game.get_opponent(player))):
            return float(999)

    return float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))
    raise NotImplementedError


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
    return float(len(game.get_legal_moves(player)))


def custom_score_3(game, player):
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
    return float(len(game.get_legal_moves(game.active_player)) - len(game.get_legal_moves(game.inactive_player)))
    raise NotImplementedError


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

        moves = game.get_legal_moves(game.active_player)
        if not moves:
            return (-1,-1), float("-inf")

        #if game.to_string() in score_cache:
            #return score_cache[game.to_string()]
            
        if depth == 0:
            return moves[0],self.score(game, game.active_player)

        bestV = float("-inf")
        bestMove = moves[0]
        for m in moves:
            game2 = game.forecast_move(m)
            bm,v = self.minimax_minvalue(game2, depth-1)
            if v > bestV:
                bestV = v
                bestMove = m
        return bestMove,bestV
#
    def minimax_minvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves(game.active_player)
        if not moves:
            if depth == 0:
                return (-1,-1), self.score(game, game.active_player)
            return (-1,-1), float("inf")

        #if game.to_string() in score_cache:
            #return score_cache[game.to_string()]
            
        if depth == 0:
            return moves[0],self.score(game, game.active_player)

        bestV = float("inf")
        bestMove = moves[0]
        for m in moves:
            game2 = game.forecast_move(m)
            bm,v = self.minimax_maxvalue(game2, depth-1)
            if v <= bestV:
                bestV = v
                bestMove = m

        return bestMove,bestV

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

        #try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
        best_move, _ = self.minimax_maxvalue(game, depth)
        return best_move

        #except SearchTimeout:
            #pass  # Handle any actions required after timeout as needed

        if best_move == (-1,-1):
            moves = game.get_legal_moves(game.active_player)
            if moves:
                best_move = moves[0]
        return best_move
        # TODO: finish this function!
        #raise NotImplementedError


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

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        if best_move == (-1,-1):
            moves = game.get_legal_moves(game.active_player)
            if moves:
                return moves[0]
        return best_move

    def alphabeta_maxvalue(self, game, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves(game.active_player)
        if not moves:
            return (-1,-1), float("-inf")

        if game.to_string() in score_cache:
            return score_cache[game.to_string()]
            
        if depth == 0:
            return moves[0],self.score(game, game.active_player)

        bestV = float("-inf")
        bestMove = moves[0]
        for m in moves:
            game2 = game.forecast_move(m)
            bestMinMove,v = self.alphabeta_minvalue(game2, depth-1, alpha, beta)
            if v > bestV:
                bestV = v
                bestMove = m
            if bestV >= beta:
                return bestMove, bestV
            alpha = max(alpha, bestV)
        if bestV == float("inf") or bestV == float("-inf"):
            score_cache[game.to_string()] = (bestMove, bestV)
        return bestMove, bestV

    def alphabeta_minvalue(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves(game.active_player)
        if not moves:
            return (-1,-1), float("inf")

        if game.to_string() in score_cache:
            return score_cache[game.to_string()]

        if depth == 0:
            return moves[0],self.score(game, game.active_player)


        bestV = float("inf")
        bestMove = (-1,-1)
        for m in moves:
            game2 = game.forecast_move(m)
            bestMaxMove,v = self.alphabeta_maxvalue(game2, depth-1, alpha, beta)
            if v < bestV:
                bestV = v
                bestMove = m
            if bestV <= alpha:
                return bestMove, bestV
            beta = min(beta, bestV)
        if bestV == float("inf") or bestV == float("-inf"):
            score_cache[game.to_string()] = (bestMove, bestV)
        return bestMove, bestV


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

        return self.alphabeta_maxvalue(game, depth, alpha, beta)[0]