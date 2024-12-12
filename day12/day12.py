import sys, argparse, time

def in_bounds(pair, board) -> bool:
  return pair[0] >= 0 and pair[0] < len(board) and pair[1] >= 0 and pair[1] < len(board[0])

def get_board(f):
  result = []
  for line in f:
    result.append([l for l in line.strip()])
  return result

def perim_value_pt1(board, i, j):
  symbol = board[i][j]
  total = 0
  if i == 0 or board[i-1][j] != symbol:
    total += 1
  if i == len(board) - 1 or board[i+1][j] != symbol:
    total += 1
  if j == 0 or board[i][j-1] != symbol:
    total += 1
  if j == len(board[0]) - 1 or board[i][j+1] != symbol:
    total += 1
  return total

def region_cost(board, i, j, perim_fn):
  symbol = board[i][j]
  
  stack = [(i, j)]
  visited = set()
  visited.add((i, j))
  area = 0
  perim = 0
  while stack:
    curr_i, curr_j = stack.pop()
    area += 1
    perim += perim_fn(board, curr_i, curr_j)
    for pair in [(curr_i - 1, curr_j), (curr_i + 1, curr_j), (curr_i, curr_j-1), (curr_i, curr_j+1)]:
      if pair not in visited and in_bounds(pair, board) and board[pair[0]][pair[1]] == symbol:
        stack.append(pair)
        visited.add(pair)
  return area, perim, visited

def in_region(board, region_symbol, i, j):
  if not in_bounds((i, j), board):
    return False
  return board[i][j] == region_symbol

def perim_value_pt2(board, i, j):
  symbol = board[i][j]
  total = 0
  if not in_region(board, symbol, i-1, j) and not in_region(board, symbol, i, j-1):
    total += 1
  if not in_region(board, symbol, i-1, j) and not in_region(board, symbol, i, j+1):
    total += 1
  if not in_region(board, symbol, i+1, j) and not in_region(board, symbol, i, j-1):
    total += 1
  if not in_region(board, symbol, i+1, j) and not in_region(board, symbol, i, j+1):
    total += 1

  if in_region(board, symbol, i-1, j) and in_region(board, symbol, i, j-1) and not in_region(board, symbol, i-1, j-1):
    total += 1
  if in_region(board, symbol, i-1, j) and in_region(board, symbol, i, j+1) and not in_region(board, symbol, i-1, j+1):
    total += 1
  if in_region(board, symbol, i+1, j) and in_region(board, symbol, i, j-1) and not in_region(board, symbol, i+1, j-1):
    total += 1
  if in_region(board, symbol, i+1, j) and in_region(board, symbol, i, j+1) and not in_region(board, symbol, i+1, j+1):
    total += 1
  return total


def part_one(f) -> int:
  board = get_board(f)
  total = 0
  visited = set()
  for i in range(len(board)):
    for j in range(len(board[0])):
      if (i, j) in visited:
        continue
      area, perim, region = region_cost(board, i, j, perim_value_pt1)
      visited.update(region)
      total += area * perim

  return total

def part_two(f) -> int:
  board = get_board(f)
  total = 0
  visited = set()
  for i in range(len(board)):
    for j in range(len(board[0])):
      if (i, j) in visited:
        continue
      area, perim, region = region_cost(board, i, j, perim_value_pt2)
      visited.update(region)
      total += area * perim

  return total

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