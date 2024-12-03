import sys, re

def part_one(f) -> int:
  total = 0

  for line in f:
    muls = re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)
    for m in muls:
      nums = [int(n) for n in re.findall(r'\d+', m)]
      total += nums[0] * nums[1]
  return total

def part_two(f) -> int:
  total = 0
  on = True
  for line in f:
    instrs = re.findall(r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)', line)
    for i in instrs:
      if i == "don't()":
        on = False
      elif i == "do()":
        on = True
      elif on:
        nums = [int(n) for n in re.findall(r'\d+', i)]
        total += nums[0] * nums[1]
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