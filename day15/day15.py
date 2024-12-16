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

def box_bounds(board, ix, iy):
  this_tile = board[iy][ix]

  if this_tile == "]":
    return [ix-1, ix, iy]
  else:
    return [ix, ix + 1, iy]

def move_box_y(board, box_pos, dy):
  bounds = box_bounds(board, box_pos[0], box_pos[1])
  stack = [bounds]

  # is there space for all of the boxes to move?
  y = box_pos[1] + dy
  # while y >= 0 and y < len(board):
  #   # check the 2 positions
  #   left = board[y][bounds[0]]
  #   right = board[y][bounds[1]]
  #   if left == "." and right == ".":
  #     break
  #   if left != ".":
  #     stack.append(box_bounds(board, bounds[0], y))
  #   if right == "[":
  #     stack.append(box_bounds(board, bounds[1], y))

  #   y += dy
  print(stack)

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
      move_box_y(board, (6, 4), -1)
      #fish = move_vertical_pt2(board, fish[1], fish[0], dy)
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