import itertools

import numpy as np
import pandas as pd

box_starts = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
box_slices = {(i, j): (slice(i, i + 3), slice(j, j + 3)) for i, j in box_starts}


def legal_coords(shape, board):
    i_max, j_max = 9 - np.array(shape.shape) + 1
    for i, j in itertools.product(range(i_max), range(j_max)):
        try:
            play(shape, board.copy(), i, j)
            yield i, j
        except AssertionError:
            ...


def play(shape, board, i, j):
    assert i <= 9 - shape.shape[0]
    assert j <= 9 - shape.shape[1]
    for i_shape, j_shape in itertools.product(range(shape.shape[0]), range(shape.shape[1])):
        if shape[i_shape, j_shape] == 1:
            assert board[i + i_shape, j + j_shape] == 0, "overlap"
    for i_shape, j_shape in itertools.product(range(shape.shape[0]), range(shape.shape[1])):
        if shape[i_shape, j_shape] == 1:
            board[i + i_shape, j + j_shape] = 1


score_coefs = {
    0: 0,
    1: 1,
    2: 3,   # x1.5
    3: 6,   # x2
    4: 10,  # x2.5
    5: 15,  # x3
    6: 21,  # x3.5
}


def score(board):
    board_score = 0
    def is_full_box(i, j):
        #return board[box_slices[i, j]].all()
        return board[i, j] == board[i + 1, j] == board[i + 2, j] == \
               board[i, j + 1] == board[i + 1, j + 1] == board[i + 2, j + 1] == \
               board[i, j + 2] == board[i + 1, j + 2] == board[i + 2, j + 2] == 1
    
    cleared_boxes = [(i, j) for i, j in box_starts if is_full_box(i, j)]
    cleared_rows = board.sum(axis=1) == 9
    cleared_cols = board.sum(axis=0) == 9
    
    box_score = len(cleared_boxes)
    row_score = cleared_rows.sum()
    col_score = cleared_cols.sum()
    
    for i, j in cleared_boxes:
        board[box_slices[i, j]] = 0
    board[cleared_rows, :] = 0
    board[:, cleared_cols] = 0
    
    simple_score = box_score + row_score + col_score
    boosted_score = score_coefs[simple_score]
    return simple_score, boosted_score
    

def anticipation_score(board):
    almost_cleared_rows = board.sum(axis=1) == 8
    almost_cleared_cols = board.sum(axis=0) == 8
    return 0.2 * (almost_cleared_rows.sum() + almost_cleared_cols.sum())


def play_shape(shape, board, i, j):
    try:        
        play(shape, board, i, j)
        return score(board)
    except AssertionError:
        return 0, 0
    

def display_best_plays(attempts, board, hand, display_max=3):
    top_attempts = pd.DataFrame(attempts).drop_duplicates().sort_values("score", ascending=False).reset_index(drop=True)
    sorted_columns = ["score", "i0", "j0", "i1", "j1", "i2", "j2"]
    other_columns = [column for column in top_attempts.columns if column not in sorted_columns]
    top_attempts = top_attempts[sorted_columns + other_columns]
    display(top_attempts.score.value_counts(ascending=True)[:3])
    for i in range(display_max):
        if top_attempts.shape[0] > i:
            display(top_attempts.iloc[i:i+1])
            display(display_hand(board, hand, top_attempts.iloc[i]))


def display_hand(board, hand, attempt):
    df = pd.DataFrame(board).replace(0, '').replace(1, '.')
    hand0, hand1, hand2 = hand
    for i, j in itertools.product(range(hand0.shape[0]), range(hand0.shape[1])):
        if hand0[i, j] == 1 and not pd.isna(attempt.i0):
            df.iloc[int(attempt.i0 + i), int(attempt.j0 + j)] = attempt.order.index(0)
    for i, j in itertools.product(range(hand1.shape[0]), range(hand1.shape[1])):
        if hand1[i, j] == 1 and not pd.isna(attempt.i1):
            df.iloc[int(attempt.i1 + i), int(attempt.j1 + j)] = attempt.order.index(1)
    for i, j in itertools.product(range(hand2.shape[0]), range(hand2.shape[1])):
        if hand2[i, j] == 1 and not pd.isna(attempt.i2):
            df.iloc[int(attempt.i2 + i), int(attempt.j2 + j)] = attempt.order.index(2)
    return df


def display_board(board):
    df = pd.DataFrame(board)
    def display_cell(value, i, j):
        if not value:
            return ""
        if 0 <= i <= 2:
            if 0 <= j <= 2:
                return "a"
            elif 3 <= j <= 5:
                return "b"
            elif 6 <= j <= 8:
                return "c"
        elif 3 <= i <= 5:
            if 0 <= j <= 2:
                return "d"
            elif 3 <= j <= 5:
                return "e"
            elif 6 <= j <= 8:
                return "f"
        elif 6 <= i <= 8:
            if 0 <= j <= 2:
                return "g"
            elif 3 <= j <= 5:
                return "h"
            elif 6 <= j <= 8:
                return "i"
        print(value, i, j)
        return value

    return pd.DataFrame([
        [display_cell(value, i, j) for j, value in enumerate(row)]
        for i, row in df.iterrows()
    ])

