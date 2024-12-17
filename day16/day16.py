import argparse, time, math, sys

best_path_pt1 = math.inf

def parse_board(f):
  start = end = None
  board = []
  for i, line in enumerate(f):
    row = []
    for j, char in enumerate(line):
      if char == "S":
        start = (i, j)
      elif char == "E":
        end = (i, j)
      row.append(char)
    board.append(row)
  return board, start, end

def in_bounds(pair, board) -> bool:
  return pair[0] >= 0 and pair[0] < len(board) and pair[1] >= 0 and pair[1] < len(board[0])

def get_neighbors_and_turns(curr, d):
  cy, cx = curr
  dy, dx = d

  neighbors = []
  turns = [0, 1, 2, 1]
  for i in range(4):
    neighbors.append([(cy + dy, cx + dx), turns[i]])
    temp = dy
    dy = dx
    dx = -temp
  return neighbors

def pathfind(board, curr, target, d, visited, memo):
  #global best_path_pt1
  
  # if (curr, d) in memo:
  #   return memo[(curr, d)]
  
  if curr == target:
    # best_path_pt1 = min(best_path_pt1, curr_score)
    memo[(curr, d)] = 0
    return 0

  #print(len(visited))
  neighbors = get_neighbors_and_turns(curr, d)
  potential_paths = []
  #print(curr, d, neighbors)
  for n, turns in neighbors:
    if n not in visited and in_bounds(n, board) and board[n[0]][n[1]] != "#":
      visited.add(n)
      dy = n[0] - curr[0]
      dx = n[1] - curr[1]
      potential_paths.append(1 + 1000 * turns + pathfind(board, n, target, (dy, dx), visited.copy(), memo))
  result = min(potential_paths) if potential_paths else math.inf
  memo[(curr, d)] = result
  return result

def part_one(f) -> int:  # 115488 too high
  sys.setrecursionlimit(5000)
  board, s, e = parse_board(f)
  d = (0, 1)  # row, col
  #print(s, e)
  visited = set()
  visited.add(s)
  memo = {}
  # for k, v in memo.items():
  #   print(k, v)
  return result

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