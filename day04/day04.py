import sys, re, argparse, time


def part_one(f) -> int:
  total = 0
  board = []

  # horizontal
  for line in f:
    total += len(re.findall("XMAS", line) + re.findall("SAMX", line))
    board.append(list(line.strip()))

  # vertical
  for i in range(len(board[0])):
    # get col
    col = ""
    for j in range(len(board)):
      col += board[j][i]
    total += len(re.findall("XMAS", col) + re.findall("SAMX", col))
    
  # diag pt 1
  for i in range(0, len(board[0])):
    diag = ""
    y = 0
    for j in range(i, -1, -1):
      diag += board[y][j]
      y += 1
    total += len(re.findall("XMAS", diag) + re.findall("SAMX", diag))
    
  for i in range(1, len(board)):
    diag = ""
    x = len(board[0]) - 1
    for j in range(i, len(board)):
      diag += board[j][x]
      x -= 1
    total += len(re.findall("XMAS", diag) + re.findall("SAMX", diag))
    
  for i in range(len(board[0]) - 1, -1, -1):
    diag = ""
    y = 0
    for j in range(i, len(board[0])):
      diag += board[y][j]
      y += 1
    total += len(re.findall("XMAS", diag) + re.findall("SAMX", diag))
    
  for i in range(1, len(board)):
    diag = ""
    x = 0
    for j in range(i, len(board)):
      diag += board[j][x]
      x += 1
    total += len(re.findall("XMAS", diag) + re.findall("SAMX", diag))
    
  return total


def part_two(f) -> int:
  board = []
  total = 0
  for line in f:
    board.append(list(line.strip()))

  for i in range(1, len(board) - 1):
    for j in range(1, len(board[0]) - 1):
      A = board[i][j] == "A"
      B = board[i-1][j-1] in "MS" and board[i+1][j+1] in "MS" and board[i-1][j-1] != board[i+1][j+1]
      C = board[i-1][j+1] in "MS" and board[i+1][j-1] in "MS" and board[i-1][j+1] != board[i+1][j-1]
      if A and B and C:
        total += 1
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