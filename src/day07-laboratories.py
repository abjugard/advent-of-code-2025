from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map
from collections import defaultdict

today = day(2025, 7)


def split_quantum_tachyons(the_map, h):
  beams = defaultdict(int)
  for p, v in list(the_map.items()):
    if v == 'S':
      beams[p[0]] += 1
      del the_map[p]
      break
  splitters_hit = 0
  for y in range(2, h, 2):
    new_beams = defaultdict(int)
    for idx, c in beams.items():
      if (idx, y) in the_map:
        splitters_hit += 1
        new_beams[(idx-1)] += c
        new_beams[(idx+1)] += c
      else:
        new_beams[idx] += c
    beams = new_beams
  return splitters_hit, sum(beams.values())


def main():
  the_map, (_, h) = build_dict_map(get_data(today), criteria='S^')
  star1, star2 = split_quantum_tachyons(the_map, h)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
