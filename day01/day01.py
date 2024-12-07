import sys, argparse, time
from collections import Counter
from typing import Tuple, List

def parse_input(f) -> Tuple[List[int], List[int]]:
  lines = [l.strip() for l in f.readlines()]
  left = sorted([int(l.split()[0]) for l in lines])
  right = sorted([int(l.split()[1]) for l in lines])
  return left, right

def part_one(f) -> int:
  left, right = parse_input(f)
  
  s = 0
  for l, r in zip(left, right):
    s += abs(l - r)

  return s

def part_two(f) -> int:
  left, right = parse_input(f)
  
  right_counts = Counter(right)
  s = 0
  for l in left:
    s += right_counts[l] * l
  return s

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
    stop = (time.perf_counter() - start) * 1000 
    
    print("Part Two:", pt_2_result, "(Ran in", round(elapsed, 8), "ms)")
    
  f.close()