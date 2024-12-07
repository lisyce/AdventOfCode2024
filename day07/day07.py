import sys, re

def eqn_from_line(line):
  nums = re.findall(r'\d+', line)
  nums = [int(n) for n in nums]
  return nums[0], nums[1:]


def can_be_solved_pt_1(test_val, curr_val, nums) -> bool:
  if len(nums) == 1:
    return curr_val + nums[0] == test_val or curr_val * nums[0] == test_val
    
  if curr_val > test_val:
    return False
  
  return can_be_solved_pt_1(test_val, curr_val + nums[0], nums[1:]) or can_be_solved_pt_1(test_val, curr_val * nums[0], nums[1:])


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