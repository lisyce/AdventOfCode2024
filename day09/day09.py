import sys, argparse, time
from tqdm import tqdm

def checksum(map_list):
  total = 0
  for i, m in enumerate(map_list):
    if m == ".":
      continue

    total += i * m
  return total

def get_map_list(f):
  disk_map = f.readline().strip()
  map_list = []

  id = 0

  total_file_blocks = 0

  file_blocks = []
  expanded_i = 0

  for i in range(len(disk_map)):
    val = int(disk_map[i])
    if i % 2 == 0:  # file
      map_list.extend([id] * val)
      id += 1
      total_file_blocks += val
      file_blocks.append((expanded_i, val))
    else:
      map_list.extend(["."] * val)
    expanded_i += val
  return map_list, file_blocks


def part_one(f) -> int:
  map_list, file_blocks = get_map_list(f)
  total_file_space = sum([x[1] for x in file_blocks])

  p1 = 0
  p2 = len(map_list) - 1
  while True:
    while map_list[p2] == ".":
      p2 -= 1
    while map_list[p1] != "." and p1 < total_file_space:
      p1 += 1
    
    if p1 >= total_file_space:
      break
    
    map_list[p1] = map_list[p2]
    map_list[p2] = "."

  return checksum(map_list)

def find_free_block(map_list, file_block):
  p1 = 0
  p2 = 0
  while True:
    # find the start of a free block
    while p1 < len(map_list) and map_list[p1] != ".":
      p1 += 1
    if p1 >= len(map_list) or file_block[0] < p1:
      return -1
    
    # find the end of the block
    p2 = p1
    while p2 < len(map_list) and map_list[p2] == ".":
      p2 += 1
    
    block_size = p2 - p1
    if block_size >= file_block[1]:
      return p1
  
    p1 = p2


def part_two(f) -> int:
  map_list, file_blocks = get_map_list(f)
  file_blocks.reverse()
  for fb in tqdm(file_blocks):
    block_val = map_list[fb[0]]

    # find first free space of sufficient size
    fsb_i = find_free_block(map_list, fb)
    
    if fsb_i == -1:
      continue  # can't move this one

    for i in range(0, fb[1]):
      map_list[fsb_i + i] = block_val
      map_list[fb[0] + i] = "."
    
    return checksum(map_list)


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