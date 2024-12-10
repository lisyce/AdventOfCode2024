import sys, argparse, time
from collections import deque

def parse_board(f):
  board = []
  for line in f:
    board.append([int(x) for x in line.strip()])
  return board

def in_bounds(pair, board) -> bool:
  return pair[0] >= 0 and pair[0] < len(board) and pair[1] >= 0 and pair[1] < len(board[0])

def nines_reachable(board, i, j):
  total = 0
  visited = set()  
  
  q = deque()
  q.append((i, j))
  visited.add((i, j))
  while q:
    curr_i, curr_j = q.popleft()
    curr_num = board[curr_i][curr_j]
    
    if curr_num == 9:
      total += 1
    else:
      # add neighbors
      for pair in [(curr_i-1, curr_j), (curr_i+1, curr_j), (curr_i, curr_j-1), (curr_i, curr_j+1)]:
        if pair not in visited and in_bounds(pair, board) and board[pair[0]][pair[1]] == curr_num + 1:
          q.append(pair)
          visited.add(pair)
  return total

def part_one(f) -> int:
  # for each 0, bfs to find hiking trails
  board = parse_board(f)
  total = 0
  
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == 0:
        total += nines_reachable(board, i, j)
      
  return total

def distinct_trails(board, i, j):
  if board[i][j] == 9:
    return 1
  
  total = 0
  for pair in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
    if in_bounds(pair, board) and board[pair[0]][pair[1]] == board[i][j] + 1:
      total += distinct_trails(board, pair[0], pair[1])
  return total

def part_two(f) -> int:
  board = parse_board(f)
  total = 0
  
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == 0:
        total += distinct_trails(board, i, j)
      
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