import argparse, time, math, sys, heapq
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

# old, slow
# def get_neighbors_and_turns(curr, d):
#   cy, cx = curr
#   dy, dx = d

#   neighbors = []
#   turns = [0, 1, 2, 1]
#   for i in range(4):
#     if i != 2:
#       neighbors.append([(cy + dy, cx + dx), turns[i]])
#     temp = dy
#     dy = dx
#     dx = -temp
#   return neighbors

# def pathfind(board, curr, target, d, visited, memo, curr_score): 
#   if (curr, d) in memo:
#     if curr_score >= memo[(curr, d)]:
#       return math.inf
#   memo[(curr, d)] = curr_score
  
#   if curr == target:
#     return curr_score

#   neighbors = get_neighbors_and_turns(curr, d)
#   potential_paths = []
#   #print(curr, d, neighbors)
#   for n, turns in neighbors:
#     if n not in visited and in_bounds(n, board) and board[n[0]][n[1]] != "#":
#       visited.add(n)
#       dy = n[0] - curr[0]
#       dx = n[1] - curr[1]
#       potential_paths.append(pathfind(board, n, target, (dy, dx), visited.copy(), memo, curr_score + 1 + 1000 * turns))
#   result = min(potential_paths) if potential_paths else math.inf
#   return result

def dijkstras_neighbors(curr, d):
  cy, cx = curr
  dy, dx = d

  neighbors = [(((cy + dy, cx + dx), d), 1)]
  for i in range(1, 4):
    temp = dy
    dy = dx
    dx = -temp
    if i != 2:
      neighbors.append(((curr, (dy, dx)), 1000))
  return neighbors

def dijkstras(board, start, target):
  queue = []
  dist = defaultdict(lambda: math.inf)
  prev = defaultdict(lambda: None)
  dist[(start, (0, 1))] = 0

  heapq.heappush(queue, (0, (start, (0, 1))))
  while queue:
    _, (location, direction) = heapq.heappop(queue)

    for (n_loc, n_dir), cost in dijkstras_neighbors(location, direction):
      if not in_bounds(n_loc, board) or board[n_loc[0]][n_loc[1]] == "#":
        continue

      alt = dist[(location, direction)] + cost
      if alt < dist[(n_loc, n_dir)]:
        prev[(n_loc, n_dir)] = (location, direction)
        dist[(n_loc, n_dir)] = alt
        heapq.heappush(queue, (alt, (n_loc, n_dir)))
  return dist, prev

def part_one(f) -> int:
  board, s, e = parse_board(f)
  dist, _ = dijkstras(board, s, e)
  result = math.inf
  for (loc, _), v in dist.items():
    if loc == e:
      result = min(result, v)
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