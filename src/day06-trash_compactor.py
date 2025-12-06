from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul, ints, lines_to_grid, transpose

today = day(2025, 6)


def is_whitespace_column(grid, x):
  return all(grid[y][x] == ' ' for y in range(len(grid)))


def transpose_preserving_whitespace(lines):
  (w, h), grid = lines_to_grid(lines)
  for x in range(w):
    if is_whitespace_column(grid, x):
      for y in range(h):
        grid[y][x] = '|'
  eqns = transpose(''.join(cs).split('|') for cs in grid)
  return [(l, mul if '*' in op else sum) for *l, op in eqns]


def solve(eqns, cephalopod=False):
  grand_total = 0
  for l, operation in eqns:
    if cephalopod:
      l = transpose(l, join=True)
    grand_total += operation(ints(l))
  return grand_total


def main():
  eqns = transpose_preserving_whitespace(get_data(today))
  print(f'{today} star 1 = {solve(eqns)}')
  print(f'{today} star 2 = {solve(eqns, cephalopod=True)}')


if __name__ == '__main__':
  timed(main)
