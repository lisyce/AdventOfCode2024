import argparse, time

def lock_heights(chunk):
  heights = [0 for _ in range(5)]
  for row in range(1, len(chunk)):
    for pin in range(len(heights)):
      if chunk[row][pin] == "#":
        heights[pin] += 1
  return heights

def key_heights(chunk):
  chunk.reverse()
  return lock_heights(chunk)


def key_fits_lock(key, lock):
  for k, l in zip(key, lock):
    if k + l > 5:
      return False
  return True


def keys_and_locks(f):
  keys = []
  locks = []

  lines = f.readlines()
  for i in range(len(lines) // 8 + 1):
    chunk = lines[i * 8:i*8 + 7]
    if chunk[0][0] == "#":
      locks.append(lock_heights(chunk))
    else:
      keys.append(key_heights(chunk))
  return keys, locks

def part_one(f) -> int:
  keys, locks = keys_and_locks(f)
  
  total = 0
  for l in locks:
    for k in keys:
      if key_fits_lock(k, l):
        total += 1
  return total

def part_two(f) -> int:
  pass

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