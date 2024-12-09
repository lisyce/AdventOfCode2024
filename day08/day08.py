import sys, argparse, time, math
from collections import defaultdict

def find_antennas(f):
  result = defaultdict(list)
  board = []
  for line in f:
    board.append([l for l in line.strip()])

  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == ".":
        continue
      
      result[board[i][j]].append((i, j))
  
  return result, len(board), len(board[0])

def all_antinodes(antennas):
  result = set()

  for i in range(len(antennas)):
    a1 = antennas[i]
    for j in range(i+1, len(antennas)):  # all pairs
      a2 = antennas[j]
      dy = a1[0] - a2[0]
      dx = a1[1] - a2[1]
      result.add((a1[0] + dy, a1[1] + dx))
      result.add((a2[0] - dy, a2[1] - dx))

  return result

def part_one(f) -> int:
  antinode_locs = set()
  antennas, board_height, board_width = find_antennas(f)
  for _, locs in antennas.items():
    antinode_locs.update(all_antinodes(locs))

  filtered = set()
  for a in antinode_locs:
    if a[0] >= 0 and a[0] < board_height and a[1] >= 0 and a[1] < board_width:
      filtered.add(a)

  return len(filtered)

def all_antinodes_pt2(antennas, board_width, board_height):
  result = set()

  for i in range(len(antennas)):
    a1 = antennas[i]
    for j in range(i+1, len(antennas)):  # all pairs
      a2 = antennas[j]

      dy = a1[0] - a2[0]
      dx = a1[1] - a2[1]
      div = math.gcd(abs(dx), abs(dy))
      dy /= div
      dx /= div

      y, x = a1
      result.add(a1)
      while x >= 0 and y >= 0 and x < board_width and y < board_height:
        result.add((y, x))
        y += dy
        x += dx

      y, x = a1
      while x >= 0 and y >= 0 and x < board_width and y < board_height:
        result.add((y, x))
        y -= dy
        x -= dx

  return result

def part_two(f) -> int:
  antinode_locs = set()
  antennas, board_height, board_width = find_antennas(f)

  for _, locs in antennas.items():
    antinode_locs.update(all_antinodes_pt2(locs, board_width, board_height))

  filtered = set()
  for a in antinode_locs:
    if a[0] >= 0 and a[0] < board_height and a[1] >= 0 and a[1] < board_width:
      filtered.add(a)
  return len(filtered)

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