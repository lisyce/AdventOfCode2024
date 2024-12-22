import argparse, time, re

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

def shortest_path_to_goal(goal_pos, goal_keypad, curr_pos):
  result = []
  dy = goal_pos[0] - curr_pos[0]
  dx = goal_pos[1] - curr_pos[1]

  def do_vertical(dy, result):
    char = "v" if dy > 0 else "^"
    for _ in range(abs(dy)):
      result.append(char)
  def do_horizontal(dx, result):
    char = ">" if dx > 0 else "<"
    for _ in range(abs(dx)):
      result.append(char)

  # will we hit the empty square?
  empty = goal_keypad["."]
  if curr_pos[0] == empty[0]:  # same row, do the vertical first
    do_vertical(dy, result)
    do_horizontal(dx, result)
  else:
    do_horizontal(dx, result)
    do_vertical(dy, result)

  return result
  

def shortest_path(seq, seq_keypad):
  result = []
  seq_pos = seq_keypad["A"]

  while seq:
    goal_key = seq[0]
    goal_pos = seq_keypad[goal_key]
    p = shortest_path_to_goal(goal_pos, seq_keypad, seq_pos)
    result.extend(p)
    result.append("A")
    seq_pos = goal_pos
    seq = seq[1:]
  print("".join(result))
  return "".join(result)

def recursive_shortest_path(goal_seq, keypads):
  if len(keypads) == 1:
    return shortest_path(goal_seq, keypads[0])
  
  return shortest_path(recursive_shortest_path(goal_seq, keypads[1:]), keypads[0])

def complexity(code, seq):
  numeric = re.findall(r"\d+", code)[0]
  numeric = int(numeric)
  return numeric * len(seq)

def part_one(f) -> int:  # 138560 too high
  keypads = [DIR_KEYPAD, DIR_KEYPAD, NUM_KEYPAD]
  total = 0
  for line in f:
    seq = recursive_shortest_path(line.strip(), keypads)
    total += complexity(line.strip(), seq)
    break
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