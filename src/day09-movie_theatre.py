from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints
from itertools import combinations
from shapely.geometry import Polygon, box

today = day(2025, 9)


def find_largest_rectangle(points):
  max_area = 0
  for p1, p2 in combinations(points, 2):
    xs, ys = zip(*[p1, p2])
    area = (max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)
    max_area = max(max_area, area)
  return max_area


def rectangle_area(p1, p2):
  xs, ys = zip(*[p1, p2])
  area = (max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)
  return box(min(xs), min(ys), max(xs), max(ys)), area


def largest_contained_rectangle(vertices):
  max_area = 0
  poly = Polygon(vertices)
  for p1, p2 in combinations(vertices, 2):
    rectancle, area = rectangle_area(p1, p2)
    if poly.contains(rectancle):
      max_area = max(max_area, area)
  return max_area


def parse(line):
  return ints(line, ',')


def main():
  vertices = list(get_data(today, parse))
  print(f'{today} star 1 = {find_largest_rectangle(vertices)}')
  print(f'{today} star 2 = {largest_contained_rectangle(vertices)}')


if __name__ == '__main__':
  timed(main)
