from santas_little_helpers import day, get_data, timed
from santas_little_submission_helper import submit_answer
from santas_little_utils import *
from collections import Counter

today = day(2025, XX)


def part1(inp):
  res = 0
  for l in inp:
    res += 1
  return None


def part2(inp):
  res = 0
  for l in inp:
    res += 1
  return None


def parse(line):
  return line


def main():
  inp = get_data(today, parse)
  star1 = part1(inp)
  print(f'{today} star 1 = {star1}')
  submit_answer(today, star1, level=1)
  # star2 = part2(inp)
  # print(f'{today} star 2 = {star2}')
  # submit_answer(today, star2, level=2)


if __name__ == '__main__':
  timed(main)
