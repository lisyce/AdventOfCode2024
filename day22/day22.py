import argparse, time
from collections import deque, defaultdict
from tqdm import tqdm

def next_num(n):
  n = ((n * 64) ^ n) % 16777216
  n = ((n // 32) ^ n) % 16777216
  return ((n * 2048) ^ n) % 16777216

def ith_num(i, n):
  for _ in range(i):
    n = next_num(n)
  return n

def part_one(f) -> int:
  total = 0
  for line in f:
    n = int(line.strip())
    total += ith_num(2000, n)
  return total

def deque_to_tuple(d):
  temp = [di for di in d]
  return (temp[0], temp[1], temp[2], temp[3])

changes = None

def price_changes(n):
  q = deque()
  seen_keys = set()
  for _ in range(2000):
    n_ = next_num(n)
    price = n_ % 10
    diff = price - n % 10
    q.append(diff)
    
    if len(q) == 4:
      key = deque_to_tuple(q)
      if key not in seen_keys:
        changes[key] += price
        seen_keys.add(key)
      q.popleft()
    n = n_


def part_two(f) -> int:
  global changes
  changes = defaultdict(int)

  for line in tqdm(f.readlines()):
    n = int(line.strip())
    price_changes(n)
  return max([v for _, v in changes.items()])
  

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