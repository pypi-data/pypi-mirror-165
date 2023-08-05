from betterdicts.codeio import CodeIO
from betterdicts import betterdict
from collections import abc, Counter

# All the code generating nonsense is silly and unjustified here, because it was
# copied out of some other project I had. It will be replaced.

def mk_dict_bin_arith(name, expr, immediate=False, elidefalse=False, with_broadcast=True):
  src = CodeIO()
  src.print(f'def {name}(self, other):')
  src.indent += 2
  res = 'self' if immediate else 'res'
  if with_broadcast:
    src.print(f'if isinstance(other, self.__class__):')
    src.indent += 2
    if not immediate:
      src.print(f'res = self.copy_with_class()')
    src.print(f'for k in other.keys():')
    src.print(f'  if r := {expr("self[k]", "other[k]")}: {res}[k] = r' if elidefalse else
              f'  {res}[k] = {expr("self[k]", "other[k]")}')
    src.indent -= 2
    src.print(f'else:')
    src.indent += 2
  if not immediate:
    src.print(f'res = self.__class__()')
  src.print(f'for k,v in self.items():')
  src.print(f'  if r := {expr("v", "other")}: {res}[k] = r' if elidefalse else
            f'  {res}[k] = {expr("v", "other")}')
  if with_broadcast:
    src.indent -= 2
  src.print(f'return {res}')
  locals, _ = src.exec()
  return locals[name]


def mk_dict_unary_arith(name, expr):
  src = CodeIO()
  src.print(f'def {name}(self, other):')
  src.print(f'  return self.__class__({{k: {expr("v")} for k,v in self.items()}})')
  locals, _ = src.exec()
  return locals[name]


def mk_dict_filter(name, expr, with_broadcast=True):
  src = CodeIO()
  src.print(f'def {name}(self, other):')
  src.indent += 2
  if with_broadcast:
    src.print(f'if isinstance(other, self.__class__):')
    src.print(f'  res = self.__class__({{k: v for k,v in self.items() if {expr("v", "other[k]")} }})')
    src.print(f'else:')
    src.indent += 2
  src.print(f'res = self.__class__({{k: v for k,v in self.items() if {expr("v", "other")} }})')
  if with_broadcast:
    src.indent -= 2
  src.print(f'return res')
  locals, _ = src.exec()
  return locals[name]


class number_dict(betterdict):
  """Acts like an `collections.Counter()` with additional arithmetic support.

  """
  __slots__ = ()

  def __init__(self, arg=None, fill=1, /, **kwargs):
    if arg is None:
      super().__init__(**kwargs)
    elif isinstance(arg, dict):
      super().__init__(arg, **kwargs)
    elif isinstance(arg, (abc.Iterable, abc.Sequence)):
      super().__init__(dict.fromkeys(arg, fill), **kwargs)
    else:
      raise TypeError(f'not sure what to do about {type(arg)}')

  @classmethod
  def singleton(cls, k, v=1):
    return cls((k,), v)

  def prune(self):
    """Prunes out all keys with false values (notably 0).

    Returns ``self``.
    """
    for k in [k for k,v in self.items() if not v]:
      del self[k]
    return self

  @classmethod
  def union(cls, it):
    ret = cls()
    for c in it:
      ret += c
    return ret

  def __getitem__(self, key):
    return self.get(key, 0)

  __lt__ = mk_dict_filter('__lt__', lambda x, y: f'{x} < {y}')
  __gt__ = mk_dict_filter('__gt__', lambda x, y: f'{x} > {y}')
  __le__ = mk_dict_filter('__le__', lambda x, y: f'{x} <= {y}')
  __ge__ = mk_dict_filter('__ge__', lambda x, y: f'{x} >= {y}')

  __abs__ = mk_dict_unary_arith('__abs__', lambda x: f'abs({x})')
  __neg__ = mk_dict_unary_arith('__neg__', lambda x: f'-{x}')
  __pos__ = mk_dict_unary_arith('__pos__', lambda x: f'+{x}')

  __add__ = mk_dict_bin_arith('__add__', lambda x, y: f'{x} + {y}')
  __sub__ = mk_dict_bin_arith('__sub__', lambda x, y: f'{x} - {y}')
  __mul__ = mk_dict_bin_arith('__mul__', lambda x, y: f'{x} * {y}')
  __mod__ = mk_dict_bin_arith('__mod__', lambda x, y: f'{x} % {y}')
  __floordiv__ = mk_dict_bin_arith('__floordiv__', lambda x, y: f'{x} // {y}')
  __truediv__ = mk_dict_bin_arith('__truediv__', lambda x, y: f'{x} / {y}')
  __pow__ = mk_dict_bin_arith('__pow__', lambda x, y: f'{x} ** {y}')

  __iadd__ = mk_dict_bin_arith('__iadd__', lambda x, y: f'{x} + {y}', immediate=True)
  __isub__ = mk_dict_bin_arith('__isub__', lambda x, y: f'{x} - {y}', immediate=True)
  __imul__ = mk_dict_bin_arith('__imul__', lambda x, y: f'{x} * {y}', immediate=True)
  __imod__ = mk_dict_bin_arith('__imod__', lambda x, y: f'{x} % {y}', immediate=True)
  __ifloordiv__ = mk_dict_bin_arith('__ifloordiv__', lambda x, y: f'{x} // {y}', immediate=True)
  __itruediv__ = mk_dict_bin_arith('__itruediv__', lambda x, y: f'{x} / {y}', immediate=True)
  __ipow__ = mk_dict_bin_arith('__ipow__', lambda x, y: f'{x} ** {y}', immediate=True)

  __radd__ = mk_dict_bin_arith('__radd__', lambda x, y: f'{y} + {x}', with_broadcast=False)
  __rsub__ = mk_dict_bin_arith('__rsub__', lambda x, y: f'{y} - {x}', with_broadcast=False)
  __rmul__ = mk_dict_bin_arith('__rmul__', lambda x, y: f'{y} * {x}', with_broadcast=False)
  __rmod__ = mk_dict_bin_arith('__rmod__', lambda x, y: f'{y} % {x}', with_broadcast=False)
  __rfloordiv__ = mk_dict_bin_arith('__rfloordiv__', lambda x, y: f'{y} // {x}', with_broadcast=False)
  __rtruediv__ = mk_dict_bin_arith('__rtruediv__', lambda x, y: f'{y} / {x}', with_broadcast=False)
  __rpow__ = mk_dict_bin_arith('__rpow__', lambda x, y: f'{y} ** {x}', with_broadcast=False)

  @classmethod
  def sum(cls, it):
    res = cls()
    for x in it:
      res += x
    return res

  @classmethod
  def prod(cls, it):
    res = cls()
    for x in it:
      res *= x
    return res


__all__ = ('number_dict', )
