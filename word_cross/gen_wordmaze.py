"""The main file that generates the puzzle and also has the game loop.

To run the script:
1. python gen_wordmaze.py
"""

import json
import random

g_max_w = 25  # upper bound on the grid size
g_max_h = 15

with open('map_idx_word.json') as json_f:
    g_words_list = json.load(json_f)

with open('map_word_idx.json') as json_f:
    g_words_dict = json.load(json_f)

with open('merged_graph.json') as json_f:
    g_word_graph = json.load(json_f)

g_scrabble_scores = {
    1: {'a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r'},
    2: {'d', 'g'},
    3: {'b', 'c', 'm', 'p'},
    4: {'f', 'h', 'v', 'w', 'y'},
    5: {'k'},
    8: {'j', 'x'},
    10: {'q', 'z'}
}


def initialize_grid(seed):
    """
    Initializes the grid with the seed word at (0,0).
    :param seed: The number used to refer to the word input by the user. (int)
    :return: [<loc and orientation of the word>, <coords of the bounding rect>, <Coords and visibility of each char>]
    """
    word_len = len(g_words_list[seed])
    all_gridwords = dict()
    all_gridwords[seed] = [(0, 0), '^']

    rect = [[0, 0], [1, word_len]]  # bounding rectangle

    coords = {}
    for x in range(rect[0][0], rect[1][0]):
        for y in range(rect[0][1], rect[1][1]):
            char = g_words_list[seed][y]
            parent_id = seed
            direction = '>'
            coords[(x, y)] = (char, parent_id, direction, 'V')

    # completed = {seed}
    return [all_gridwords, rect, coords]


def empty_h(coord_set, origin, left_idx, right_idx):
    """Makes sure no conflicts occur when a word is placed horizontally.
    
    :param coord_set: Set of all 'filled' coordinates.
    :param origin: Starting (x,y) index for the new word to be placed.
    :param left_idx: The left 'edge' for the new word.
    :param right_idx: The right 'edge' for the new word.
    :return: True if there is no conflict, False otherwise.
    """
    # print(origin)
    top = origin[1] - 1
    bot = origin[1] + 1
    ex = origin[0]
    for idx in range(left_idx, right_idx + 1):
        if idx == ex:
            continue
        # print((idx, top))
        # print((idx, bot))
        if (idx, top) in coord_set or (idx, bot) in coord_set:
            return False

    return True


def empty_v(coord_set, origin, top_idx, bot_idx):
    """Makes sure no conflicts occur when a word is placed vertically.
    The parameters and return values are similar to the function, empty_h()
    """
    # print(origin)
    left = origin[0] - 1
    right = origin[0] + 1
    ex = origin[1]
    for idx in range(top_idx, bot_idx + 1):
        if idx == ex:
            continue
        # print((idx, left))
        # print((idx, right))
        if (left, idx) in coord_set or (right, idx) in coord_set:
            return False

    return True


def rand_next_moves(grid, ch):
    """Given a character, ch, on the grid, a next move (i.e. a new word) is chosen randomly.
    Provided no constraints are broken.
    
    :param grid: The entire grid. 
    :param ch: A single location and character on the grid.
    :return: A new word and location chosen at random.
    """

    already_used = grid[0]
    boundary = grid[1]
    node_details = grid[2][ch]
    character = node_details[0]
    parent_id = str(node_details[1])
    direction = node_details[2]
    potential_words = g_word_graph[parent_id]

    next_moves = []
    for w_n in potential_words:
        w_ = g_words_list[w_n]
        if character in w_ and w_n not in already_used:
            indices = [idx for idx, cx in enumerate(w_) if cx == character]
            for idx in indices:
                # print(w_)
                lw = len(w_)
                # print(lw)
                if direction == '>':
                    left_idx = min(ch[0]-idx, boundary[0][0])
                    # print(left_idx)
                    right_idx = max(boundary[1][0], ch[0] + lw - idx)
                    # print(right_idx)
                    total_width = right_idx - left_idx
                    # print("total width: ", end=": ")
                    # print(total_width)
                    if total_width <= g_max_w and empty_h(grid[2], ch, left_idx, right_idx):
                        next_moves.append([w_n, ch[0] - idx])
                elif direction == '^':
                    top_idx = min(ch[1]-idx, boundary[0][1])
                    bot_idx = max(boundary[1][1], ch[1] + lw - idx)
                    total_width = bot_idx - top_idx
                    if total_width <= g_max_h and empty_v(grid[2], ch, top_idx, bot_idx):
                        next_moves.append([w_n, ch[1] - idx])

    # print(next_moves)
    # print(len(next_moves))
    if len(next_moves) > 0:
        return random.choice(next_moves)
    else:
        return []


def update_bounds(bounds, new_word, direction):
    """Check and update the rectangular bounds containing the grid.
    
    :param bounds: The current bounds.
    :param new_word: Contains the new word and it's location in the grid.
    :param direction: Vertical or horizontal, tells us which boundary could potentially change.
    :return: None
    """
    ll = len(g_words_list[new_word[0]])
    if direction == '>':
        left_idx = new_word[1]
        right_idx = new_word[1] + ll
        if left_idx < bounds[0][0]:
            bounds[0][0] = left_idx
        if right_idx > bounds[1][0]:
            bounds[1][0] = right_idx
    elif direction == '^':
        top_idx = new_word[1]
        bot_idx = new_word[1] + ll
        if top_idx < bounds[0][1]:
            bounds[0][1] = top_idx
        if bot_idx > bounds[1][1]:
            bounds[1][1] = bot_idx


def update_chars(char_set, start_loc, direction, m):
    """Adds new characters to the grid.
    
    :param char_set: Dictionary of characters on the grid.
    :param start_loc: Point on the grid where the new word meets the old. (This location need not be updated)
    :param direction: Vertical or Horizontal.
    :param m: Contains the new word and also it's location.
    :return: 
    """
    if direction == '>':
        left_idx = m[1]
        right_idx = len(g_words_list[m[0]]) + left_idx
        for idx in range(left_idx, right_idx):
            if idx == start_loc[0]:
                continue
            char_set[(idx, start_loc[1])] = (g_words_list[m[0]][idx-left_idx], m[0], '^', 'H')
    elif direction == '^':
        top_idx = m[1]
        bot_idx = len(g_words_list[m[0]]) + top_idx
        for idx in range(top_idx, bot_idx):
            if idx == start_loc[1]:
                continue
            char_set[(start_loc[0], idx)] = (g_words_list[m[0]][idx-top_idx], m[0], '>', 'H')


def monte_carlo(grid):
    """Randomly picks a character on the grid and the next word that crosses it.
    Repeats this process X=2000 times. 
    
    :param grid: The entire grid. 
    :return: None.
    """
    char_locs = grid[2]
    for _ in range(0, 2000):  # randomize X times
        r = random.choice(list(char_locs))
        m = rand_next_moves(grid, r)
        if len(m) > 0:
            # print(g_words_list[m[0]])
            direction = grid[2][r][2]
            grid[0][m[0]] = [r, direction]
            update_bounds(grid[1], m, direction)
            update_chars(grid[2], r, direction, m)
            # print(grid)
            t = list(grid[2][r])
            t[2] = '.'
            grid[2][r] = tuple(t)


def viz_console(grid):
    """Visualizes the grid on the console.
    
    :param grid: The entire grid.
    :return: None.
    """
    board = grid[2]

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for k in board:
        if k[0] < min_x:
            min_x = k[0]
        if k[1] < min_y:
            min_y = k[1]
        if k[0] > max_x:
            max_x = k[0]
        if k[1] > max_y:
            max_y = k[1]

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x + 1):
            if (x, y) in board:
                if board[(x, y)][3] == 'V':
                    print(board[(x, y)][0].upper(), end=" ")
                elif board[(x, y)][3] == 'H':
                    print("_", end=" ")
            else:
                print(" ", end=" ")
        print("")


def get_next_hint(grid):
    """Picks one of the hidden letters as the next hint.
    
    :param grid: The grid.
    :return: A hidden letter if any exists.
    """
    letters = grid[2]
    dup = set()
    hidden_letters = set()
    for l in letters:
        if letters[l][3] == 'H' or letters[l][3] == 'h' and letters[l][0] not in dup:
            dup.add(letters[l][0])
            hidden_letters.add(l)
    # print(hidden_letters)
    if len(hidden_letters) > 0:
        return letters[random.sample(hidden_letters, 1)[0]]
    else:
        return {}


def make_visible(grid, c):
    """Makes the all the characters, c, visible on the grid.
    
    :param grid: The grid.
    :param c: A hidden character.
    :return: None.
    """
    letters = grid[2]
    for l in letters:
        if letters[l][0] == c:
            temp = list(letters[l])
            temp[3] = 'V'
            letters[l] = tuple(temp)


def find_top(char_locs, pt):
    """Finds the 'top' coord of a word that a character belongs to.
    
    :param char_locs: All character locations on the grid. 
    :param pt: The coord of the required character.
    :return: The 'top' coord.
    """
    if pt not in char_locs:
        return []

    l = list(pt)
    while (l[0], l[1]-1) in char_locs:
        l = [l[0], l[1]-1]

    return l


def find_left(char_locs, pt):
    """Finds the 'left' coord of a word that a character belongs to.
    Similar to find_top()    
    """
    if pt not in char_locs:
        return []

    l = list(pt)
    while (l[0]-1, l[1]) in char_locs:
        l = [l[0]-1, l[1]]

    return l


def find_score(letter):
    """Finds the scrabble score of the given letter.
    
    :param letter: A letter.
    :return: The scrabble score.
    """
    for x in g_scrabble_scores:
        if letter in g_scrabble_scores[x]:
            return x


def check_end_condition(grid):
    """The end condition: There are no more hidden characters.
    
    :param grid: The grid. 
    :return: Returns False if there still are hidden characters, otherwise returns True.
    """
    char_locs = grid[2]
    for x in char_locs:
        if char_locs[x][3] == 'H' or char_locs[x][3] == 'h':
            return False
    return True


def start():
    """The main function. Contains user interaction. The Game Loop. Scoring and the end condition.
    
    :return: None.
    """

    # seed_word = 34330  # rain
    random.seed()

    while True:
        word = input('Enter a word to begin: ')
        word = word.strip().lower()
        if word in g_words_dict:
            seed_word = g_words_dict[word]
            break
        else:
            print("Sorry! Please enter another word.")

    print("Generating Puzzle...")
    trials = 75
    max_score = 0
    max_grid = {}
    for _ in range(0, trials):
        grid = initialize_grid(seed_word)
        monte_carlo(grid)
        # viz_console(grid)
        score = len(grid[2])
        if score > max_score:
            max_score = score
            max_grid = grid
        prev_perc = 100*(_-1)/(trials-1)
        perc_done = 100*_/(trials-1)
        if int(int(perc_done) / 10) > int(int(prev_perc) / 10) and int(int(perc_done) / 10) % 2 == 0:
            print("="*(int(perc_done/10)*5), end=": ")
            print((int(perc_done/10)*10), end="% done.\n")

    print("\nGame On! (H for hints, Q to quit)")
    grid = max_grid
    viz_console(grid)

    my_score = 0
    while True:
        # print(grid)
        print("\nYour Score = ", end="")
        print(my_score)

        query = input('Type a word > ')
        query = query.strip().lower()

        if query == 'q':
            exit(0)
        if query == 'h':
            c = get_next_hint(grid)
            # print(len(c))
            if len(c) > 0:
                make_visible(grid, c[0])
                viz_console(grid)
        else:
            if query in g_words_dict and g_words_dict[query] in grid[0]:
                w_len = len(query)
                start_pt = grid[0][g_words_dict[query]][0]
                direction = grid[0][g_words_dict[query]][1]
                loc = grid[2][start_pt]
                if direction == '>':
                    left_pt = find_left(grid[2], start_pt)
                    for _ in range(0, w_len):
                        k = (left_pt[0]+_, left_pt[1])
                        # print(k, end=": ")
                        # print(grid[2][k])
                        t = list(grid[2][k])
                        if len(t) >= 4 and t[3] == 'H':
                            my_score += find_score(t[0])
                        t[3] = 'V'
                        grid[2][k] = tuple(t)
                elif direction == '^':
                    top_pt = find_top(grid[2], start_pt)
                    # print("top = ", end="")
                    # print(top_pt)
                    for _ in range(0, w_len):
                        k = (top_pt[0], top_pt[1]+_)
                        # print(k, end=": ")
                        # print(grid[2][k])
                        t = list(grid[2][k])
                        if len(t) >= 4 and t[3] == 'H':
                            my_score += find_score(t[0])
                        t[3] = 'V'
                        grid[2][k] = tuple(t)

                viz_console(grid)
        game_over = check_end_condition(grid)
        if game_over:
            print("\nGame Over! Your final score: "+str(my_score))
            break


start()
