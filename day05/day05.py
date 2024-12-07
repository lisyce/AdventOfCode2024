import sys, functools, argparse, time

def is_valid(nums_before, update) -> bool:
  update_set = set(update)
  
  for i, num in enumerate(update):
    before_rule = nums_before[num] if num in nums_before else set()
    before_actual = set(update[0:i]) if i > 0 else set()
    for br in before_rule:
      if br in update_set and br not in before_actual:
        return False
  
  return True
    

def part_one(f) -> int:
  nums_before = {}
  seen_break = False
  total = 0
  for line in f:
    if not line.strip():
      # the split
      seen_break = True
      continue
    
    if not seen_break:
      nums = [int(n) for n in line.strip().split("|")]
      if nums[1] not in nums_before:
        nums_before[nums[1]] = set()
      nums_before[nums[1]].add(nums[0])
      
    else:
      update = [int(n) for n in line.strip().split(",")]
      if is_valid(nums_before, update):
        total += update[len(update) // 2]
      
  return total
  
def comparator(a, b, nums_before):
  before_a = nums_before[a] if a in nums_before else set()
  before_b = nums_before[b] if b in nums_before else set()
  return -1 if a in before_b else 1 if b in before_a else 0
    

def reorder_update(nums_before, update):
  return sorted(update, key=functools.cmp_to_key(lambda a, b: comparator(a, b, nums_before)))
    
def part_two(f) -> int:
  nums_before = {}
  seen_break = False
  total = 0
  for line in f:
    if not line.strip():
      # the split
      seen_break = True
      continue
    
    if not seen_break:
      nums = [int(n) for n in line.strip().split("|")]
      if nums[1] not in nums_before:
        nums_before[nums[1]] = set()
      nums_before[nums[1]].add(nums[0])
      
    else:
      update = [int(n) for n in line.strip().split(",")]
      if not is_valid(nums_before, update):
        reordered = reorder_update(nums_before, update)
        total += reordered[len(reordered) // 2]
      
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
    stop = (time.perf_counter() - start) * 1000 
    
    print("Part Two:", pt_2_result, "(Ran in", round(elapsed, 8), "ms)")
    
  f.close()