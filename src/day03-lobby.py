from santas_little_helpers import day, get_data, timed

today = day(2025, 3)


def maximise_joltage(joltage_banks, batt_size=2):
  total_joltage = 0
  for bank in joltage_banks:
    start, joltage = 0, ''
    for cursor_idx in range(batt_size):
      end = len(bank) - (batt_size - cursor_idx)
      joltage += max(bank[start:end+1])
      start = bank.index(joltage[-1], start, end+1) + 1
    total_joltage += int(joltage)
  return total_joltage


def main():
  joltage_banks = list(get_data(today))
  print(f'{today} star 1 = {maximise_joltage(joltage_banks)}')
  print(f'{today} star 2 = {maximise_joltage(joltage_banks, 12)}')


if __name__ == '__main__':
  timed(main)
