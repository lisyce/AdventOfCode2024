import argparse, time
from collections import defaultdict

def build_circuit(f):
  lines = f.readlines()
  split_idx = lines.index("\n")
  inputs = {l.strip().split(": ")[0]: int(l.strip().split(": ")[1]) for l in lines[:split_idx]}
  
  parents = defaultdict(set)
  ops = {}
  for l in lines[split_idx+1:]:
    parts = l.strip().split(" ")
    a = parts[0]
    op = parts[1]
    b = parts[2]
    out = parts[4]

    parents[out].add(a)
    parents[out].add(b)
    ops[out] = op
  
  return inputs, parents, ops

graph_values = {}

def compute_node(node, inputs, parents, ops):
  if node in graph_values:
    return graph_values[node]

  if not parents[node]:
    graph_values[node] = inputs[node]
    return inputs[node]
  
  a, b = parents[node]
  a = compute_node(a, inputs, parents, ops)
  b = compute_node(b, inputs, parents, ops)

  match ops[node]:
    case "AND":
      return a and b
    case "OR":
      return a or b
    case "XOR":
      return a ^ b
    case _:
      raise Exception("Invalid operation")


def part_one(f) -> int:
  inputs, parents, ops = build_circuit(f)

  i = 0
  result = 0
  while f"z{i:02}" in parents:
    zi = compute_node(f"z{i:02}", inputs, parents, ops)
    result |= zi << i

    i += 1
  return result


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