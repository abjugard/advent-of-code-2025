from santas_little_helpers import day, get_data, timed

today = day(2025, 5)


def merge_overlapping(ranges):
  intervals = sorted(ranges)
  merged = []
  handled = set()

  for i, (start, end) in enumerate(intervals):
    if i in handled:
      continue
    handled.add(i)
    for j, (s2, e2) in enumerate(intervals):
      if s2 <= end + 1:
        end = max(end, e2)
        handled.add(j)
      else:
        break
    merged.append(range(start, end + 1))
  return merged


def parse(line):
  if '-' in line:
    return list(map(int, line.split('-', 1)))
  return int(line)


def main():
  ranges, ingredients = list(map(list, get_data(today, parse, groups=True)))
  ranges = merge_overlapping(ranges)
  print(f'{today} star 1 = {sum(any(i in r for r in ranges) for i in ingredients)}')
  print(f'{today} star 2 = {sum(len(r) for r in ranges)}')


if __name__ == '__main__':
  timed(main)
