import argparse, time

def parse_input(f):
  lines = f.readlines()
  split_idx = lines.index("\n")
  board = [[l for l in line.strip()] for line in lines[:split_idx]]
  moves = [l.strip() for l in lines[split_idx+1:]]
  return board, moves

def where_fish(board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == "@":
        return (i, j)

def move_item(board, ix, iy, dx, dy):
  if board[iy][ix] == "#":
    return ix, iy
  
  # move if so then return whether we moved it
  if board[iy + dy][ix + dx] == "O":
    move_item(board, ix + dx, iy + dy, dx, dy)

  if board[iy + dy][ix + dx] in "O#":
    return ix, iy
  elif board[iy + dy][ix + dx] == ".":
    board[iy + dy][ix + dx] = board[iy][ix]
    board[iy][ix] = "."
    return ix + dx, iy + dy

def direction(move):
  if move == "<":
    return -1, 0
  elif move == "^":
    return 0, -1
  elif move == ">":
    return 1, 0
  else:
    return 0, 1

def score(board):
  total = 0
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] in "[O":
        total += 100 * i + j
  return total

def part_one(f) -> int:
  board, moves = parse_input(f)
  fish = where_fish(board)
  for move_line in moves:
    for move in move_line:
      dx, dy = direction(move)
      fish = move_item(board, fish[0], fish[1], dx, dy)
  return score(board)

def double_board(board):
  result = []
  for row in board:
    new_row = []
    for char in row:
      if char in ".#":
        new_row.append(char)
        new_row.append(char)
      elif char == "O":
        new_row.append("[")
        new_row.append("]")
      elif char == "@":
        new_row.append("@")
        new_row.append(".")
    result.append(new_row)
  return result

def box_bounds(board, ix, iy):
  this_tile = board[iy][ix]

  if this_tile == "]":
    return [ix - 1, ix, iy]
  else:
    return [ix, ix + 1, iy]

def move_box_y(board, box_pos, dy):
  # find all of the boxes in the way
  boxes_to_move = []
  stack = [box_bounds(board, box_pos[0], box_pos[1])]
  while stack:
    left, right, y = stack.pop()
    boxes_to_move.append((left, right, y))

    # can we move this box? if not, we can't move anything
    if board[y + dy][left] == "#" or board[y + dy][right] == "#":
      return
    
    # find adjacent boxes to move
    if board[y + dy][left] in "[]":
      stack.append(box_bounds(board, left, y+dy))
    if board[y + dy][right] in "[]":
      stack.append(box_bounds(board, right, y+dy))

  # we can move all the boxes, so let's do it!
  moved = set()
  while boxes_to_move:
    left, right, y = boxes_to_move.pop()
    if (left, right, y) in moved:
      continue
    moved.add((left, right, y))
    board[y][left] = "."
    board[y][right] = "."
    board[y + dy][left] = "["
    board[y + dy][right] = "]"

def move_box_x(board, box_pos, dx):
  boxes_to_move = []
  stack = [box_bounds(board, box_pos[0], box_pos[1])]
  while stack:
    left, right, y = stack.pop()
    boxes_to_move.append((left, right, y))
    
    # can we move this box? if not, we can't move anything
    next_tile_x = left - 1 if dx == -1 else right + 1
    if board[y][next_tile_x] == "#":
      return
    
    # find adjacent boxes to move
    elif board[y][next_tile_x] in "[]":
      stack.append(box_bounds(board, next_tile_x, y))

  # we can move all the boxes, so let's do it!
  moved = set()
  while boxes_to_move:
    left, right, y = boxes_to_move.pop()
    if (left, right, y) in moved:
      continue
    board[y][left] = "."
    board[y][right] = "."
    board[y][left + dx] = "["
    board[y][right + dx] = "]"

def part_two(f) -> int:
  board, moves = parse_input(f)
  board = double_board(board)

  fish = where_fish(board)
  for move_line in moves:
    for move in move_line:
      dx, dy = direction(move)
      if board[fish[0] + dy][fish[1] + dx] in "[]":
        if dy != 0:
          move_box_y(board, (fish[1], fish[0]+dy), dy)
        elif dx != 0:
          move_box_x(board, (fish[1]+dx, fish[0]), dx)
      if board[fish[0] + dy][fish[1] + dx] == ".":
        board[fish[0]][fish[1]] = "."
        fish = (fish[0] + dy, fish[1] + dx)
        board[fish[0]][fish[1]] = "@"

  return score(board)

if __name__ == "__main__":  
  parser = argparse.ArgumentParser()
  parser.add_argument("parts", nargs="*")
  parser.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
  args = parser.parse_args()
  
  file_name = "input_test.txt" if args.test else "input.txt"
  f = open(file_name)
  
  run_pt_1 = not args.parts or "1" in args.parts
  run_pt_2 = not args.parts or "2" in args.parts
  
  if run_pt_1:
    start = time.perf_counter()
    pt_1_result = part_one(f)
    elapsed = (time.perf_counter() - start) * 1000 
    
    print("Part One:", pt_1_result, "(Ran in", round(elapsed, 8), "ms)")
  
  f.seek(0)
  
  if run_pt_2:
    start = time.perf_counter()
    pt_2_result = part_two(f)
    elapsed = (time.perf_counter() - start) * 1000 
    
    print("Part Two:", pt_2_result, "(Ran in", round(elapsed, 8), "ms)")
    
  f.close()