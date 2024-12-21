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

def cheat_neighbors_pt1(board, pos):
  i, j = pos
  cheats = []

  # up
  if i > 2 and board[i-1][j] == "#" and board[i-2][j] != "#":
    cheats.append((i-2, j))
  # down
  if i < len(board) - 3 and board[i+1][j] == "#" and board[i+2][j] != "#":
    cheats.append((i+2, j))
  # left
  if j > 2 and board[i][j-1] == "#" and board[i][j-2] != "#":
    cheats.append((i, j-2))
  # right
  if j < len(board[0]) - 3 and board[i][j+1] == "#" and board[i][j+2] != "#":
    cheats.append((i, j+2))

  return cheats

# TODO don't need dijkstra's lol
def neighbors(board, pos, cheat = None):
  y, x = pos
  result = [(y + 1, x, 1), (y-1, x, 1), (y, x-1, 1), (y, x+1, 1)]
  result = [r for r in result if in_bounds((r[0], r[1]), board) and board[r[0]][r[1]] != "#"]

  if cheat:
    cheat_start, cheat_end, cost = cheat
    if pos == cheat_start:
      result.append((cheat_end[0], cheat_end[1], cost))
  return result

def dijkstras(board, start, cheat = None):
  queue = []
  dist = defaultdict(lambda: math.inf)
  prev = defaultdict(lambda: None)
  dist[start] = 0

  heapq.heappush(queue, (0, start))
  while queue:
    _, curr = heapq.heappop(queue)
    for y, x, cost in neighbors(board, curr, cheat):
      alt = dist[curr] + cost
      if alt < dist[(y, x)]:
        prev[(y, x)] = curr
        dist[(y, x)] = alt
        heapq.heappush(queue, (alt, (y, x)))
  return dist, prev

def part_one(f) -> int:
  board, s, e = parse_board(f)
  # get the path
  _, prev = dijkstras(board, s)
  path, order = trace_path(e, prev)
  
  total = 0
  for i, pos in enumerate(path):
    can_reach = cheat_neighbors_pt1(board, pos)
    for cr in can_reach:
      diff = order[cr] - i - 2
      if diff >= 100:
        total += 1
  return total

def trace_path(end, prev):
  curr = end
  path = []
  inverse = {}
  while curr:
    path.append(curr)
    curr = prev[curr]

  path.reverse()
  for i, pos in enumerate(path):
    inverse[pos] = i
  return path, inverse


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