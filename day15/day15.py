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

def part_two(f) -> int:
  pass

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