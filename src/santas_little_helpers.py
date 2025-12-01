import json, re, importlib, sys, os
from time import time
from datetime import date
from pathlib import Path
from typing import Callable, Iterator, Any
from functools import reduce
from string import ascii_lowercase, ascii_uppercase

setup_start = time()

alphabet = ascii_lowercase
ALPHABET = ascii_uppercase
full_alphabet = alphabet + ALPHABET

base_ops = [('replace', (r'\n', ''))]

aoc_root = Path(__file__).resolve().parent.parent
aoc_data = aoc_root / 'data'

with (aoc_root / 'config.json').open('r') as config_file:
  config = json.load(config_file)


def day(year: int, theday: int) -> date:
  global setup_start
  setup_start = time()
  return date(year, 12, theday)


def build_op(op, args):
  if op == 'func':
    if isinstance(args, tuple):
      return lambda line: args[0](line, *args[1])
    else:
      return lambda line: args(line)
  elif op == 'map':
    return lambda line: list(map(args, line))
  elif op == 'replace':
    matcher = re.compile(args[0])
    return lambda line: matcher.sub(args[1], line)
  elif op == 'split':
    return lambda line: line.split(args)
  elif op == 'skip':
    return lambda line: line[args:]
  elif op == 'take':
    return lambda line: line[:args]
  elif op == 'elem':
    return lambda line: line[args]
  elif op == 'translate':
    if isinstance(args, dict):
      translations = str.maketrans(args)
    else:
      translations = str.maketrans(*args)
    return lambda line: line.translate(translations)
  elif op == 'translatemany':
    targets, replacement = args
    translations = str.maketrans(targets, replacement * len(targets))
    return lambda line: line.translate(translations)


def build_op_chain(ops):
  if isinstance(ops, Callable):
    ops = [('func', ops)]
  for op, args in ops:
    yield build_op(op, args)


def format_line(line, op_chain):
  return reduce(lambda data, op: op(data), op_chain, line)


def import_requests():
  from requests import request, codes
  return request, codes


def get_data(today: date = date.today(), ops=None, groups: bool = False) -> Iterator:
  if ops is None:
    ops = []
  if not aoc_data.exists():
    aoc_data.mkdir()

  def save_daily_input() -> None:
    request, status_codes = import_requests()
    url = f'https://adventofcode.com/{today.year}/day/{today.day}/input'
    res = request('GET', url, cookies=config)
    if res.status_code != status_codes.ok:
      print(f'Day {today.day} not available yet')
      sys.exit(0)
    with file_path.open('wb') as new_input_file:
      for chunk in res.iter_content(chunk_size=128):
        new_input_file.write(chunk)

  file_path = aoc_data / f'{today.year}-{today.day:02}.txt'
  if not file_path.exists():
    print(f'Data for day {today.day} not available, downloading!')
    save_daily_input()

  op_chain = list(build_op_chain(ops))
  with file_path.open() as input_file:
    lines = input_file.read().rstrip().split('\n\n' if groups else '\n')
  if groups:
    def format_group(group_lines):
      for group_line in group_lines.split('\n'):
        yield format_line(group_line, op_chain)
    for group in lines:
      yield format_group(group)
  else:
    for line in lines:
      yield format_line(line, op_chain)


def time_fmt(delta: float) -> (float, str):
  if delta < 1e-6:
    return 1e9, 'ns'
  elif delta < 1e-3:
    return 1e6, 'µs'
  elif delta < 1:
    return 1e3, 'ms'
  return 1, 'seconds'


def execute(func: Callable) -> tuple[Any, float]:
  start = time()
  result = func()
  return result, time() - start


def execute_multiple(func: Callable, times) -> [float]:
  setup = time() - setup_start
  _, initial = execute(func)
  if times is None:
    times = 1000 if initial < 0.005 else 100
  deltas = [initial + setup]

  disable_stdout()
  for _ in range(times - 1):
    deltas += [execute(func)[1] + setup]
  restore_stdout()

  return deltas


def timed(func: Callable, start=None) -> None:
  setup = 0
  if setup_start is not None:
    setup = time() - setup_start
  if start is not None:
    setup = time() - start
  result, delta = execute(func)
  print_result(delta + setup)
  return result


def disable_stdout() -> None:
  sys.stdout = open(os.devnull, 'w')


def restore_stdout() -> None:
  sys.stdout = sys.__stdout__


def bench(func: Callable, times=None):
  start = time()
  deltas = execute_multiple(func, times)
  total = time() - start
  times = len(deltas)
  print_result(min(deltas), 'min')
  avg = sum(deltas) / len(deltas)
  print_result(avg, 'avg')
  print_result(total, 'tot', suffix=f'(n={times})')


def average(func: Callable, times: int = 100):
  deltas = execute_multiple(func, times)
  avg = sum(deltas) / len(deltas)
  print_result(avg, 'avg')


def print_result(delta: [float], prefix: str = '', suffix: str = ''):
  multiplier, unit = time_fmt(delta)
  divider = ''
  if prefix != '':
    divider = ': '
  if suffix != '':
    suffix = ' ' + suffix
  print(f'--- {prefix}{divider}{delta*multiplier:.2f} {unit}{suffix} ---')


def run_all():
  for file in sorted(Path('.').glob('day[!X]?-*.py')):
    try:
      import_start = time()
      day_module = importlib.import_module(file.name[:-3])
    except Exception as e:
      print(f'Failed to import \'{file.name}\': {e}', file=sys.stderr)
      print()
      continue
    print(f'Running \'{file.name}\':')
    timed(day_module.main, import_start)
    print()


if __name__ == '__main__':
  timed(run_all)
