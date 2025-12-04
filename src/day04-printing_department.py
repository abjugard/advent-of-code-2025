from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours

today = day(2025, 4)


def assess_warehouse(rolls):
  return sum(len(list(neighbours(p, rolls, diagonals=True))) < 4 for p in rolls)


def optimise_warehouse(rolls):
  accessible = 0
  while True:
    n_rolls = rolls.copy()
    for p in n_rolls:
      if len(list(neighbours(p, rolls, diagonals=True))) < 4:
        accessible += 1
        rolls.remove(p)
    if rolls == n_rolls:
      return accessible


def main():
  rolls, _ = build_dict_map(get_data(today), criteria='@')
  rolls = set(rolls.keys())
  print(f'{today} star 1 = {assess_warehouse(rolls)}')
  print(f'{today} star 2 = {optimise_warehouse(rolls)}')


if __name__ == '__main__':
  timed(main)
