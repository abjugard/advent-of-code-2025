from collections import deque, defaultdict, namedtuple
from itertools import product, zip_longest

from santas_little_helpers import alphabet

Turn = namedtuple('Turn', ['l', 'r'])

directions_8 = [('NW', (-1, -1)), ('N', (0, -1)), ('NE', (1, -1)),
                ('W',  (-1,  0)),                 ('E',  (1,  0)),
                ('SW', (-1,  1)), ('S', (0,  1)), ('SE', (1,  1))]

directions_4 = [('N', (0, -1)), ('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1))]
directions_x = [d for d in directions_8 if d not in directions_4]

direction_arrow_lookup = {
  '^': 'N',
  '>': 'E',
  '<': 'W',
  'v': 'S',
}
turn = {
  'N': Turn('W', 'E'),
  'E': Turn('N', 'S'),
  'W': Turn('S', 'N'),
  'S': Turn('E', 'W'),
}


def get_iterator(variable):
  try:
    it = iter(variable)
    return it
  except TypeError:
    return get_iterator([variable])


def skip(count, it):
  for _ in range(count):
    next(it)
  return next(it)


def get_last(generator):
  d = deque(generator, maxlen=2)
  d.pop()
  return d.pop()


def tesseract_parse(inp, lookup=True, chars=alphabet.upper()):
  from santas_little_ocr_lib import parse_datastructure, set_to_grid, create_image
  data, boundary = parse_datastructure(inp, lookup)
  try:
    import pytesseract
    image = create_image(data, *boundary)
    return pytesseract.image_to_string(image, config=f'--psm 6 -c tessedit_char_whitelist={chars}').strip()
  except ImportError:
    for line in set_to_grid(data, *boundary):
      print(''.join('█' if c else ' ' for c in line))
    print('for cooler results, please install Pillow and pytesseract\n' \
        + '(along with a tesseract-ocr distribution)')
    return None


def debug_map(the_map, inform=None, cursor=None):
  keys = []
  values = lambda p: '#' if p in keys else '.'
  if isinstance(the_map, dict):
    keys = the_map.keys()
    values = lambda p: the_map[p] if p in the_map else '#'
  elif isinstance(the_map, list):
    keys = the_map
  elif isinstance(the_map, set):
    keys = the_map

  max_h, max_w, min_h, min_w = find_bounds(keys)

  for y in range(min_h-1, max_h+2):
    line = ''
    for x in range(min_w-1, max_w+2):
      if y == min_h-1 and inform is not None and x == inform[0]:
        line += 'v'
      else:
        nv = values((x, y))
        if inform is not None and nv == '.' and x == inform[0]:
          nv = '|'
          if y == inform[1] and cursor is not None:
            nv = str(cursor)
        if inform is not None and nv == '.' and y == inform[1]:
          nv = '-'
        line += nv
    if inform is not None and y == inform[1]:
      line += ' <'
    print(line)
  print()


def find_bounds(points):
  min_w, max_w, min_h, max_h = 1_000_000, 0, 1_000_000, 0
  for x, y in points:
    min_w = min(min_w, x)
    max_w = max(max_w, x)
    min_h = min(min_h, y)
    max_h = max(max_h, y)
  return max_h, max_w, min_h, min_w


def build_dict_map(map_data, conv_func=None, key_func=None, criteria=None, default=None):
  the_map = dict() if default is None else defaultdict(lambda: default)
  def get_value(c, p):
    return c if conv_func is None else conv_func(c, p)
  def get_key(c, p):
    return p if key_func is None else key_func(c, p)
  for y, xs in enumerate(map_data):
    for x, c in enumerate(xs):
      if criteria is None or c in criteria:
        the_map[get_key(c, (x, y))] = get_value(c, (x, y))
    else:
      w = x + 1
  else:
    h = y + 1
  return the_map, (w, h)


def map_frame(w, h):
  for x in range(w):
    yield x, -1
    yield x, w
  for y in range(h):
    yield -1, y
    yield h, y
  return


def all_points(w, h):
  return product(range(w), range(h))


def neighbours(p=(0, 0), borders=None, diagonals=False, normal=True, labels=False):
  def within_borders(pt):
    if borders is None:
      return True
    elif isinstance(borders, tuple):
      x_n, y_n = pt
      w, h = borders
      return 0 <= y_n < h and 0 <= x_n < w
    elif isinstance(borders, dict):
      return pt in borders
    elif isinstance(borders, set):
      return pt in borders
    elif isinstance(borders, list):
      x_n, y_n = pt
      h = len(borders)
      return h > 0 and 0 <= y_n < h and 0 <= x_n < len(borders[0])
    elif hasattr(borders, '__call__'):
      return borders(pt)
    raise Exception(f'unknown datastructure: {type(borders)}')
  x, y = p
  dirs = directions_4
  if diagonals:
    dirs = directions_8
  if not normal:
    dirs = directions_x
  for label, (xd, yd) in dirs:
    p_n = x + xd, y + yd
    if within_borders(p_n):
      yield (label, p_n) if labels else p_n


def mul(numbers):
  result = 1
  for n in numbers:
    if n == 0:
      return 0
    result *= n
  return result


def lines_to_grid(lines):
  grid = [list(l) for l in lines]
  return (len(grid[0]), len(grid)), grid


def transpose(l, join=False, fill=None):
  transposed = list(map(list, zip_longest(*l, fillvalue=fill)))
  if join:
    return [''.join(n) for n in transpose(l)]
  return transposed


def flatten(list_of_lists):
  return [item for l in list_of_lists for item in l]


def ints(num_strings, split=None):
  if split:
    num_strings = [s.strip() for s in num_strings.split(split)]
  return tuple(map(int, num_strings))
