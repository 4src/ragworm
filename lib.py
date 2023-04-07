# vim: set ts=2:sw=2:et:
import re
import ast
import sys

inf  = sys.maxsize / 2
ninf = -inf - 1

def same(x)  : return x
def coerce(x): return x if x=="?" else ast.literal_eval(x)
def showd(d) : return "S("+(" ".join([f":{k} {v}" for k, v in d.items()]))+")"

class of(dict):
  """dot.notation access to dictionary attributes"""
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__
  __repr__    = showd

def csv(file:str):
  "Iterator for CSV files"
  with open(file) as fp:
    for line in fp:
      line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
      if line:
         yield [cell.strip() for cell in line.split(",")]


