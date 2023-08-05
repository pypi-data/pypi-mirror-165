import numpy as np

def _try_merge(row):
    score = 0
    result_row = []

    i = 1
    while i < len(row):
      if row[i] == row[i - 1]:
        score += row[i] + row[i - 1]
        result_row.append(row[i] + row[i - 1])
        i += 2
      else:
        result_row.append(row[i - 1])
        i += 1

    if i == len(row):
      result_row.append(row[i - 1])

    return score, result_row

def _slide_left_and_merge(board):
    """Slide tiles on a grid to the left and merge."""

    result = []

    score = 0
    for row in board:
      row = np.extract(row > 0, row)
      score_, result_row = _try_merge(row)
      score += score_
      row = np.pad(np.array(result_row), (0, board.shape[0] - len(result_row)),
                   'constant', constant_values=(0,))
      result.append(row)

    return score, np.array(result, dtype=np.int64)

def is_done(board):
    copy_board = board.copy()

    if not copy_board.all():
      return False

    for action in [0, 1, 2, 3]:
      rotated_obs = np.rot90(copy_board, k=action)
      _, updated_obs = _slide_left_and_merge(rotated_obs)
      if not updated_obs.all():
        return False

    return True

def action_possible(board, action):
    copy_board = board.copy()

    #an action is not possible, if no squares would move/merge

    
    rotated_obs = np.rot90(copy_board, k=action)
    _, updated_obs = _slide_left_and_merge(rotated_obs.copy())
    
    #action is possible, if the result is changed from the original plus action    
    return not np.array_equal(rotated_obs, updated_obs)

def action_names():
   return { 0: "LEFT", 1: "UP", 2: "RIGHT", 3:"DOWN"}