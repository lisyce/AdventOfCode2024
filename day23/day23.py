import argparse, time
from collections import defaultdict, deque

def build_graph(f):
  graph = defaultdict(set)
  for line in f:
    a, b = line.strip().split("-")
    graph[a].add(b)
    graph[b].add(a)
  return graph

def sets_of_3(graph):
  result = set()
  
  for node in graph:
    for neighbor in graph[node]:
      union = graph[node] & graph[neighbor]
      for u in union:
        result.add(frozenset([node, neighbor, u]))
  return result

def part_one(f) -> int:
  graph = build_graph(f)
  sets = sets_of_3(graph)
  total = 0
  for s in sets:
    if any([si.startswith("t") for si in s]):
      total += 1
  return total
  
def bron_kerbosch(R, P, X, graph, out):
  if not P and not X:
    if len(R) == max([len(graph[k]) for k in graph]):
      out.update(R)
    return
  u = (P | X).pop()
  for v in P - graph[u]:
    bron_kerbosch(R | {v}, P & graph[v], X & graph[v], graph, out)
    P.remove(v)
    X.add(v)


def part_two(f) -> int:
  graph = build_graph(f)
  clique = set()
  bron_kerbosch(set(), set([v for v in graph]), set(), graph, clique)
  return ",".join(sorted(list(clique)))

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