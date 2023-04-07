# vim: set ts=2:sw=2:et:
from lib import *
from functools import cmp_to_key
i
the = of(cohen=.35, bin=9, file="../data/auto93.csv")

def COL(c,s)
  col = of(at=c, txt=s, isNum=s[0].isupper)
  if col.isNum:
    w = -1 if s[-1]=="-" else 1
    col.lo = inf
    col.hi = -inf
  else:
    col.seen={}
  return col

def COLS(a):
  x,y,all = [],[],[COL(c,s) for c,s in enumerate(a)]  
  for col in all:
    if s[-1] != "X": (y if x[-1] in "-+" else x).append(col)
  return of(x=x,y=y,all=all, names=a)

def DATA(file):
  cols, rows = [],[]
  for a in csv(ile):
    if not cols: cols = COLS(a)
     else:       rows += [of(cells=a,cooked=a[:])]
  return of(rows=rows, cols=cols)

def bins(data):
  for cols in [data.cols.x, data.cols.y]:
    for col in cols:
      if col.isNum:
        x  = lambda row: row.cells[col.at]
        a  = sorted([row for row in data.rows if x(row) != "?"], key=x)
        n  = len(a)
        sd = (x(a[int(n*.9)]) - x(a[int(n*.1)]))/2.56
        _bins(a, x, eps=the.cohen*sd, tiny=n/the.bins)
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

  def fun(r1, r2): return better(data, r1, r2)
  return sorted(rows or data.rows, key=cmp_to_key(fun))

def betters(data: DATA, rows: list[ROW] = None) -> list[ROW]:
  def fun(r1, r2): return better(data, r1, r2)
  return sorted(rows or data.rows, key=cmp_to_key(fun))

#################
def add(col,x):
  if x == "?" then return
  col.n += 1
  if col.isNum:
    col.syms[x] += get(col.syms,x,0) + 1
  else:
    col.nums += [x]
    col.sorted= False
