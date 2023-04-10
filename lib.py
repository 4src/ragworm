# vim: set ts=2:sw=2:et:
import re
import ast
import sys
import math
import random
import traceback
from copy import deepcopy
from termcolor import colored


seed = random.seed
r    = random.random

inf  = sys.maxsize / 2
ninf = -inf - 1

def showd(d): return "{"+(" ".join([f":{k} {show(v)}"
                         for k,v in d.items() if k[0]!="_"]))+"}"

def show(x):
  if callable(x)         : return x.__name__+'()'
  if isinstance(x,float) : return f"{x:.2f}"
  return x

def per(a, p=.5, key=lambda x:x):
  p=int(len(a)*p); p=max(0,min(len(a)-1,p)); return key(a[p])

def median(a, key=lambda x:x):
  return key(per(a,.5))

def stdev(a, key=lambda x:x):
  return (key(per(a,.9)) - key(per(a,.1)))/2.56

def ent(d):
  n = sum(( d[k] for k in d))
  return -sum((d[k]/n*math.log(d[k]/n,2) for k in d if d[k]>0))

def coerce(x):
  if x=="?": return x
  try: return ast.literal_eval(x)
  except: return x

def cli(d):
  for k,v in d.items():
    v=str(v)
    for i,x in enumerate(sys.argv):
      if ("-"+k[0]) == x:
         v="False" if v=="True" else ("True" if v=="False" else sys.argv[i+1])
      d[k] = coerce(v)
  return d


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

def runs(the,funs):
  return sum((run(fun,the) for fun in funs if todo(fun,the)))

def todo(f,the):
  return f.__name__ == the.go or the.go=="all"

def yell(s,c):
  print(colored(s,"light_"+c,attrs=["bold"]),end="")

def run(fun,the):
  fail, cache = False, deepcopy(the)
  try:
    yell((fun.__name__ or "fun")+"\t","yellow")
    print((fun.__doc__ or "")+ " ",end="")
    seed(the.seed)
    fail = fun() == False
  except:
    print(traceback.format_exc())
  if fail: yell("FAIL\n","red")
  else:    yell("PASS\n","green")
  for k,v in cache.items(): the[k] = v
  return fail


