import argparse, time
from collections import defaultdict

def build_circuit(f):
  lines = f.readlines()
  split_idx = lines.index("\n")
  inputs = {l.strip().split(": ")[0]: int(l.strip().split(": ")[1]) for l in lines[:split_idx]}
  
  parents = defaultdict(set)
  graph = defaultdict(set)
  ops = {}
  for l in lines[split_idx+1:]:
    parts = l.strip().split(" ")
    a, op, b, _, out = parts

    parents[out].add(a)
    parents[out].add(b)

    graph[a].add(out)
    graph[b].add(out)
    ops[out] = op
  
  return inputs, graph, parents, ops

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
  inputs, _, parents, ops = build_circuit(f)

  i = 0
  result = 0
  while f"z{i:02}" in parents:
    zi = compute_node(f"z{i:02}", inputs, parents, ops)
    result |= zi << i

    i += 1
  return result


# def find_bad_outputs(inputs, parents, ops):
#   bad_outs = set()

#   # check that all z bits come from an XOR
#   i = 0
#   zi = f"z{i:02}"
#   while zi in parents:
#     if ops[zi] != "XOR":
#       bad_outs.add(zi)
    
#     i += 1
#     zi = f"z{i:02}"

#   return bad_outs

def check_half_adder(graph, ops):
  bad_outs = set()
  if ops["z00"] != "XOR":
    bad_outs.add("z00")
  
  carry_out = next(iter((graph["x00"] - {"z00"})))
  return bad_outs, carry_out

def check_full_adder(graph, parents, ops, zi, ci):
  bad_outs = set()
  co = ""

  i = zi[1:]
  xi = "x" + i
  yi = "y" + i

  # sum XOR output
  if ops[zi] != "XOR" or graph[zi]:
    bad_outs.add(zi)

  # find out which output of xi and yi is the XOR/AND
  xi_yi_outputs = graph[xi] & graph[yi]
  if len(xi_yi_outputs) != 2:
    raise Exception("We didn't plan for this")
  out_a, out_b = xi_yi_outputs
  xy_xor = out_a if ops[out_a] == "XOR" else out_b if ops[out_b] == "XOR" else None
  xy_and = out_a if ops[out_a] == "AND" else out_b if ops[out_b] == "AND" else None
  if xy_xor is None or xy_and is None:
    raise Exception("We didn't plan for this (2)")

  if len(graph[xy_and]) != 1:
    bad_outs.add(xy_and)
  else:
    co = next(iter(graph[xy_and]))
  
  if len(graph[xy_xor]) != 2:
    bad_outs.add(xy_xor)
  else:
    out_a, out_b = graph[xy_xor]
    xor_xor = out_a if ops[out_a] == "XOR" else out_b if ops[out_b] == "XOR" else None
    xor_and = out_a if ops[out_a] == "AND" else out_b if ops[out_b] == "AND" else None
    if xor_xor is None or xor_and is None:
      raise Exception("We didn't plan for this (3)")
    
    if not xor_xor.startswith("z"):
      bad_outs.add(xor_xor)
    
    
  return bad_outs, co


def find_bad_outputs(graph, parents, ops):
  bad_outs = set()

  # start with the half adder
  bo, co = check_half_adder(graph, ops)
  bad_outs |= bo

  # now do the full adders
  z_count = 44  # plus one carry-out to make 45
  for i in range(1, z_count + 1):  # since exclusive bound
    zi = f"z{i:02}"
    bo, co = check_full_adder(graph, parents, ops, zi, co)
    bad_outs |= bo
    
  return ",".join(sorted(bad_outs))

def part_two(f) -> int:
  _, graph, parents, ops = build_circuit(f)
  bad_outs = find_bad_outputs(graph, parents, ops)

  return bad_outs

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