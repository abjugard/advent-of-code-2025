from dataclasses import dataclass
from types import SimpleNamespace

from santas_little_utils import direction_arrow_lookup

turn = {
  'N': { 'l':'W', 'r': 'E', 'u': 'S' },
  'E': { 'l':'N', 'r': 'S', 'u': 'W' },
  'W': { 'l':'S', 'r': 'N', 'u': 'E' },
  'S': { 'l':'E', 'r': 'W', 'u': 'N' },
}


class NestedNamespace(SimpleNamespace):
  def __init__(self, dictionary, **kwargs):
    super().__init__(**kwargs)
    for key, value in dictionary.items():
      self.__setattr__(key, self.__get_entry__(value))

  def __getattr__(self, key):
    return self.default

  def __get_entry__(self, value):
    if isinstance(value, dict):
      return NestedNamespace(value)
    elif isinstance(value, list):
      return [self.__get_entry__(item) for item in value]
    else:
      return value

  def to_dict(self):
    return self.__dict__


@dataclass
class Heading:
  def __init__(self, direction='N'):
    if direction in direction_arrow_lookup:
      self.direction = direction_arrow_lookup[direction]
    elif direction.upper() in turn:
      self.direction = direction.upper()
    else:
      raise ValueError('Invalid direction')

  def __eq__(self, other):
    return self.direction == other.direction
  def __hash__(self):
    return ord(self.direction)
  def __str__(self):
    return self.direction

  @property
  def char(self):
    return '^><v'['NEWS'.index(self.direction)]

  def turn_l(self): self.direction = self.__get_l__()
  def turn_r(self): self.direction = self.__get_r__()
  def u_turn(self): self.direction = self.__get_u__()

  @property
  def l(self): return Heading(self.__get_l__())
  @property
  def r(self): return Heading(self.__get_r__())
  @property
  def u(self): return Heading(self.__get_u__())

  def __get_l__(self): return turn[self.direction]['l']
  def __get_r__(self): return turn[self.direction]['r']
  def __get_u__(self): return turn[self.direction]['u']


@dataclass
class Point:
  x: int = 0
  y: int = 0


  def __add__(self, other):
    if isinstance(other, tuple):
      ox, oy, *_ = other
      return Point(self.x + ox, self.y + oy)
    if isinstance(other, Heading):
      return self.next(other)
    return Point(self.x + other.x, self.y + other.y)
  def __sub__(self, other):
    if isinstance(other, tuple):
      ox, oy, *_ = other
      return Point(self.x - ox, self.y - oy)
    return Point(self.x - other.x, self.y - other.y)
  def __eq__(self, other):
    if isinstance(other, tuple):
      ox, oy, *_ = other
      return self.x == ox and self.y == oy
    return self.x == other.x and self.y == other.y
  def __lt__(self, other):
    if self.y < other.y:
      return True
    if self.y > other.y:
      return False
    return self.x < other.x
  def __hash__(self):
    return 2971215073 * self.x + 433494437 * self.y
  def __iter__(self):
    yield self.x
    yield self.y
  def __str__(self):
    return f'({self.x}, {self.y})'


  @property
  def n  (self): return Point(self.x,   self.y-1)
  @property
  def ne (self): return Point(self.x+1, self.y-1)
  @property
  def e  (self): return Point(self.x+1, self.y)
  @property
  def se (self): return Point(self.x+1, self.y+1)
  @property
  def s  (self): return Point(self.x,   self.y+1)
  @property
  def sw (self): return Point(self.x-1, self.y+1)
  @property
  def w  (self): return Point(self.x-1, self.y)
  @property
  def nw (self): return Point(self.x-1, self.y-1)

  north = n
  northeast = ne
  east = e
  southeast = se
  south = s
  southwest = sw
  west = w
  northwest = nw

  def next(self, d):
    if isinstance(d, Heading):
      return self.next(d.direction)
    match d:
      case 'N': return self.n
      case 'E': return self.e
      case 'W': return self.w
      case 'S': return self.s


  @property
  def t(self):
    return self.x, self.y
  @property
  def copy(self):
    return Point(self.x, self.y)


  @property
  def direct_neighbours(self):
    return {self.n, self.e, self.s, self.w}
  @property
  def neighbours(self):
    return [self.nw, self.n, self.ne,
            self.w,          self.e,
            self.sw, self.s, self.se]


  def move(self, other, multiplier=1, wrap=None):
    if wrap is not None:
      xw, yw = wrap
      self.x = (self.x + other.x * multiplier) % xw
      self.y = (self.y + other.y * multiplier) % yw
    else:
      self.x += other.x * multiplier
      self.y += other.y * multiplier
    return self


  def offset_from(self, other):
    return self.x-other.x, self.y-other.y


  def distance_to(self, other):
    return abs(self.x-other.x), abs(self.y-other.y)


  def manhattan_distance_to(self, other):
    return abs(self.x-other.x) + abs(self.y-other.y)


  def is_neighbour(self, other):
    dx, dy = self.distance_to(other)
    return dx <= 1 and dy <= 1


Origo = Point()
