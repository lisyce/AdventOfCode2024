import argparse, time, re, math


NUM_KEYPAD = {
  "7": (0, 0),
  "8": (0, 1),
  "9": (0, 2),
  "4": (1, 0),
  "5": (1, 1),
  "6": (1, 2),
  "1": (2, 0),
  "2": (2, 1),
  "3": (2, 2),
  ".": (3, 0),
  "0": (3, 1),
  "A": (3, 2)
}

DIR_KEYPAD = {
  ".": (0, 0),
  "^": (0, 1),
  "A": (0, 2),
  "<": (1, 0),
  "v": (1, 1),
  ">": (1, 2)
}
  
def in_bounds(keypad, pos):
  if pos[0] < 0 or pos[1] < 0 or pos[1] > 2:
    return False
  return pos[0] < 2 if keypad == DIR_KEYPAD else pos[0] < 4

def keypad_neighbors(goal_pos, curr_pos):
  result = []
  dy = goal_pos[0] - curr_pos[0]
  dx = goal_pos[1] - curr_pos[1]

  if dy != 0:
    result.append(((curr_pos[0] + dy / abs(dy), curr_pos[1]), "^" if dy < 0 else "v"))
  if dx != 0:
    result.append(((curr_pos[0], curr_pos[1] + dx / abs(dx)), "<" if dx < 0 else ">"))
  return result


def shortest_paths_to_pos(goal_pos, goal_keypad, shortest_len, curr_pos, path, visited, out):
  if curr_pos == goal_pos:
    out.append("".join(path) + "A")
    return
  if len(path) >= shortest_len:
    return
  
  for n, path_addition in keypad_neighbors(goal_pos, curr_pos):
    if n not in visited and n != goal_keypad["."] and in_bounds(goal_keypad, n):
      visited.add(n)
      path.append(path_addition)
      shortest_paths_to_pos(goal_pos, goal_keypad, shortest_len, n, path, visited, out)
      path.pop()
      visited.remove(n)

shortest_paths_to_pos_memo = {}

def shortest_paths(seq, keypad):
  result = []
  curr_pos = keypad["A"]
  while seq:
    goal_key = seq[0]
    goal_pos = keypad[goal_key]

    dy = goal_pos[0] - curr_pos[0]
    dx = goal_pos[1] - curr_pos[1]

    key = (goal_pos, curr_pos, "N" if keypad == NUM_KEYPAD else "D")
    if key not in shortest_paths_to_pos_memo:
      paths = []
      shortest_paths_to_pos(goal_pos, keypad, abs(dy) + abs(dx), curr_pos, [], set(), paths)
      shortest_paths_to_pos_memo[key] = paths
    paths = shortest_paths_to_pos_memo[key]

    if not result:
      result = paths
    else:
      temp = []
      for r in result:
        for p in paths:
          temp.append(r + p)
      result = temp

    curr_pos = goal_pos
    seq = seq[1:]
  return list(set(result))

def recursive_shortest_path(goal_seq, keypads):
  if len(keypads) == 1:
    return shortest_paths(goal_seq, keypads[0])

  paths = recursive_shortest_path(goal_seq, keypads[1:])

  min_cost = math.inf
  min_cost_paths = []
  for p in paths:
    for sp in shortest_paths(p, keypads[0]):
      if len(sp) == min_cost:
        min_cost_paths.append(sp)
      elif len(sp) < min_cost:
        min_cost_paths = [sp]
        min_cost = len(sp)
  return min_cost_paths

def complexity(code, seq):
  numeric = re.findall(r"\d+", code)[0]
  numeric = int(numeric)
  return numeric * len(seq)

def part_one(f) -> int:  # 138560 too high
  keypads = [DIR_KEYPAD, DIR_KEYPAD, NUM_KEYPAD]

  total = 0
  for line in f:
    seq = recursive_shortest_path(line.strip(), keypads)[0]
    total += complexity(line.strip(), seq)
  return total

def part_two(f) -> int:
  keypads = [DIR_KEYPAD for _ in range(25)]
  keypads.append(NUM_KEYPAD)

  total = 0
  for line in f:
    seq = recursive_shortest_path(line.strip(), keypads)[0]
    total += complexity(line.strip(), seq)
    break
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