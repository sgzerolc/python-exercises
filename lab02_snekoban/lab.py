# 6.009 Lab 2: Snekoban

import json
import typing

# NO ADDITIONAL IMPORTS!

direction_vector = {
    # trick you :)
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
    # "up": (0, -1),
    # "down": (0, 1),
    # "left": (-1, 0),
    # "right": (1, 0),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    row_j, col_i = len(level_description[0]), len(level_description)
    new_board = {}
    new_board['target'], new_board['count_i_j'] = set(), (row_j, col_i)
    for j in range(row_j):
        for i in range(col_i):
            checkbox = level_description[i][j]
            if 'player' in checkbox:   # store player's location(one-player game)
                new_board['player'] = (i, j)
            if 'target' in checkbox:
                new_board['target'].add((i, j))
            new_board[(i, j)] = frozenset(level_description[i][j])
    return new_board


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    if len(game['target']) == 0:
        return False
    for loc in game['target']:
        if 'computer' not in game[loc]:
            return False
    return True

def adder(x, y):
    return (x[0]+y[0], x[1]+y[1])

def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    # add_tuple using lambda
    new_dict = {'target': game['target'], 'count_i_j': game['count_i_j'],
                'player': game['player']}
    row_j, col_i = game['count_i_j']
    for j in range(row_j):
        for i in range(col_i):
            new_dict[(i, j)] = set(game[(i, j)])

    # player's basic operations, assuming no other objects
    # set current loc and update next loc

    old_loc = game['player']
    new_loc = adder(old_loc, direction_vector[direction])

    # wall's case: wall will not be moved
    if 'wall' in game[new_loc]:
        return game

    # computer's case: pushing behavior
    # pushing everywhere
    if 'computer' in game[new_loc]:
        new_pc_loc = adder(new_loc, direction_vector[direction])

        # misc case: cannot be moved if there is wall or computer
        if 'computer' in new_dict[new_pc_loc] or 'wall' in new_dict[new_pc_loc]:
            return game

        # move operation:
        new_dict[new_pc_loc].add('computer')
        new_dict[new_loc].remove('computer')

    # general case: 1) player steps into target zone;
    new_dict[new_loc].add('player')
    # 2) player steps out target zone
    new_dict[old_loc].remove('player')
    # new_dict[old_loc] = set()
    new_dict['player'] = new_loc

    return new_dict



def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    row_j, col_i = game['count_i_j']
    old_game = []
    for i in range(col_i):
        rows = []
        for j in range(row_j):
            rows.append(list(game[(i, j)]))
        old_game.append(rows)
    return old_game

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    

if __name__ == "__main__":
    # simple case: player's world
    board = [
        [['wall'], ['wall'], ['wall'], ['wall']],
        [['wall'], [], ['wall'], ['wall']],
        [['wall'], ['computer'], ['wall'], ['wall']],
        [['wall'], ['player'], ['wall'], ['wall']],
        [['wall'], ['wall'], ['wall'], ['wall']]
    ]

    # computer case
    new_board = new_game(board)
    new_pc_config = step_game(new_board, "up")
    assert(new_pc_config['player'] == (2, 1))
    assert(new_pc_config[(1, 1)] == {'computer'})
    print(new_board)
    print(dump_game(new_board))
    # assert(board == )

    # misc case




