# vim: set ts=2:sw=2:et:
import re
import ast
import sys

inf  = sys.maxsize / 2
ninf = -inf - 1

def same(x)   : return x
def coerce(x) : return x if x=="?" else ast.literal_eval(x)
def showd(d)  : return "{"+(", ".join([f"{k}:{show(v)}" for k,v in d.items()]))+"}"
def show(x)   :
  if callable(x): return x.__name__
  if isinstance(x,float): return round(x, ndigits=3)
  return x

class has(dict):
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__
  __repr__    = showd

def csv(file):
  with open(file) as fp:
    for line in fp:
      line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
      if line:
        yield [cell.strip() for cell in line.split(",")]
