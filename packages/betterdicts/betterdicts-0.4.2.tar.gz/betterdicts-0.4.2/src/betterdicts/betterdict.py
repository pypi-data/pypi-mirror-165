"""The `betterdict` utility class.

It inherits from `dict` but adds various convenience method for inversion,
filtering, mapping, and collating.

"""

import collections.abc

class hybridmethod(classmethod):
  """Similar to ``classmethod`` but also allows the function to works as a method.

  Use something like ``isinstance(self_or_cls, type)`` to test for it in the
  function.

  """
  def __get__(self, instance, typ):
    if instance is None:
      return super().__get__(instance, typ)
    return self.__func__.__get__(instance, typ)

__all__ = ('betterdict',)

_MISSING = object()


class betterdict(dict):
  """A ``dict`` with a few extra utility methods and improvements.

  Extra functionality:

  - Several ways to deal with key-value iterators where keys may occur several
    times. See ``cls.collect()`` (for creating a dict of (mutable) collections)
    and ``cls.collate()`` (the functional alternative).

  - Generalized filtering of keys, values, or pairs: ``filter(keys=...,
    values=..., pairs=...)``

  - Generalized transformation of keys, values, or pairs: ``map(keys=...,
    value=..., pairs=...)``

  - Both the above also provide more verbose alternatives ``filter_values()``,
    ``map_keys()``, etc.

  - Map inversion, giving a dict of values to keys: ``invert()``. There's also
    methods ``invert_and_collate()`` and ``invert_and_collect()`` for handling
    non-injective mappings.

  Improvements:

  - ``.update()`` and ``.clear()`` returns ``self`` so these operations can be
    chained in a functional manner.

  - ``.insert()`` as a functional alternative to the assignment statement.


  Other notes:

  - ``.copy_with_class()`` tries to create an instance of the same type as the
    instance instead of returning a plain ``dict`` like ``dict.copy()``.

  """

  __slots__ = ()

  def invert(self):
    """Inverts the dictionary, returning a mapping from values to keys.

    Note that duplicate values will be discarded if the mapping is not
    one-to-one. Use ``invert_and_collect()`` or ``invert_and_combine()`` to
    handle these cases.

    >>> betterdict(a=2).invert()
    {2: 'a'}
    >>> betterdict(a=2,b=2,c=3).invert()
    {2: 'b', 3: 'c'}
    >>> betterdict(a=2,b=2,c=3).invert_and_collect(list)
    {2: ['a', 'b'], 3: ['c']}
    >>> betterdict(a=2,b=2,c=3).invert_and_collate(lambda x, y: x + y)
    {2: 'ab', 3: 'c'}

    """
    return self.__class__({v: k for k,v in self.items()})

  def invert_and_collect(self, coll_factory=set, add_action=None):
    """Invert and collect keys mapping to the same values into collections.

    Functionally like ``cls.collect(type, obj.iter_inverted(), [add_action=...])``.

    >>> d = betterdict({0: 'even', 1: 'odd', 2: 'even'})
    >>> d.invert_and_collect(list)
    {'even': [0, 2], 'odd': [1]}

    The type defaults to ``set``.

    """
    return self.__class__.collect(coll_factory, self.iter_inverted(), add_action=add_action)

  def invert_and_combine(self, func, initial=_MISSING):
    """Invert and combine keys mapping to the same values.

    Functionally like ``cls.collect(func, obj.iter_inverted(), [initial=...])``.

    """
    return self.__class__.combine(func, self.iter_inverted(), initial=initial)

  @hybridmethod
  def collect(self_or_cls, coll_factory, it=None, add_action=None):
    """Collects key-value pairs into a dictionary of collections. Values with
    equal keys go into the same collection.

    Normally ``dict`` discards (overwrites) values when identical keys are
    encountered in creation or update. This method (and ``.combine()``) are
    provided as alternative behaviors when you want to collect or combine the
    values instead.

    >>> betterdict.collect( list, [('l', 10), ('l', 0), ('r', -2), ('l', 7), ('r', 4)] )
    {'l': [10, 0, 7], 'r': [-2, 4]}

    This can be used in the following ways with slightly different semantics:

    - as a class method: ``betterdict.collect(type, iterator, [add_action=None])``
    - as an update instance method: ``obj.collect([type], iterator, [add_action=None])``

    Unlike with ``.combine()`` it makes no sense for the update-like method to
    return a new dictionary (the collections are usually mutably updated), so it
    will just return ``obj``.

    Specifying the collection type is optional in the second case. If ``obj`` is
    non-empty it will be auto-detected. If ``obj`` is empty it will default to
    ``list``.

    >>> q = betterdict(a={2})
    >>> q.collect( zip('abc', range(3)) )
    {'a': {0, 2}, 'b': {1}, 'c': {2}}

    The method with which values are added to the collections is auto-detected
    (``coll_factory`` is checked for attributes "append", "add", "push", and
    "insert", in that order). This can be specified for custom containers or
    behaviors:

    >>> betterdict.collect(list, zip('llrrrluuuu', range(10)), lambda coll, val: coll.insert(0, val))
    {'l': [5, 1, 0], 'r': [4, 3, 2], 'u': [9, 8, 7, 6]}

    It is invoked with ``add_action(collection_object, value)``. Its return
    value is ignored.

    This is explicitly intended to be used with mutable collection objects. If a
    more functional or immutable reduction is desired (such as summing numbers,
    concatenating strings, etc.), use ``.combine()`` instead.

    If the given iterator is a dictionary, it will be iterated over with ``dict.items()``.

    >>> q = betterdict.collect(list, zip('syzygy', range(6)))
    >>> q
    {'s': [0], 'y': [1, 3, 5], 'z': [2], 'g': [4]}
    >>> q.collect( dict(w=-1, z=10) )
    {'s': [0], 'y': [1, 3, 5], 'z': [2, 10], 'g': [4], 'w': [-1]}

    """
    if isinstance(self_or_cls, type):
      # Used as a class method.
      obj = self_or_cls()
    else:
      # Update method.
      obj = self_or_cls
      if not isinstance(coll_factory, type):
        assert add_action is None
        add_action = it
        it = coll_factory
        try:
          coll_factory = type(next(iter(obj.values())))
        except StopIteration:
          coll_facory = list
      if isinstance(it, dict):
        it = it.items()

    if not isinstance(it, collections.abc.Iterable):
      raise ValueError('source needs to be iterable')

    if add_action is None:
      for attr in ('append', 'add', 'push', 'insert'):
        if hasattr(coll_factory, attr):
          add_action = getattr(coll_factory, attr)
          break
      else:
        raise ValueError("no suitable way to add to the collection found")

    for k, v in it:
      if k in obj:
        add_action(obj[k], v)
      else:
        obj[k] = c = coll_factory()
        add_action(c, v)

    return obj

  def disperse(self):
    """Assuming values in the dictionary are iterable, yields all ``(k,v)``
    pairs such that ``k in self`` and ``v in self[k]``.

    Can be thought of as the inverse of ``betterdict.collect()``.

    """
    return ((k, subv) for k, v in self.items() for subv in v)

  @hybridmethod
  def combine(self_or_cls, func, it=None, *, initial=_MISSING):
    """Combines key-value pairs into a dictionary by combining (folding) values
    of identical keys.

    Normally ``dict`` discards (overwrites) values when identical keys are
    encountered in creation or update. This method (and ``.collect()``) are
    provided as alternative behaviors when you want to collect or combine the
    values instead.

    >>> betterdict.combine( max, [('l', 10), ('l', 0), ('r', -2), ('l', 7), ('r', 4)] )
    {'l': 10, 'r': 4}

    Useful when you have a stream providing keyed data that is naturally
    monoidal, like numbers, vectors, etc. If you want to keep all the values and
    collect them into subcontainers, consider ``.collect()`` instead.

    Always returns a fresh dictionary.

    This can be used in the following ways:

    * As a class method: ``betterdict.combine(op, iterator, [initial=value])``

    As seen above. Repeatedly combines values with equal keys in the given. A
    new dictionary is returned.

    * As a (functional) update instance method: ``obj.combine(op, iterator, [initial=value])``

    This works like the first case but doesn't start from an empty dictionary.
    (Unlike ``.update()`` it does not modify ``obj``.)

    It can be thought of as a shorthand for ``betterdict.combine(func,
    itertools.chain(obj.items(), it), ...)``, i.e. prepending the iterator with
    the key-value pairs in ``obj``.

    >>> betterdict(a=10).combine(ops.add, [('a', 2)])
    {'a': 12}

    * As a reduction operation: ``obj.combine(op, [initial=value])``

    This treats ``obj`` as a dictionary of iterables, performing a reduction
    over those iterables. (Again, unlike ``.update()`` it does not modify
    ``obj``.)

    >>> W = betterdict(a=[1,4,5], b=[2,3])
    >>> W.combine(ops.add)
    {'a': 10, 'b': 5}
    >>> W
    {'a': [1, 4, 5], 'b': [2, 3]}

    Often equivalent to something like ``ops.map_values(...)``.

    The ``initial`` argument has semantics similar to that in the built-in
    ``reduce()``. The first time a new key is encountered, instead of using
    the value as is, ``func(initial, value)`` will be used instead.

    >>> V = betterdict.combine( ops.add, [(0,'z'), (1,'o'), (0,'t'), (0,'f')] )
    >>> V
    {0: 'ztf', 1: 'o'}
    >>> V.combine( ops.add, [(2,'x'), (1,'y'), (0,'z')] )
    {0: 'ztfz', 1: 'oy', 2: 'x'}
    >>> betterdict.combine(ops.add, zip('vcvvcvcvcv', 'oneirology'))
    {'v': 'oeiooy', 'c': 'nrlg'}

    This function could also be called "fold" (it is specifically a left fold),
    "reduce", or even "concatenate" (the monoidal operator is sometimes called
    this). It's all the same.

    """

    if isinstance(self_or_cls, type):
      # Used as a class method.
      if it is None:
        raise ValueError("an iterator must be provided when used as a class method")
      obj = self_or_cls()
    elif it is None:
      # Reduction operation.
      assert callable(func)
      obj = self_or_cls.__class__()
      it = self_or_cls.disperse()
    else:
      # Update method.
      obj = self_or_cls.copy()
      if isinstance(it, dict):
        it = it.items()

    for k, v in it:
      if k in obj:
        obj[k] = func(obj[k], v)
      elif initial is _MISSING:
        obj[k] = v
      else:
        obj[k] = func(initial, v)

    return obj

  def filter(self, keys=None, values=None, pairs=None):
    """Filter keys or values, returning a new dictionary.

    This method covers many use cases depending on how it's used:

    - filter()

      Filters (k,v) pairs where ``bool(v)`` is true.

    - filter(keys=f) or filter(f)

      Filters (k,v) pairs where ``f(k)`` is true.

    - filter(values=f) or filter(None, f)

      Filters (k,v) pairs where f(v) is true.

    - filter(f,g) or filter(keys=f, values=g)

      Filters (k,v) pairs where f(k) and g(v) are both true.

    - filter(pairs=f)

      Filters (k,v) pairs where f(k,v) is true.

    """
    if pairs is None:
      if keys is not None:
        if values is not None:
          pairs = lambda k, v: keys(k) and values(v)
        else:
          pairs = lambda k, _: keys(k)
      elif values is not None:
        pairs = lambda _, v: values(v)
      else:
        pairs = lambda _, v: bool(v)
    elif keys is not None or values is not None:
      raise ValueError("pairs=... cannot be combined with other filters")

    return self.__class__({
      k: v for k, v in self.items()
      if pairs(k, v)
    })

  def filter_keys(self, pred=None):
    """Equivalent to ``.filter(keys=...)``.

    The only exception is that if no argument is given it is equivalent to
    ``.filter(keys=bool)``.

    """
    return self.filter(keys=bool if pred is None else pred)

  def filter_values(self, pred=None):
    """Equivalent to ``.filter(values=...)``.

    """
    return self.filter(values=pred)

  def filter_pairs(self, pred=None):
    """Equivalent to ``.filter(pairs=...)``.

    """
    return self.filter(pairs=pred)

  def map(self, keys=None, values=None, pairs=None):
    """Map keys or values, returning a new dictionary.

    """
    if pairs is None:
      if keys is not None:
        pairs = lambda k, v: (keys(k), v)
      elif values is not None:
        pairs = lambda k, v: (k, values(v))
      else:
        raise ValueError("at least one of the arguments must be provided")
    elif keys is not None or values is not None:
      raise ValueError("pairs=... cannot be combined with other arguments")

    return self.__class__(pairs(k, v) for k, v in self.items())

  def map_keys(self, func, combine_func=None, initial=_MISSING):
    """Equivalent to ``.map(keys=func)`` but with the option to collate."""
    if combine_func is not None:
      return self.__class__.combine(combine_func, ((func(k), v) for k, v in self.items()), initial=initial)
    return self.map(keys=func)

  def map_values(self, func):
    """Equivalent to ``.map(values=func)``."""
    return self.map(values=func)

  def map_pairs(self, func, combine_func=None, initial=_MISSING):
    """Equivalent to ``.map(pairs=func)`` but with the option to collate."""
    if combine_func is not None:
      return self.__class__.combine(combine_func, (func(k, v) for k, v in self.items()), initial=initial)
    return self.map(pairs=func)

  def copy(self):
    """Creates a shallow copy of the dictionary (preserving type).

    """
    return self.__class__(self)

  def iter_inverted(self):
    return ((v, k) for k, v in self.items())

  def update(self, *args, **kwargs):
    "Like ``dict.update()`` but returns ``self``."
    dict.update(self, *args, **kwargs)
    return self

  def clear(self):
    "Like ``dict.clear()`` but returns ``self``."
    dict.clear(self)
    return self

  def cache_get(self, key, factory):
    """Gets the value associated with the given key.

    If the key is missing, a new value is produced by calling ``factory(key)``.
    This is inserted into the dictionary and then returned.

    Useful for implementing various cache behaviors, thus the name.

    Can be thought of as a lazy version of ``.setdefault()``, for when creating
    the new entry is expensive. See also ``dynamic_dict()`` which makes this
    behavior default for all lookups.

    >>> d = betterdict()
    >>> d.cache_get('2**16', eval)
    65536
    >>> d
    {'2**16': 65536}

    """
    if (val := self.get(key, _MISSING)) is _MISSING:
      self[key] = val = factory(key)
    return val

  def insert(self, key, value, missing=None):
    """Equivalent to ``self[key] = value`` but returns the previous value.

    If no previous value at the given key, ``missing`` is returned.

    """
    previous = dict.get(self, key, missing)
    self[key] = value
    return previous
