import argparse, time, heapq, math
from collections import defaultdict
from tqdm import tqdm

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

def possible_cheats_pt1(board):
  cheats = []  # ((curr_y, curr_x), (dy, dx))
  for i in range(1, len(board) - 1):
    for j in range(1, len(board[0]) - 1):
      if board[i][j] == "#":
        continue

      # up
      if i > 2 and board[i-1][j] == "#" and board[i-2][j] != "#":
        cheats.append(((i, j), (-1, 0)))
      # down
      if i < len(board) - 3 and board[i+1][j] == "#" and board[i+2][j] != "#":
        cheats.append(((i, j), (1, 0)))
      # left
      if j > 2 and board[i][j-1] == "#" and board[i][j-2] != "#":
        cheats.append(((i, j), (0, -1)))
      # right
      if j < len(board[0]) - 3 and board[i][j+1] == "#" and board[i][j+2] != "#":
        cheats.append(((i, j), (0, 1)))
  return cheats


def neighbors(board, pos, cheat = None):
  y, x = pos
  result = [(y + 1, x), (y-1, x), (y, x-1), (y, x+1)]
  result = [r for r in result if in_bounds(r, board) and board[r[0]][r[1]] != "#"]

  if cheat:
    cheat_start, cheat_dir = cheat
    if pos == cheat_start:
      dy, dx = cheat_dir
      result.append((y + dy, x + dx))
  return result


def dijkstras(board, start, cheat = None):
  queue = []
  dist = defaultdict(lambda: math.inf)
  prev = defaultdict(lambda: None)
  dist[start] = 0

  heapq.heappush(queue, (0, start))
  while queue:
    _, curr = heapq.heappop(queue)

    for loc in neighbors(board, curr, cheat):
      alt = dist[curr] + 1
      if alt < dist[loc]:
        prev[loc] = curr
        dist[loc] = alt
        heapq.heappush(queue, (alt, loc))
  return dist, prev

def part_one(f) -> int:
  board, s, e = parse_board(f)
  # get the shortest path
  dist, _ = dijkstras(board, s)
  shortest = dist[e]

  total = 0
  for cheat in tqdm(possible_cheats_pt1(board)):
    dist, _ = dijkstras(board, s, cheat)
    diff = shortest - dist[e]
    if diff >= 100:
      total += 1
  return total

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