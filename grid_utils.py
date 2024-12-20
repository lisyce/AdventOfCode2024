import heapq, math
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