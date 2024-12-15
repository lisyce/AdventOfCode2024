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
      if board[i][j] == "O":
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

def move_item_pt2(board, ix, iy, dx, dy):
  this_tile = board[iy][ix]
  if this_tile == "#":
    return ix, iy

  # move stuff in the way if we can
  if this_tile == "@":
    this_left_x = this_right_x = ix
  else:
    # it's a box!
    if this_tile == "]":
      this_left_x, this_right_x = ix-1, ix
    else:
      this_left_x, this_right_x = ix, ix+1

  next_tiles = [(this_left_x + dx, iy + dy), (this_right_x + dx, iy + dy)]
  for next_tile in next_tiles:
    move_item_pt2(board, next_tile[0], next_tile[1], dx, dy)  # this has issues with lateral moves

  # move this item if we can
  # if this is a fish, it's easy
  if this_tile == "@":
    if board[iy + dy][ix + dx] in "[]#":
      return ix, iy
    elif board[iy + dy][ix + dx] == ".":
      board[iy + dy][ix + dx] = board[iy][ix]
      board[iy][ix] = "."
      return ix + dx, iy + dy
  else:  # we are moving a box
    if dx == 0:  # vertical move
      pass

def item_bounds(board, ix, iy):
  this_tile = board[iy][ix]
  if this_tile in "#.@":
    return [(ix, iy)]

  if this_tile == "]":
    return [(ix, iy), (ix-1, iy)]
  else:
    return [(ix, iy), (ix+1, iy)]

def move_vertical_pt2(board, ix, iy, dy):
  #print(ix, iy, dy, board[iy][ix])
  if board[iy][ix] in "#.":
    return ix, iy
  
  this_bounds = item_bounds(board, ix, iy)
  next_tiles = [(x, y + dy) for x, y in this_bounds]
  #print(this_bounds, next_tiles)
  # move items in the way if possible
  for nt in next_tiles:
    ntnewx, ntnewy = move_vertical_pt2(board, nt[0], nt[1], dy)
    if ntnewx == nt[0] and ntnewy == nt[1]:
      # we couldn't move this item in the way
      

  # move ourself if possible
  if board[iy][ix] == "@":
    # we are the fish
    if board[iy + dy][ix] in "[]#":
      return ix, iy
    elif board[iy + dy][ix] == ".":
      board[iy + dy][ix] = board[iy][ix]
      board[iy][ix] = "."
      return ix, iy + dy
  else:
    # we are a box
    for nt in next_tiles:
      if board[nt[1]][nt[0]] != ".":
        return ix, iy
    # we can move up/down
    for tb in this_bounds:
      board[tb[1] + dy][tb[0]] = board[tb[1]][tb[0]]
      board[tb[1]][tb[0]] = "."
    return ix, iy + dy


def part_two(f) -> int:
  board, moves = parse_input(f)
  #board = double_board(board)

  fish = where_fish(board)
  for row in board:
    print("".join(row))
  for move_line in moves:
    for move in move_line:
      print(move)
      dx, dy = direction(move)
      fish = move_vertical_pt2(board, fish[1], fish[0], dy)
      for row in board:
        print("".join(row))
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