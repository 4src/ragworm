import re
import ast

inf=float('inf')

def same(x): return x

def coerce(x):
  return x if x=="?" else ast.literal_eval(x)

class O(object):
  def __init__(self, **d): self.__dict__.update(**d)
  def __repr__(self):
    return self.__class__.__name__+"{"+(" ".join([f":{k} {v}" for k, v in d.items()]))+"}"

def csv(file:str):
  "Iterator for CSV files"
  with open(file) as fp:
    for line in fp:
      line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
      if line:
         yield [cell.strip() for cell in line.split(",")]


