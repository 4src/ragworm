# vim: set ts=2:sw=2:et:
import re
import ast
import sys
import random

seed = random.seed

inf  = sys.maxsize / 2
ninf = -inf - 1

def same(x) : return x
def showd(d): return "{"+(" ".join([f":{k} {show(v)}"
                         for k,v in d.items() if k[0]!="_"]))+"}"
def show(x):
  if callable(x)         : return x.__name__+'()'
  if isinstance(x,float) : return f"{x:.2f}"
  return x

def per(a, p=.5, key=lambda x:x):
  p=int((len(a) * p); p=math.max(0,math.min(len(a)-1,p)); return key(a[p])

def ent(d):
  N = sum(( d[k] for k in d))
  return -sum((n/N)*math.log(n/N,2) for n in col.has.values() if n>0))


def coerce(x):
  if x=="?": return x
  try: return ast.literal_eval(x)
  except: return x

class BAG(dict):
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__
  __repr__    = showd

#   bags=0
#   def __hash__(self) : return self._id
#
# def BAG(**d):
#   tmp = bag(**d)
#   bag.bags = tmp._id = bag.bags + 1
#   return tmp

def csv(file):
  with open(file) as fp:
    for line in fp:
      line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
      if line:
        yield [coerce(cell.strip()) for cell in line.split(",")]
