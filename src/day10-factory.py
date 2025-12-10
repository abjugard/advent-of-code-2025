from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints
from collections import deque
from z3 import Int, Optimize

today = day(2025, 10)


def optimize_indicators(target, buttons, _):
  initial_state = (False,) * len(target)
  queue = deque([(initial_state, 0)])
  visited = {initial_state}

  while queue:
    state, presses = queue.popleft()
    if state == target:
      return presses

    for b in buttons:
      n_state = tuple([not s if idx in b else s for (idx, s) in enumerate(state)])
      if n_state not in visited:
        visited.add(n_state)
        queue.append((n_state, presses + 1))


def optimize_joltages(_, buttons, target):
  xs = [Int(f'x{i}') for i in range(len(buttons))]
  solver = Optimize()
  solver.add(x >= 0 for x in xs)
  for t_idx, value in enumerate(target):
    expr = sum(x for btn, x in zip(buttons, xs) if t_idx in btn)
    solver.add(expr == value)
  solver.minimize(sum(xs))
  solver.check()
  model = solver.model()
  return sum(model[x].as_long() for x in xs)


def parse(line):
  indicators, *buttons, joltages = line.split(' ')
  indicators = tuple([c == '#' for c in indicators[1:-1]])
  buttons = [set(ints(bs[1:-1], ',')) for bs in buttons]
  joltages = tuple(ints(joltages[1:-1], ','))
  return indicators, buttons, joltages


def main():
  manual = list(get_data(today, parse))
  print(f'{today} star 1 = {sum(optimize_indicators(*specs) for specs in manual)}')
  print(f'{today} star 2 = {sum(optimize_joltages(*specs) for specs in manual)}')


if __name__ == '__main__':
  timed(main)
