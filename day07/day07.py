import sys, argparse, time, re

def eqn_from_line(line):
  nums = re.findall(r'\d+', line)
  nums = [int(n) for n in nums]
  return nums[0], nums[1:]


def can_be_solved_pt_1(test_val, curr_val, nums) -> bool:
  if len(nums) == 1:
    return curr_val + nums[0] == test_val or curr_val * nums[0] == test_val
    
  if curr_val > test_val:
    return False
  
  return can_be_solved_pt_1(test_val, curr_val + nums[0], nums[1:]) or \
    can_be_solved_pt_1(test_val, curr_val * nums[0], nums[1:])


def can_be_solved_pt_2(test_val, curr_val, nums) -> bool:
  concatenated = int(str(curr_val) + str(nums[0]))
  if len(nums) == 1:
    return curr_val + nums[0] == test_val or curr_val * nums[0] == test_val or concatenated == test_val
    
  if curr_val > test_val:
    return False
  
  return can_be_solved_pt_2(test_val, curr_val + nums[0], nums[1:]) or \
    can_be_solved_pt_2(test_val, curr_val * nums[0], nums[1:]) or \
    can_be_solved_pt_2(test_val, concatenated, nums[1:])


def part_one(f) -> int:
  total = 0
  for line in f:
    test_val, nums = eqn_from_line(line)
    if can_be_solved_pt_1(test_val, nums[0], nums[1:]):
      total += test_val
    
  return total
    

def part_two(f) -> int:
  total = 0
  for line in f:
    test_val, nums = eqn_from_line(line)
    if can_be_solved_pt_2(test_val, nums[0], nums[1:]):
      total += test_val
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