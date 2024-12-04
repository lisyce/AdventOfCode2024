import sys, re


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