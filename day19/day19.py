import argparse, time
from tqdm import tqdm
from functools import cache

towels = None

def parse_input(f):
  towels = f.readline().strip().split(", ")
  f.readline()

  patterns = [l.strip() for l in f.readlines()]
  return towels, patterns

@cache
def pattern_possible(pattern):
  if not pattern:
    return True
  
  for t in towels:
    if not pattern.startswith(t):
      continue
    
    if pattern_possible(pattern[len(t):]):
      return True
    
  return False


def part_one(f) -> int:
  global towels
  towels, patterns = parse_input(f)
  total = 0
  for p in tqdm(patterns):
    if pattern_possible(p):
      total += 1
  return total

@cache
def num_ways_make_pattern(pattern):
  if not pattern:
    return 1
  
  total = 0
  for t in towels:
    if not pattern.startswith(t):
      continue
    
    total += num_ways_make_pattern(pattern[len(t):])
    
  return total

def part_two(f) -> int:
  global towels
  towels, patterns = parse_input(f)
  total = 0
  for p in tqdm(patterns):
    total += num_ways_make_pattern(p)
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