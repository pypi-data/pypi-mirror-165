from functools import wraps
from betterdicts.betterdict import betterdict

class dynamic_dict(betterdict):
  """A dictionary which dynamically creates entries on lookup.

  Similar to `collections.defaultdict()` but strictly more powerful in that the
  factory function is given the key as an argument, allowing it to create
  default values based on what was requested.

  >>> d = default_dict(hex)
  >>> d[10]
  "0xa"
  >>> d
  {10: '0xa'}

  """
  __slots__ = ('_factory',)

  def __init__(self, factory, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._factory = factory

  def __missing__(self, key):
    self[key] = self._factory(key)
    return self[key]


def cache_dict(f):
  """A `dynamic_dict` which acts as a function with cache.

  WARNING: caches based on its first argument only. The other arguments are
  ignored when considering if it's a cache hit or miss.

  The point of using this over `functools.cache` is that here you have full
  access and control over the dictionary used. Indeed, the "function" is just a
  dictionary, and you can manually clear it, insert items manually, etc.

  You'd normally use this dict as a decorator:

  ```python
  @cache_dict
  def heavy_calculation(n):
    ...

  print( heavy_calculation(10) ) # invokes the function
  print( heavy_calculation(10) ) # uses cache
  heavy_calculation.clear()
  print( heavy_calculation(10) ) # invokes the function again
  ```

  Note that the cache is unlimited, and that `heavy_calculation` here can be
  treated as just a dictionary.

  Each invocation withh generate a new type. Documentation and name will be
  copied from the given function.

  """
  @wraps(f, updated=())
  class cache_dict(dynamic_dict):
    __slots__ = ('__doc__',)
    def __call__(self, *args, **kwargs):
      if args[0] in self:
        return self[args[0]]
      res = f(*args, **kwargs)
      self[args[0]] = res
      return res

  return cache_dict(f)
