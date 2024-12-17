import argparse, time, math, sys
from collections import defaultdict

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
    if i != 2:
      neighbors.append([(cy + dy, cx + dx), turns[i]])
    temp = dy
    dy = dx
    dx = -temp
  return neighbors

def pathfind(board, curr, target, d, visited, memo, curr_score): 
  if (curr, d) in memo:
    if curr_score >= memo[(curr, d)]:
      return math.inf
  memo[(curr, d)] = curr_score
  
  if curr == target:
    return curr_score

  print(len(visited))
  neighbors = get_neighbors_and_turns(curr, d)
  potential_paths = []
  #print(curr, d, neighbors)
  for n, turns in neighbors:
    if n not in visited and in_bounds(n, board) and board[n[0]][n[1]] != "#":
      visited.add(n)
      dy = n[0] - curr[0]
      dx = n[1] - curr[1]
      potential_paths.append(pathfind(board, n, target, (dy, dx), visited.copy(), memo, curr_score + 1 + 1000 * turns))
  result = min(potential_paths) if potential_paths else math.inf
  return result

# def expand_graph(board, s, e):
#   result = defaultdict(dict)
  
#   # do rotations
#   for i in range(len(board) * len(board[0])):
#     for j in range(4):
#       ccw = i * 4 + ((j + 1) % 4)
#       result[i * 4 + j][ccw] = 1000

#       cw = i * 4 + ((4 + j - 1) % 4)
#       result[i * 4 + j][cw] = 1000

#   for i in range(len(board)):
#     for j in range(len(board[0])):
#       # rotations
        

#   return result

def part_one(f) -> int:  # 115488 too high
  sys.setrecursionlimit(5000)
  board, s, e = parse_board(f)

  d = (0, 1)  # row, col
  #print(s, e)
  visited = set()
  visited.add(s)
  memo = {}
  result = pathfind(board, s, e, d, visited, memo, 0)
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