import  argparse, time, math, re
import numpy as np

def parse_input(f):
  lines = f.readlines()
  result = []
  for chunk in range(len(lines) // 4):
    machine = lines[chunk * 4:chunk * 4 + 4]
    A = re.findall(r"\d+", machine[0])
    B = re.findall(r"\d+", machine[1])
    P = re.findall(r"\d+", machine[2])
    result.append(([int(a) for a in A], [int(b) for b in B], [int(p) for p in P]))
  return result

# SLOW DP
# def solve_machine(machine):
#   A, B, prize = machine
#   memo = np.full(prize, -1.0)

#   res = OPT(prize[0], prize[1], A, B, memo)
#   if res == math.inf:
#     return 0
#   return res

# def OPT(X, Y, A, B, memo):
  if memo[X-1][Y-1] != -1:
    return memo[X-1][Y-1]

  new_XA, new_YA = X - A[0], Y-A[1]
  new_XB, new_YB = X - B[0], Y-B[1]

  if new_XB == 0 and new_YB == 0:
    return 1
  elif new_XA == 0 and new_YA == 0:
    return 3
  
  m = math.inf
  if new_XB > 0 and new_YB > 0:
    m = min(m, OPT(new_XB, new_YB, A, B, memo) + 1)
  if new_XA > 0 and new_YA > 0:
    m = min(m, OPT(new_XA, new_YA, A, B, memo) + 3)
  memo[X-1][Y-1] = m
  return m

def part_one(f) -> int:
  machines = parse_input(f)
  total = 0
  for m in machines:
    total += sys_eqns(m)
  return total

def sys_eqns(machine):
  (x_A, y_A), (x_B, y_B), (x_P, y_P) = machine
  a2 = (y_A * x_P - x_A * y_P) / (y_A * x_B - y_B * x_A)
  a1 = (y_P - y_B * a2) / y_A
  if int(a1) != a1 or int(a2) != a2:
    return 0
  return int(3 * a1 + a2)

def part_two(f) -> int:
  machines = parse_input(f)
  total = 0
  for m in machines:
    m[2][0] += 10000000000000
    m[2][1] += 10000000000000
    total += sys_eqns(m)
    
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
    elapsed = (time.perf_counter() - start) * 1000 
    
    print("Part Two:", pt_2_result, "(Ran in", round(elapsed, 8), "ms)")
    
  f.close()