from math import sqrt
from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints, mul
import networkx as nx

today = day(2025, 8)


def distance(points, n1, n2):
  x1, y1, z1 = points[n1]
  x2, y2, z2 = points[n2]
  return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2) + pow(z1-z2, 2))


def pairs_by_distance(points):
  n = len(points)
  pairs = []
  for n1 in range(n):
    for n2 in range(n1+1, n):
      pairs.append((distance(points, n1, n2), n1, n2))
  return sorted(pairs)


def three_largest(G):
  circuits = sorted(nx.connected_components(G), key=len, reverse=True)
  return mul(len(c) for c in circuits[:3])


def connect_junctions(points):
  G = nx.Graph()
  G.add_nodes_from(range(len(points)))
  for i, (_, n1, n2) in enumerate(pairs_by_distance(points)):
    G.add_edge(n1, n2)
    if i+1 == 1000:
      yield three_largest(G)
    if i > 1000 and nx.is_connected(G):
      yield points[n1][0] * points[n2][0]


def parse(line):
  return ints(line, split=',')


def main():
  points = list(get_data(today, parse))
  star_gen = connect_junctions(points)
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
