import sys
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
  args = sys.argv
  file_name = "input_test.txt" if "--test" in args else "input.txt"
  f = open(file_name)
  
  if "1" not in args and "2" not in args:
    print("Part One:", part_one(f))
    f.seek(0)
    print("Part Two:", part_two(f))
  else:
    part = int(args[1])
    if part == 1:
      print("Part One:", part_one(f))
    else:
      print("Part Two:", part_two(f))
    
  f.close()