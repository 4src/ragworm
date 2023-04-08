# vim: set ts=2:sw=2:et:
from lib import *
from functools import cmp_to_key

the = has(cohen=.35, bin=9, file="../data/auto93.csv")

def COL(c,s):
  col = has(at=c, txt=s, isNum=s[0].isupper())
  if col.isNum:
    w = -1 if s[-1]=="-" else 1
    col.lo =  inf
    col.hi = -inf
  else:
    col.seen = {}
  return col

def COLS(a):
  cols = has(names=a, x=[], y=[], all=[COL(c,s) for c,s in enumerate(a)])
  for col in cols.all:
    if col.txt[-1] != "X":
      (cols.y if col.txt[-1] in "-+" else cols.x).append(col)
  return cols

def DATA(file):
  data = has(cols=[], rows=[])
  for a in csv(file):
    if not data.cols:
      data.cols = COLS(a)
    else:
      a = [coerce(x) for x in a]
      data.rows += [has(cells=a, cooked=a[:])]
      for cols in [data.cols.x, data.cols.y]:
        for col in cols:
          add(col, a[col.at])
  return data

def add(col,x):
  if x != "?":
    if col.isNum:
      col.lo = min(x, col.lo)
      col.hi = max(x, col.hi)
  return x

def bins(data):
  for cols in [data.cols.x, data.cols.y]:
    for col in cols:
      if col.isNum:
        x  = lambda row: row.cells[col.at]
        a  = sorted([row for row in data.rows if x(row) != "?"], key=x)
        n  = len(a)
        _bins(a, x, eps=the.cohen*stdev(a,x), tiny=n/the.bins)
  return data

def _bins(rows,x,eps=.35,tiny=4):
  nz,z,new, lo = 0,-1,True
  for i,r in enumerate(rows):
    if new:
      nz, z, lo, new = 0, z+1, x(r), False
    nz += 1
    r.cooked[col.at] = z
    new = nz > tiny and len(rows)-i > tiny and x(r)-lo > eps and x(r) != x(rows[i+1])

def better(data, row1, row2):
  s1, s2, cols, n = 0, 0, data.cols.y, len(data.cols.y)
  for col in cols:
    x    = lambda row: row.cells[col.at]
    norm = lambda row: (x(col,row)-col.lo)/(col.hi - col.lo + 1/inf)
    a, b = norm(col,row1), norm(col,row2)
    s1 -= math.exp(col.w * (a - b) / n)
    s2 -= math.exp(col.w * (b - a) / n)
  return s1 / n < s2 / n

def betters(data, rows):
  def fun(r1, r2): return better(data, r1, r2)
  return sorted(rows or data.rows, key=cmp_to_key(fun))

def stdev(a,fun):
  return (fun(a[ int(len(a)*.9) ]) - fun(a[ int(len(a)*.1) ]))/2.56
