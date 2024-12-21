import argparse, time, heapq, math
from collections import defaultdict
from tqdm import tqdm

def parse_board(f):
  start = end = None
  board = []
  for i, line in enumerate(f):
    row = []
    for j, char in enumerate(line.strip()):
      if char == "S":
        start = (i, j)
      elif char == "E":
        end = (i, j)
      row.append(char)
    board.append(row)
  return board, start, end

def in_bounds(pair, board) -> bool:
  return pair[0] >= 0 and pair[0] < len(board) and pair[1] >= 0 and pair[1] < len(board[0])

def cheat_neighbors(board, pos, max_len):
  cheats = set()

  visited = set()
  visited.add(pos)
  stack = [pos]

  while stack:
    curr = stack.pop()
    for n in neighbors(board, curr):
      if n not in visited and manhattan_dist(pos, n) <= max_len:
        if board[n[0]][n[1]] != "#":
          cheats.add((n, manhattan_dist(pos, n)))
        visited.add(n)
        stack.append(n)
  return cheats

def manhattan_dist(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

# don't need dijkstra's lol but i'm not deleting it
def neighbors(board, pos):
  y, x = pos
  result = [(y + 1, x), (y-1, x), (y, x-1), (y, x+1)]
  result = [r for r in result if in_bounds(r, board)]
  return result

def dijkstras(board, start):
  queue = []
  dist = defaultdict(lambda: math.inf)
  prev = defaultdict(lambda: None)
  dist[start] = 0

  heapq.heappush(queue, (0, start))
  while queue:
    _, curr = heapq.heappop(queue)
    for y, x in neighbors(board, curr):
      if board[y][x] == "#":
        continue
      alt = dist[curr] + 1
      if alt < dist[(y, x)]:
        prev[(y, x)] = curr
        dist[(y, x)] = alt
        heapq.heappush(queue, (alt, (y, x)))
  return dist, prev

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

def solve(f, cheat_len) -> int:
  board, s, e = parse_board(f)
  # get the path
  _, prev = dijkstras(board, s)
  path, order = trace_path(e, prev)
  
  total = 0
  for i, pos in tqdm(enumerate(path)):
    can_reach = cheat_neighbors(board, pos, cheat_len)
    for cr, cl in can_reach:
      diff = order[cr] - i - cl
      if diff >= 100:
        total += 1
  return total

def part_one(f) -> int:
  return solve(f, 2)

def part_two(f) -> int:
  return solve(f, 20)
  

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