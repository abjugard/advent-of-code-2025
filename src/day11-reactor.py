from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
from itertools import pairwise
from functools import cache
import networkx as nx

today = day(2025, 11)


def count_paths(G, path):
  @cache
  def paths_between(here, dest):
    if here == dest:
      return 1
    return sum(paths_between(n, dest) for n in G.neighbors(here))
  return mul(paths_between(n1, n2) for n1, n2 in pairwise(path))


def parse(line):
  node, rest = line.split(':', 1)
  return node, rest.split()


def main():
  G = nx.DiGraph()
  for node, neighbours in get_data(today, parse):
    for n in neighbours:
      G.add_edge(node, n)
  print(f'{today} star 1 = {count_paths(G, ('you', 'out'))}')
  print(f'{today} star 2 = {count_paths(G, ('svr', 'fft', 'dac', 'out'))}')


if __name__ == '__main__':
  timed(main)
