
try:
  from .VERSION import __version__
except:
  pass

from .betterdict import betterdict
from .jsdict import attr_dict, jsdict, njsdict, rjsdict
from .persistent import persistent_dict
from .number_dict import number_dict
from .dynamic_dict import dynamic_dict, cache_dict
