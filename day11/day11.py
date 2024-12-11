import sys, argparse, time, math
from collections import defaultdict

def simulate_blink(stones):
  result = defaultdict(int)
  for stone, count in stones.items():
    num_digits = 1 if stone == 0 else int(math.log10(stone))+1
    
    if stone == 0:
      result[1] += count
    elif num_digits % 2 == 0:
      half = num_digits // 2
      left = stone // (10 ** half)
      right = stone - left * (10 ** half)
      result[left] += count
      result[right] += count
    else:
      result[stone * 2024] += count
  return result

def solve(f, num_blinks):
  line = f.readline().strip().split(" ")
  stones = defaultdict(int)
  for num in line:
    stones[int(num)] += 1
  
  for i in range(num_blinks):
    stones = simulate_blink(stones)
  return sum([v for k, v in stones.items()])

def part_one(f) -> int:
  return solve(f, 25)

def part_two(f) -> int:
  return solve(f, 75)

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