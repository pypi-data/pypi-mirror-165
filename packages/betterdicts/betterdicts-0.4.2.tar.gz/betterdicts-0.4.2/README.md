# betterdicts

A collection of dictionary and dictionary-like classes improving on the built-in
`dict` type and providing some extra utility.

## betterdict

``` python
from betterdicts import betterdict
```

Intended to work just like a dict, but with extra functionality and convenience.

Most of these things can be achieved with simple generator expressions or
similar, but having need of them constantly it got to a boiling point.

### Increased Functional Friendliness

`obj.update()` and `obj.clear()` now return `obj` instead of `None`, so they are
no longer _as_ useless.

```python-console
>>> d = betterdict()
>>> d.update(a=1).update(zip('abc', [7,4,2]))
{'a': 7, 'b': 4, 'c': 2}
```

There's also `betterdict.insert(key, value, [missing])` as an alternative to
`obj[key] = value`. It returns the previous value (if present).

``` python-console
>>> d.insert('b', 69)
4
>>> d.insert('d', 0)
>>> d.insert('e', 0, 'default return value goes here')
'default return value goes here'
>>> d
{'a': 7, 'b': 69, 'c': 2, 'd': 0, 'e': 0}
```

Python being a statement-oriented language rather than expression-oriented can
sometimes get in the way when you want to do simple operations inside of a list
comprehension or test. These methods are intended to temper this problem.

``` python-console
>>> d = betterdict()
>>> [d.insert(len(w), w) for w in 'fare thee well great heart'.split()]
[None, 'fare', 'thee', None, 'great']
>>> d
{4: 'well', 5: 'heart'}
```

Note that `del obj[x]` (a good example of Python's statement fanaticism) already
has an expression alternative in `dict.pop(x, [default])`.

The annoyance of statements led to the infamous walrus wart`^W`operator being
added after several bikeshed bonfires, finally admitting that
expression-oriented language design is _objectively superior_. [TODO: add
tongue-in-cheek emoji here.]

### Combining and Collecting
  
Often you're collecting things into dictionaries where the key you're interested
in is not unique. Or simiarly, if given a stream of keyed data, you usually need
some extra logic to handle identical keys.

One way to handle this is to write out some loop and add some
tedious-but-mandatory `if` branch in the loop. These loops start to feel like
Chinese water torture when they number in the thousands.

The default behavior of `dict` if you just give it an iterator is to discard
(overwrite). That default behavior has been kept, but alternatives have been
provided.

- `betterdict.combine(func, it, [initial=...])`

This works like the built-in `reduce(func, it, [initial])`. It works well when
you're dealing with simple data like numbers and you just want a single answer.

``` python-console
>>> betterdict.combine(int.__add__, [('a',1), ('a',5), ('b',2), ('a',7)])
{'a': 13, 'b': 2}
```

It's short-hand for two kinds of loops:

``` python-console
# with a specified initial value
for k, v in source:
  d[k] = func(d.get(k, initial), v)

# without
for k, v in source:
  if k in d:
    d[k] = func(d[k], v)
  else:
    d[k] = v
```

This _can_ be used to put values into collections like in a functional language, as the following example:

``` python-console
>>> betterdict.combine(lambda x, y: x + (y,), [('a',1), ('a',5), ('b',2), ('a',7)], initial=())
{'a': (1, 5, 7), 'b': (2,)}
```

But it's very inefficient and painful to use with mutable containers like lists.
This is where `collect()` comes in:

- `betterdict.collect(type, it, [add_action=...])`

This will return a dictionary-of-collections, where the collection is created
with `type` and added with `add_action` (which defaults to being auto-detected
as something like `list.append`, `set.add`, etc.).

``` python-console
>>> betterdict.collect(list, [('a',1), ('a',5), ('b',2), ('a',7)])
{'a': [1, 5, 7], 'b': [2]}
```

A more realistic example:

``` python-console
>>> some_stream_of_words = open('README.md', 'r', encoding='utf-8').read().split()
>>> l2w = betterdict.collect(set, ((len(w), w) for w in some_stream_of_words))
>>> l2w[2]
{'{}', 'in', 'of', 'be', 'up', '(a', '-1', 'is', 'no', '4,', '6}', 'to', 'if', 'as', 'v)', '1,', '38', '"\'', '6:', 'As', '-c', '2,', 'w)', '8:', 'or', 'v:', '2}', '2:', 'on', '10', '==', 'x,', '7,', '0}', '-l', '4}', "',", 'k:', 'do', 'So', 'it', '4:', 'd:', '9,', '3)', 'at', '7:', 'Or', '3:', '40', '5:', '##', 'ad', '^D', 'an', '20', '9:', 'ls', "T'", 'p2', 'y:', '1}', 'It', 'To', 'so', '1)', '17', '0)', 'by', 'k,', '3,', '//', 'x:', '0,', '26', '5,', '+=', 'p1', 'me', '1:'}
```

These functions are magic in that they can work both as class methods and as
instance methods. The instance methods `obj.collect(...)` and `obj.combine(...)`
works kind of like a combining or collecting `obj.update()`. The only exception
is that `obj.combine()` works immutably by returning a new dictionary as if it
was a binary operator.

See `help(betterdict.combine)` and `help(betterdict.collect)` for more
information.

### Filtering and Mapping

`.map_keys(f)`, `.map_values(f)`, `.map_pairs(f)`, `.filter_keys(p)`,
`.filter_values(p)`, `.filter_pairs(p)` all do the somewhat obvious thing.

``` python-console
>>> q = betterdict(enumerate("I'm nothing but heart"))
>>> q.filter_keys(lambda x: 4 < x < 10)
{5: 'o', 6: 't', 7: 'h', 8: 'i', 9: 'n'}
>>> q.filter_values(str.isupper)
{0: 'I'}
```

Though it should be noted that unlike `.update` they do not modify the
dictionary in-place as they're targeting more functional programming.

`map_pairs(f)` and `filter_pairs(f)` take a function of two arguments.

``` python-console
>>> q.map_pairs(lambda x, y: (x, x * y))
{0: '', 1: "'", 2: 'mm', 3: '   ', 4: 'nnnn', 5: '', 6: 't', 7: 'hh', 8: 'iii', 9: 'nnnn', 10: '', 11: ' ', 12: 'bb', 13: 'uuu', 14: 'tttt', 15: '', 16: 'h', 17: 'ee', 18: 'aaa', 19: 'rrrr', 20: ''}
```

Since `map_keys()` and `map_pairs()` might map two values to the same key, they
also take a function and initial value as optional arguments to do a reduction,
similar to how the built-in `reduce()` works. (Refer to `.combine()`.)

``` python-console
>>> q.map_keys(lambda x: x%2, str.__add__)
{0: 'Imntigbthat', 1: "' ohn u er"} 
```

There's also `.filter([keys=f], [values=g])` and `.map([keys=f], [values=g])`
which can be used to filter/map both keys and values with two different
functions in one step:

``` python-console
>>> q.filter(lambda k: 4 < k < 10, lambda v: v in 'aeiouy')
{5: 'o', 8: 'i'}
```

### Inversion

Flipping those arrows.

```python-console
>>> q = betterdict(enumerate('divebar'))
>>> q
{0: 'd', 1: 'i', 2: 'v', 3: 'e', 4: 'b', 5: 'a', 6: 'r'}
>>> q.invert()
{'d': 0, 'i': 1, 'v': 2, 'e': 3, 'b': 4, 'a': 5, 'r': 6}
>>> q == q.invert().invert()
```

Note that `q.invert()` does _not_ modify `q`, but returns a new dictionary.
(Functional friendliness where it makes sense.)

Most of the time the map is not expected to be injective (one-to-one) though,
and there are two ways of handling that:

- you can either _collect_ values into a container like a list, or

``` python-console
>>> q = betterdict(enumerate('syzygy'))
>>> q.invert()
{'s': 0, 'y': 5, 'z': 2, 'g': 4}
>>> q.invert_and_collect(list)
{'s': [0], 'y': [1, 3, 5], 'z': [2], 'g': [4]}
>>> q.invert_and_collect(set)
{'s': {0}, 'y': {1, 3, 5}, 'z': {2}, 'g': {4}}
```

- you can _combine_ values repeatedly until you get a single answer.

```python-console
>>> q.invert_and_combine(int.__mul__)
{'s': 0, 'y': 15, 'z': 2, 'g': 4}
>>> q.invert_and_combine(lambda x, y: x+[y], [])
{'s': [0], 'y': [1, 3, 5], 'z': [2], 'g': [4]}
```

As seen above, collecting and combining are sometimes just special cases of a
more general operation (folding, repeated applicaitino of a monoid, etc). More
functional languages usually only has one operation for this, but I chose to
separate them because they have very a different feel in in Python, with very
different performance characteristics.


## jsdict (ad hoc use only)

``` python
from betterdicts import jsdict, njsdict, rjsdict
```

`jsdict` is a `betterdict`s which works like JavaScript object, where keys and
attributes are the same. This is accomplished with zero overhead.

``` python-console
>>> d = jsdict()
>>> d['hello'] = 1
>>> d.filepath = '/'
>>> d
{'hello': 1, 'filepath': '/'}
>>> d.hello, d['filepath']
(1, '/')
```

For _obvious reasons_, this is a touch insane. JavaScript was never accused of
good design, and bringing it to Python where conventions are different will lead
to awful things:

``` python-console
>>> d = jsdict(clear=0)
>>> d.clear()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not callable
```

Thus these are for _ad hoc_ use only, i.e. in one-off scripts or when doging
work directly in the REPL.

Refer to `attr_dict` below for a slightly safer alternative.

But sometimes this kind of convenience is just too good to pass up. You'll know
this in your heart too, if you've ever dealt with loading configuration from
some source that gives you a `dict`, and then having to type out `['...']` so
many times you actually get angry.

``` python-console
>>> import json
>>> config = json.loads('{"lazy": "sarah", "active": false}', object_pairs_hook=jsdict)
>>> config.active
False
>>> config
{'lazy': 'sarah', 'active': False}
```

I get equally angry whenever a source gives me some object of a godforsaken
abstract `ConfigurationProxyHelper` class which is just a glorified `dict`
without any of the functionality or compatibility.

- `rjsdict` is a `jsdict` where `obj.key` for a missing key automatically
  returns and inserts a new `rjsdict` instance. Think of it as a recursive
  `jsdict`. It's useful for when you're building some hierarchical structure:

``` python-console
 >>> config = rjsdict()
>>> config.lights = 'off'
>>> config.player.health = 40
>>> config.player.name = 'Mr. T'
>>> config
{'lights': 'off', 'player': {'health': 40, 'name': 'Mr. T'}}
```

- `njsdict` is a `jsdict` where `obj.key` evaluates to `None` instead of raising
  `AttributeError`. (`obj` is not modified.)

### attr_dict

``` python
from betterdicts import attr_dict
```

Inspired by `jsdict` above, it works in much the same way (though different
mechanism). It is provided as a slightly safer alternative, because it doesn't
overwrite extant attributes:

``` python-console
>>> q = attr_dict(a=10)
>>> q.a
10
>>> q.b = 20
>>> q
{'a': 10, 'b': 20}
>>> q.pop = -1
>>> q
{'a': 10, 'b': 20, 'pop': -1}
>>> q.pop
<built-in method pop of attr_dict object at 0x7fc85a580c40>
```

But note it is still has the glow of insanity, which will inspire nothing but
anger, fear, and frustration.

## dynamic_dict

``` python
from betterdicts import dynamic_dict, cache_dict
```

How many times have you been frustrated by the fact that the standard
`collections.defaultdict()` calls its factory function without providing the key
context?

Yeah, me too.


`dynamic_dict(f)` is equivalent to a `betterdict` but if a missing key is requested
it is first created with `f(key)` and inserted.

``` python-console
>>> d = dynamic_dict(hex)
>>> d[16]
'0x10'
>>> d[100]
'0x64'
>>> d
{16: '0x10', 100: '0x64'}
```

### cache_dict

How many times have you wanted concrete access to the function cache when using
something like `functools.cache`?

Yeah, me too.

Intended to be used as a decorator on a function, this will turn the function
into a callable dictionary. The dictionary is its own cache and can freely be
inspected, modified, etc.

``` python
@cache_dict
def heavy_bite(n):
  "Calculates a heavy bite."
  if n < 1: return 1
  print(f'calculating heavy bite {n}...')
  return heavy_bite(n // 3) * heavy_bite(n - 3 + (-n % 3)) + heavy_bite(n - 1)
```

``` python-console
>>> heavy_bite(10)
calculating heavy bite 10...
calculating heavy bite 3...
calculating heavy bite 1...
calculating heavy bite 2...
calculating heavy bite 9...
calculating heavy bite 6...
calculating heavy bite 5...
calculating heavy bite 4...
calculating heavy bite 8...
calculating heavy bite 7...
2880
>>> heavy_bite(10)
2880
>>> del heavy_bite[10]
>>> heavy_bite(10)
calculating heavy bite 10...
2880
>>> heavy_bite.__doc__
'Calculates a heavy bite.'
```

NOTE: per now it only caches on its first argument. The rest are just passed
through (in case of a cache miss). Ideally I want a way to specify an argument
signature with indication of which ones constitutes the key.

## number_dict

Acts like a `collections.Counter()` with arithmetic support like a number.

This is sort of a poor man's `numpy-dict`.

``` python-console
>>> q = number_dict(range(5))
>>> q
{0: 1, 1: 1, 2: 1, 3: 1, 4: 1}
>>> q[1] += 5
>>> q[4] += 1
>>> q[9]
0
>>> q[9] = 9
>>> (q+1)**2
{0: 4, 1: 49, 2: 4, 3: 4, 4: 9, 9: 100}
>>> 1 / q
{0: 1.0, 1: 0.16666666666666666, 2: 1.0, 3: 1.0, 4: 0.5, 9: 0.1111111111111111}
```

## persistent_dict

The _simplest possible_ persistent state exposed as a `betterdict`. Also
intended for ad hoc use.

This is for when you need something really simple and magic to store some flat
data between script invocations, without the extra management of a database or
file formats.

``` bash
[franksh@moso ~]$ python -iq -c 'from betterdicts import persistent_dict'
>>> p = persistent_dict()
>>> p
{}
>>> p['foo'] = 17
>>> p
{'foo': 17}
>>> persistent_dict()
{'foo': 17}
>>> p['bar'] = [1,2]
>>> persistent_dict()
{'foo': 17, 'bar': [1, 2]}
>>> ^D
[franksh@moso ~]$ ls -l cache.pickle 
-rw-r--r-- 1 franksh franksh 38 Aug 26 17:18 cache.pickle
[franksh@moso ~]$ python -iq -c 'from betterdicts import persistent_dict'
>>> persistent_dict()
{'foo': 17, 'bar': [1, 2]}
>>> 
```

It defaults to loading and saving from `./cache.pickle` in whatever the current
working directory happens to be, as seen above.

_Any change made directly[^1] to the dictionary causes it to save itself to disk
as a pickle file._ So obviously if you're building up some initial data quickly,
you want to use another dictionary first, and then convert it later with
`persistent_dict([filename], data)`. This will automatically both load and save.

To use a custom filename use `persisent_dict([filename])`:

``` python-console
[franksh@moso ~]$ python -iq -c 'from betterdicts import persistent_dict'
>>> p1 = persistent_dict('foo.p', dict(a=1,b=22,c=333))
>>> p2 = persistent_dict('bar.p', p1.invert())
not pers ({1: 'a', 22: 'b', 333: 'c'},) {}
>>> persistent_dict('foo.p')
{'a': 1, 'b': 22, 'c': 333}
>>> persistent_dict('bar.p')
{1: 'a', 22: 'b', 333: 'c'}
>>> del p2[22]
>>> p2 == persistent_dict('bar.p')
True
```

*Warning:* Two separate `persistent_dict()` objects bound to the same file will
not automatically stay in sync, instead they will keep overwriting each other's
data!

[^1]: "deep" changes, like modifying a mutable object in the dictionary are not detected
