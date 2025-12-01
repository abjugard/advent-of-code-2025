from santas_little_helpers import day, get_data, timed
from santas_little_submission_helper import submit_answer
from santas_little_utils import *
from collections import Counter

today = day(2025, 1)


def part1(inp):
  dial = 50
  count = 0
  for d, s in inp:
    dial += s if d == 'R' else -s
    count += (dial % 100) == 0
  return count


def part2(inp):
  dial = 50
  count = 0
  for d, s in inp:
    m = 1 if d == 'R' else -1
    for _ in range(s):
      dial += m
      count += (dial % 100) == 0
  return count


def parse(line):
  return line[0], int(line[1:])


def main():
  inp = list(get_data(today, parse))
  star1 = part1(inp)
  print(f'{today} star 1 = {star1}')
  star2 = part2(inp)
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
