import sys, argparse, time
from collections import deque
from tqdm import tqdm

def part_one(f) -> int:
  board = []
  for line in f:
    board.append(list(line.strip()))
  
  # find index of guard
  loc = start_loc(board)  # row, col
  d_row = -1
  d_col = 0
        
  while True:
    # mark
    board[loc[0]][loc[1]] = "X"
    
    # check out of bounds
    if out_of_bounds(loc, d_row, d_col, board):
      break
    
    # move
    next_tile = board[loc[0] + d_row][loc[1] + d_col]
    if next_tile == "#":
      # turn
      d_row, d_col = turn(d_row, d_col)
      continue
    else:
      loc = (loc[0] + d_row, loc[1] + d_col)
      
  total = 0
  for row in board:
    for tile in row:
      if tile == "X":
        total += 1
  return total
    
def out_of_bounds(loc, d_row, d_col, board) -> bool:
  return loc[0] + d_row < 0 or loc[0] + d_row >= len(board) or loc[1] + d_col < 0 or loc[1] + d_col >= len(board[0])

def turn(d_row, d_col):
  if d_row == -1:
    return 0, 1
  elif d_row == 1:
    return 0, -1
  elif d_col == -1:
    return -1, 0
  else:
    return 1, 0

def start_loc(board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == "^":
        return (i, j)

def part_two(f) -> int:
  board = []
  for line in f:
    board.append(list(line.strip()))
  
  total = 0
  start = start_loc(board)
  for i in tqdm(range(len(board))):
    for j in range(len(board[0])):
      if (i, j) == start:
        continue
      
      if board[i][j] == "." and will_it_loop(board, (i, j)):
        total += 1
        #print(i, j)
        
  return total

def looped_turn_locs(turn_locs) -> bool:
  if len(turn_locs) < 8:
    return False
  
  for i in range(4, len(turn_locs) // 2):
    A = turn_locs[-1*i:]
    B = turn_locs[-2*i:-1*i]
    if A == B:
      return True
  return False

def will_it_loop(board, obstacle_loc) -> bool:
  board[obstacle_loc[0]][obstacle_loc[1]] = "#"
  turn_locs = []
  
  loc = start_loc(board)
  d_row = -1
  d_col = 0
  while True:
    # check loop
    if looped_turn_locs(turn_locs):
      break  # will jump down and return True
    
    # check out of bounds
    if out_of_bounds(loc, d_row, d_col, board):
      board[obstacle_loc[0]][obstacle_loc[1]] = "."
      return False
    
    # move
    next_tile = board[loc[0] + d_row][loc[1] + d_col]
    if next_tile == "#":
      # turn
      d_row, d_col = turn(d_row, d_col)
      turn_locs.append(loc)
      continue
    else:
      loc = (loc[0] + d_row, loc[1] + d_col)
    

  board[obstacle_loc[0]][obstacle_loc[1]] = "."
  return True


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