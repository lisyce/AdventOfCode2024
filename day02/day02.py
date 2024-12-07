import sys, argparse, time

def part_one(f) -> int:
  safe_count = 0
  for line in f:
    nums = [int(n) for n in line.split()]
    if is_safe(nums):
      safe_count += 1
  return safe_count


def is_safe(nums) -> bool:
  is_inc = nums[1] - nums[0] > 0

  for i in range(len(nums) - 1):
    diff = nums[i+1] - nums[i]
    if abs(diff) < 1 or abs(diff) > 3:
      return False
    
    if (is_inc and diff < 0) or (not is_inc and diff > 0):
      return False

  return True


def part_two(f) -> int:
  safe_count = 0
  for line in f:
    nums = [int(n) for n in line.split()]
    for i in range(len(nums)):
      new_nums = nums[:i] + nums[i+1:]
      if is_safe(new_nums):
        safe_count += 1
        break
      
  return safe_count


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