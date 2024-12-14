import argparse, time, re, time
import numpy as np
import matplotlib.pyplot as plt

def parse_input(f):
  result = []
  for line in f:
    nums = [int(n) for n in re.findall(r"-?\d+", line)]
    result.append([[nums[0], nums[1]], [nums[2], nums[3]]])
  return result

def part_one(f, width, height) -> int:
  robots = parse_input(f)
  
  # simulate each robot 100 steps
  final_pos = [0, 0, 0, 0]
  for pos, vel in robots:
    dx = 100 * vel[0]
    dy = 100 * vel[1]
    x = (pos[0] + dx) % width
    y = (pos[1] + dy) % height
    if x == width // 2 or y == height // 2:
      continue
    
    if x < width // 2:
      if y < height // 2:
        final_pos[0] += 1
      else:
        final_pos[2] += 1
    else:
      if y < height // 2:
        final_pos[1] += 1
      else:
        final_pos[3] += 1
  return final_pos[0] * final_pos[1] * final_pos[2] * final_pos[3]


def error(positions):
  avg = np.mean(positions, axis=0)
  err = np.mean(np.square(positions - avg))
  return err

def part_two(f, width, height) -> int:
  robots = np.array(parse_input(f))
  
  positions = robots[:, 0]
  velocities = robots[:, 1]
  
  min_err = np.inf
  min_iter = -1
  errs = []
  for iteration in range(10000):
    positions += velocities   
    positions[:, 0] %= width
    positions[:, 1] %= height
    
    err = error(positions)
    errs.append(err)
    if err < min_err:
      min_err = err
      min_iter = iteration + 1
  plt.title("MSE per iteration")
  plt.xlabel("Iteration")
  plt.ylabel("Error")
  plt.plot(np.arange(len(errs)) + 1, errs)
  plt.plot(min_iter, errs[min_iter-1], 'ro')
  plt.text(min_iter + len(errs) / 100, errs[min_iter-1], f"({min_iter}, {errs[min_iter-1]})")
  plt.show()
  return min_iter
    

if __name__ == "__main__":  
  parser = argparse.ArgumentParser()
  parser.add_argument("parts", nargs="*")
  parser.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
  args = parser.parse_args()
  
  file_name = "input_test.txt" if args.test else "input.txt"
  f = open(file_name)
  
  width = 11 if args.test else 101
  height = 7 if args.test else 103
  
  run_pt_1 = not args.parts or "1" in args.parts
  run_pt_2 = not args.parts or "2" in args.parts
  
  if run_pt_1:
    start = time.perf_counter()
    pt_1_result = part_one(f, width, height)
    elapsed = (time.perf_counter() - start) * 1000 
    
    print("Part One:", pt_1_result, "(Ran in", round(elapsed, 8), "ms)")
  
  f.seek(0)
  
  if run_pt_2:
    start = time.perf_counter()
    pt_2_result = part_two(f, width, height)
    elapsed = (time.perf_counter() - start) * 1000 
    
    print("Part Two:", pt_2_result, "(Ran in", round(elapsed, 8), "ms)")
    
  f.close()