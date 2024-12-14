import argparse, time, re, time

def parse_input(f):
  result = []
  for line in f:
    nums = [int(n) for n in re.findall(r"-?\d+", line)]
    result.append([(nums[0], nums[1]), (nums[2], nums[3])])
  return result

def part_one(f) -> int:
  robots = parse_input(f)
  width = 101  # todo change based on test or not
  height = 103
  
  # simulate each robot 100 steps
  final_pos = [0, 0, 0, 0]
  for pos, vel in robots:
    dx = 100 * vel[0]
    dy = 100 * vel[1]
    x = (pos[0] + dx) % width
    y = (pos[1] + dy) % height
    #print(x, y)
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
  #print(final_pos)
  return final_pos[0] * final_pos[1] * final_pos[2] * final_pos[3]


def check_end(board, bots):
  total = 0
  for row in board:
    for col in row:
      if col == "#":
        total += 1
  return total == len(bots)


def part_two(f) -> int:
  robots = parse_input(f)
  width = 101  # todo change based on test or not
  height = 103
  
  c = 1
  while True:
    #print(c)
    # move all the guys
    board = [["." for _ in range(width)] for _ in range(height)]
    for i, (pos, vel) in enumerate(robots):
      x = (pos[0] + vel[0]) % width
      y = (pos[1] + vel[1]) % height
      board[y][x] = "#"
      robots[i][0] = (x, y)
    if check_end(board, robots):
      for row in board:
        print("".join(row))
      return c
    c += 1
    
    
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