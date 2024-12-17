import argparse, time, math, heapq
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

def dijkstras(board, start):
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

def all_nodes_on_best_paths(board, curr, d, target, visited, curr_score, best_score, nodes_on_best_paths, dist):
  if curr == target:
    if curr_score == best_score:
      nodes_on_best_paths.update([x for x, y in visited])
    return curr_score
  
  if curr_score > dist[(curr, d)]:
    # stop trying
    return math.inf

  neighbors = dijkstras_neighbors(curr, d)
  potential_paths = []
  for (n_loc, n_dir), cost in neighbors:
    if (n_loc, n_dir) not in visited and in_bounds(n_loc, board) and board[n_loc[0]][n_loc[1]] != "#":
      visited.add((n_loc, n_dir))
      potential_paths.append(all_nodes_on_best_paths(board, n_loc, n_dir, target, visited, curr_score + cost, best_score, nodes_on_best_paths, dist))
      visited.remove((n_loc, n_dir))
  result = min(potential_paths) if potential_paths else math.inf
  return result

def part_one(f) -> int:
  board, s, e = parse_board(f)
  dist, _ = dijkstras(board, s)
  result = math.inf
  for (loc, _), v in dist.items():
    if loc == e:
      result = min(result, v)
  return result

def part_two(f) -> int:
  board, s, e = parse_board(f)
  dist, _ = dijkstras(board, s)

  best_path_cost = math.inf
  for (loc, _), v in dist.items():
    if loc == e:
      best_path_cost = min(best_path_cost, v)

  all_nodes = set()
  visited = set()
  visited.add((s, (0, 1)))
  all_nodes_on_best_paths(board, s, (0, 1), e, visited, 0, best_path_cost, all_nodes, dist)
    
  return len(all_nodes)


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