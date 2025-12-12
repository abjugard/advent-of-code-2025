from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints

today = day(2025, 12)


def area(presents, present_counts):
  return sum(count*presents[shape] for shape, count in enumerate(present_counts))


def calc_area(shape):
  _, *lines = shape
  return sum(l.count('#') for l in lines)


def parse_region(region):
  dimensions, present_counts = region.split(': ', 1)
  return tuple(ints(dimensions, split='x')), ints(present_counts, split=' ')


def main():
  *presents, regions = list(get_data(today, groups=True))
  presents = {idx: calc_area(shape) for idx, shape in enumerate(presents)}
  regions = [parse_region(region) for region in regions]
  print(f'{today} star 1 = {sum(area(presents, pc) <= x*y for (x, y), pc in regions)}')


if __name__ == '__main__':
  timed(main)
