"""Simple 5x5 Boggle game solver.

Free to use under the New BSD License:
http://opensource.org/licenses/BSD-3-Clause

"""

import optparse
import random

MIN_LENGTH = 4
DICTIONARY = set()
PREFIXES = {}
WIDTH = 5
HEIGHT = 5
SCORES = {4: 1, 5: 2, 6: 3, 7: 5, None: 11}
OFFSETS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
CUBES = [s.lower().split() for s in [
    'S N S U S E',
    'A R Y I F S',
    'O H H L R D',
    'T E T M O T',
    'J K B X Qu Z',
    'T E T I I I',
    'E T P S C I',
    'E E E E M A',
    'S A R A I F',
    'F R Y S I P',
    'E A E A E E',
    'N D N A N E',
    'N T D H H O',
    'Y I R P R H',
    'N R L D D O',
    'L I T C E P',
    'H D R O L N',
    'N N E M G A',
    'W U N T O O',
    'A A A F R S',
    'C C W N T S',
    'O T O U T O',
    'L I T C E I',
    'O V W R R G',
    'M E A G E U',
]]

def load_dictionary():
    global DICTIONARY
    global PREFIXES

    DICTIONARY = set()
    with open('words.txt') as f:
        for line in f:
            word = line.strip()
            if len(word) >= MIN_LENGTH and word.isalpha():
                DICTIONARY.add(word.lower())

    PREFIXES = {}
    for word in sorted(DICTIONARY):
        node = PREFIXES
        for letter in word:
            if letter not in node:
                node[letter] = {}
            node = node[letter]

    print len(DICTIONARY), 'words loaded'
    print '----'

def is_prefix(prefix):
    node = PREFIXES
    for letter in prefix:
        if letter not in node:
            return False
        node = node[letter]
    return True

# given a dictionary, prefixes, and a Boggle board, find all viable words in the board
# (x, y)
# (0, 0) is the left-top most corner
# T N N H A
# I G N E I
# S G E I B
# C A H N I
# O N F O E

# board is in the form 
# {(1, 3): 'a', (3, 0): 'h', (2, 1): 'n', (0, 3): 'c', (4, 0): 'a', (1, 2): 'g', (3, 3): 'n', (4, 4): 'e', (0, 4): 'o', (4, 1): 'i', (1, 1): 'g', (3, 2): 'i', (0, 0): 't', (2, 2): 'e', (1, 4): 'n', (2, 3): 'h', (4, 2): 'b', (1, 0): 'n', (0, 1): 'i', (3, 1): 'e', (2, 4): 'f', (2, 0): 'n', (4, 3): 'i', (3, 4): 'o', (0, 2): 's'}


# returns a set of found words
def find_words(board, positions_used, prefix, pos):
    prefix = prefix + board[pos] # update prefix
    if not is_prefix(prefix):
        # no words with this as a prefix
        return set() # return an empty set

    found = set()
    if prefix in DICTIONARY:
        found.add(prefix)
    positions_used.add(pos) # keep track of which coordinates we've visited

    for offset in OFFSETS:
        new_pos = (pos[0] + offset[0], pos[1] + offset[1])
        if new_pos in positions_used:
            continue
        if not (0 <= new_pos[0] < WIDTH and 0 <= new_pos[1] < HEIGHT):
            continue

        found.update(find_words(board, positions_used, prefix, new_pos))

    positions_used.remove(pos) # reset for use in other recursive calls
    return found

def solve(board):
    words = set()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            found = find_words(board, set(), '', (x, y)) # initialize empty set and prefix for first call
            words.update(found) # update set words with elements from set found
    return words

def make_board(letters=None): 
    if letters is None:
        cubes = list(CUBES)
        random.shuffle(cubes)
        letters = ' '.join(random.choice(cube) for cube in cubes)
    board = {}
    y = 0
    x = 0
    for letter in letters.split():
        board[x, y] = letter.lower()
        x += 1
        if x >= WIDTH:
            x = 0
            y += 1
    return board

def print_board(board):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            letter = board[x, y]
            if letter == 'qu':
                letter = 'Qu'
            else:
                letter = letter.upper()
            print letter,
        print

def main():
    load_dictionary()

    usage = """Usage: %prog [board_letters]

Example: %prog  T N N H A  I G N E I  S G E I B  C A H N I  O N F O E"""
    parser = optparse.OptionParser(usage=usage)
    options, args = parser.parse_args()

    if args:
        board = make_board(letters=' '.join(args))
    else:
        board = make_board()

    print_board(board)
    print board
    print '----'
    words = solve(board)
    total_score = 0
    for word in sorted(words):
        word_score = SCORES.get(len(word), SCORES[None])
        total_score += word_score
        # print word

    print '----'
    print 'Total score:', total_score, 'from', len(words), 'words'

if __name__ == '__main__':
    main()
