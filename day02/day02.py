import sys

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
  args = sys.argv
  file_name = "input_test.txt" if "--test" in args else "input.txt"
  f = open(file_name)
  
  if "1" not in args and "2" not in args:
    print("Part One:", part_one(f))
    print("Part Two:", part_two(f))
  else:
    part = int(args[1])
    if part == 1:
      print("Part One:", part_one(f))
    else:
      print("Part Two:", part_two(f))
    
  f.close()