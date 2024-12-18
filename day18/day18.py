import argparse, time, heapq, math
from collections import defaultdict

def in_bounds(pair, board) -> bool:
  return pair[0] >= 0 and pair[0] < len(board) and pair[1] >= 0 and pair[1] < len(board[0])

def neighbors(pos):
  y, x = pos
  return [(y + 1, x), (y-1, x), (y, x-1), (y, x+1)]

def dijkstras(board, start):
  queue = []
  dist = defaultdict(lambda: math.inf)
  prev = defaultdict(lambda: None)
  dist[start] = 0

  heapq.heappush(queue, (0, start))
  while queue:
    _, curr = heapq.heappop(queue)

    for loc in neighbors(curr):
      if not in_bounds(loc, board) or board[loc[0]][loc[1]] == "#":
        continue

      alt = dist[curr] + 1
      if alt < dist[loc]:
        prev[loc] = curr
        dist[loc] = alt
        heapq.heappush(queue, (alt, loc))
  return dist, prev


def part_one(f) -> int:
  board = []
  for i in range(71):
    board.append(["." for _ in range(71)])
  
  bytes = []
  for line in f:
    coords = [int(n) for n in line.strip().split(",")]
    bytes.append(coords)
  
  # first kb
  for i in range(1024):
    x, y = bytes[i]
    #print(x, y)
    board[y][x] = "#"
  
  # shortest path
  dist, _ = dijkstras(board, (0, 0))
  return dist[(70, 70)]

def path_from_prev(prev):
  curr = (70, 70)
  path = [curr]
  while curr != (0, 0):
    curr = prev[curr]
    path.append(curr)
  return path
    
def path_still_exists(board, path):
  for y, x in path:
    if board[y][x] == "#":
      return False
  return True

def part_two(f) -> str:
  board = []
  for i in range(71):
    board.append(["." for _ in range(71)])
  
  bytes = []
  for line in f:
    coords = [int(n) for n in line.strip().split(",")]
    bytes.append(coords)

  # first kb (we know it's fine)
  for i in range(1024):
    x, y = bytes[i]
    board[y][x] = "#"

  # next bytes
  path = None
  for i in range(1025, len(bytes)):
    x, y = bytes[i]
    board[y][x] = "#"
    if path and path_still_exists(board, path):
      continue

    dist, prev = dijkstras(board, (0, 0))

    if dist[(70, 70)] == math.inf:
      return ",".join([str(n) for n in bytes[i]])
    path = path_from_prev(prev)

if __name__ == "__main__":  
  parser = argparse.ArgumentParser()
  parser.add_argument("parts", nargs="*")
  args = parser.parse_args()
  
  file_name = "input.txt"
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