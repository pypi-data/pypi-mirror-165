"""JavaScript-like dictionaries.

These works like regular dictionaries but expose their keys as regular attributes.

"""
from betterdicts import betterdict

__all__ = ('attr_dict', 'jsdict', 'njsdict', 'rjsdict',)


class jsdict(betterdict):
  """:class:`jsdict` is a :class:`betterdict` which functions like a JavaScript object:
  it exposes its keys as attributes.

  It still has the regular :class:`betterdict` and :class:`dict` methods and can
  be used as such.

  >>> d = jsdict()
  >>> d['hello'] = 1
  >>> d.hello
  1
  >>> d.foobar = 2
  >>> d.get('foobar')
  2
  >>> setattr(d, 'X', 3)
  >>> d['X']
  3
  >>> del d.X
  >>> 'X' in d
  False
  >>> del d['foobar']
  >>> hasattr(d, 'foobar')
  False

  Warning::

    Setting a key with the same name as any of the already existing methods will
    effectively shadow those methods.

    >>> d['items'] = lambda: "NO"
    >>> d.items()
    "NO"

  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__dict__ = self



class attr_dict(betterdict):
  """A slightly safer alternative to `jsdict`.

  Dictionary values can still be accessed and set as attributes, but this won't
  overwrite normal attributes.

  """
  __slots__ = ()
  __getattr__ = betterdict.__getitem__

  def __setattr__(self, attr, val):
    self[attr] = val



class njsdict(jsdict):
  """A :class:`jsdict` where attributes default to `None` instead of raising
  `AttributeError`.

  """
  def __getattr__(self, _key):
    return None


class rjsdict(jsdict):
  """Recursive :class:`jsdict`.

  Like :class:`jsdict` but unknown attributes default to creating a new
  `rjsdict` subobject with that key.

  >>> q = rjsdict()
  >>> q.header.title = 'test'
  >>> q.col.type.name = 'i'
  >>> q
  {'header': {'title': 'test'}, 'col': {'type': {'name': 'i'}}}

  """
  def __getattr__(self, key):
    return self.setdefault(key, rjsdict())


