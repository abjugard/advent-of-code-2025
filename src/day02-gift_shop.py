from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints

today = day(2025, 2)


def detect_invalid_ids(ranges):
  star1 = star2 = 0
  for l, r in ranges:
    for id_num in range(l, r + 1):
      id_s = str(id_num)
      id_l = len(id_s)
      id_lh = id_l // 2

      if id_l % 2 == 0 and id_s[:id_lh] == id_s[id_lh:]:
        star1 += id_num

      for size in range(1, id_lh + 1):
        if id_l % size != 0:
          continue
        if id_s[:size] * (id_l // size) == id_s:
          star2 += id_num
          break
  return star1, star2


def main():
  inp = next(get_data(today))
  ranges = [ints(d, '-') for d in inp.split(',')]
  star1, star2 = detect_invalid_ids(ranges)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
