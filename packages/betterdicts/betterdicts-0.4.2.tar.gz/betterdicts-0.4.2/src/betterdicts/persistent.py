import pickle
# import copyreg -- the old way
from pathlib import Path
from functools import wraps

from betterdicts import betterdict

__all__ = ('persistent_dict',)

def make_wrapper(name, meth):
  @wraps(meth)
  def _override(self, /, *args, **kwargs):
    ret = meth(self, *args, **kwargs)
    self.save()
    return ret
  return wraps(meth)(_override)


class PersistentMeta(type):
  def __new__(cls, name, bases, ns):
    for meth_name in '__setitem__ __delitem__ clear update pop popitem setdefault insert'.split():
      ns[meth_name] = make_wrapper(meth_name, getattr(betterdict, meth_name))
    return type.__new__(cls, name, bases, ns)

  def __call__(cls, *args, **kwargs):
    if cls is not persistent_dict:
      print('not pers', args, kwargs)
      obj = cls.__new__(cls)
      obj.__init__(*args, **kwargs)
      return obj
    print('pers')

    if args and isinstance(args[0], (str, Path)):
      pth = Path(args[0])
      args = args[1:]
    else:
      pth = Path.cwd() / 'cache.pickle'

    # Trick to push the filename into the class information.
    class persistent_instance(persistent_dict):
      _path = pth

    obj = persistent_instance.__new__(persistent_instance)
    obj.__init__(*args, **kwargs)
    if pth.is_file():
      with pth.open('rb') as fil:
        data = pickle.load(fil)
      dict.update(obj, data)
    if args:
      obj.save()
    return obj

  # # Needed to prevent dict() from giving its own reduce tuple.
  # def __reduce_ex__(self, pv):
  #   return (copyreg.__newobj_ex__, (persistent_dict, (dict(self), ), {'skip_load': True}))


class persistent_dict(betterdict, metaclass=PersistentMeta):
  """A dict that auto-saves itself to disk _whenever it is modified_.

  Simply creating the instance `persistent_dict()` will auto-load the previous
  content from the default file `cache.pickle` in the current directory. To
  specify another file use `persistent_dict(<filename>)`.

  Any modifications to the dictionary will be synced to this file. Note that
  "deep" changes are not detected -- i.e. modifications to a list stored in the
  dictionary. Thus it works best for simple, flat values.

  If a a lot modifications need to be done in one go (e.g. a tight loop), you
  can use a regular `dict()` and then periodically invoke `obj.update(work)` to
  update and save.

  Warning:: Use separate files for separate objects. Two separate
  `persistent_dict()` objects bound to the same file will *not* stay in sync.
  Whichever object was modified (and thus saved) last will be what is reflected
  in the saved file.

  """
  __slots__ = ()
  _path = None

  # The meta class injecs save-logic in the regular methods.

  def save(self):
    """Save the dictionary to a pickle file.

    """
    with self._path.open('wb') as fil:
      pickle.dump(dict(self), fil)
    return self
