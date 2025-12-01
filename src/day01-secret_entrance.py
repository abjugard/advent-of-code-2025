from santas_little_helpers import day, get_data, timed

today = day(2025, 1)


def unlock_safe(instructions):
  dial = 50
  star1 = star2 = 0
  for clicks in instructions:
    prev = dial
    loops, dial = divmod(dial + clicks, 100)
    star1 += dial == 0
    star2 += abs(loops)
    star2 -= prev == 0 and loops < 0 # started on 0 when moving left
    star2 += dial == 0 and clicks < 0 # ended on 0 after moving left
  return star1, star2


def parse(line):
  m = 1 if line[0] == 'R' else -1
  return m*int(line[1:])


def main():
  instructions = get_data(today, parse)
  star1, star2 = unlock_safe(instructions)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
