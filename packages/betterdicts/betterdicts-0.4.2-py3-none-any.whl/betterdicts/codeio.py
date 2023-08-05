import io

# This is all stupid. Will be replaced.

class CodeIO(io.StringIO):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.indent = 0

  def __enter__(self):
    self.indent += 2
  def __exit__(self, *args):
    self.indent -= 2

  def print(self, fmt, *args, **kwargs):
    print(self.indent * ' ' + fmt, *args, **kwargs, file=self)

  def exec(self, locals=None, globals=None):
    if locals is None:
      locals = dict()
    if globals is None:
      globals = dict()
    exec(self.getvalue(), globals, locals)
    return locals, globals
