import sys, re, argparse, time

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