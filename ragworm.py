# vim: set et sts=2 sw=2 ts=2 :
from lib import *
import math
import random
from copy import deepcopy
from functools import cmp_to_key
#------------------------------------------------ --------- --------- ----------
the = BAG(cohen=.5, bins=7, min=.5, rest=3, file="../data/auto93.csv", seed=1234567891)
#------------------------------------------------ --------- --------- ----------
def SYM(c=0,s=" "):
   return BAG(ako=SYM, at=c, txt=s, n=0, tally={})

def NUM(c=0,s=" "):
  return BAG(ako=NUM, at=c, txt=s, n=0, mu=0, m2=0,
              lo=inf, hi=-inf, w = -1 if s[-1]=="-" else 1)

def COLS(a):
  cols = BAG(ako=COLS, names=a, x=[], y=[], all=[], klass=None)
  for c,s in enumerate(a):
    col = (NUM if s[0].isupper() else SYM)(c,s)
    cols.all += [col]
    if s[-1] != "X":
      if s[-1]=="!": klass=col
      (cols.y if s[-1] in "-+" else cols.x).append(col)
  return cols

def DATA(src, rows=[]):
  data = BAG(ako=DATA, cols=[], rows=[])
  if type(src)==str:
    [dataAdd(data, ROW(a)) for a in csv(src)]
  elif src.ako is DATA:
    data.cols = COLS(src.cols.names)
  [dataAdd(data,row) for row in rows]
  return data

def ROW(a):
  return BAG(ako=ROW, cells=a, cooked=a[:])
#------------------------------------------------ --------- --------- ----------
def dataAdd(data,row):
  if data.cols:
    data.rows += [row]
    for col in data.cols.all: colAdd(col,row.cells[col.at])
  else:
    data.cols = COLS(row.cells)

def colAdd(col,x,inc=1):
  if x != "?":
    col.n += inc
    if col.ako is NUM:
      col.lo  = min(x, col.lo)
      col.hi  = max(x, col.hi)
      d       = x - col.mu
      col.mu += d/col.n
      col.m2 += d * (x - col.mu)
    else:
      col.tally[x] = col.tally.get(x,0) + inc
  return x

def mid(col):
  return col.mu if col.ako is NUM else max((n,x) for c,x in col.tally.items)[1]

def div(col):
  def fun(x): return p*math.log(p,2)
  if col.ako is NUM: return (col.m2/(col.n - 1))**.5
  return -sum((fun(n/col.n) for n in col.tally.values() if n>0))

def stats(data, cols=None, fun=mid):
  tmp = {col.txt: fun(col) for col in (cols or data.cols.y)}
  tmp["N"] = len(data.rows)
  return BAG(**tmp)

def norm(num,x):
  return x if x=="?" else (x - num.lo)/(num.hi - num.lo + 1/inf)

def syms(rows, x=lambda z:z):
  s=SYM(); [colAdd(s,x(row)) for row in rows]; return s
#------------------------------------------------ --------- --------- ----------
def better(data, row1, row2):
  s1, s2, cols, n = 0, 0, data.cols.y, len(data.cols.y)
  for col in cols:
    y    = lambda row: row.cells[col.at]
    a, b = norm(col,y(row1)), norm(col,y(row2))
    s1  -= math.exp(col.w * (a - b) / n)
    s2  -= math.exp(col.w * (b - a) / n)
  return s1 / n < s2 / n

def betters(data, rows=None):
  rows = rows or data.rows
  def fun(r1, r2): return better(data, r1, r2)
  rows= sorted(rows or data.rows, key=cmp_to_key(fun))
  n = int(len(rows))**the.min
  best,rest = [],[]
  for i,row in enumerate(rows):
    row.y = i > len(rows) - n
    (best if row.y else rest).append(row)
  B,R = len(best), the.rest*len(best)
  def fun(b,r):
    b,r = b/(B+10**-30), r/(R+10**-30)
    return b**2/(b+r)
  return DATA(data, best + random.sample(rest, R)), fun
#------------------------------------------------ --------- --------- ----------
def BIN(col):
  return BAG(ako=BIN, _rows=[], at=col.at, txt=col.txt,
             score=0, x=BAG(lo=inf, hi=-inf), y=SYM())

def binAdd(bin, row, x, y, fun=lambda b,r: b):
  colAdd(bin.y, y)
  bin.score  = fun(bin.y.tally.get(True,10**-30), bin.y.tally.get(False,10**-30))
  bin._rows += [row]
  bin.x.lo   = min(x, bin.x.lo)
  bin.x.hi   = max(x, bin.x.hi)

def showBins(bins):
  tmp={}
  for b in bins:
    if b.txt not in tmp: tmp[b.txt] = []
    tmp[b.txt] += [(b.x.lo, b.x.hi)]
  return {k:sorted(v) for k,v in tmp.items()}

def bins(data,fun):
  out = []
  for cols in [data.cols.x] : #  data.cols.y]:
    for col in cols:
      if col.ako is NUM:
        x    = lambda row: row.cells[col.at]
        a    = sorted([row for row in data.rows if x(row) != "?"], key=x)
        n    = len(a)
        out += _bins(a,col,x,fun, eps=the.cohen*div(col), tiny=n/the.bins)
  return sorted(out, key=lambda b:b.score,reverse=True)

def _bins(rows,col,x, fun, eps=.35, tiny=4):
  out, new = [BIN(col)], True
  for i,row in enumerate(rows):
    if new:
      new = False
      out += [BIN(col)]
    bin = out[-1]
    binAdd(bin, row, x(row), row.y, fun)
    if len(bin._rows) > tiny and len(rows) - i > tiny:
      if x(row) - x(bin._rows[0]) > eps:
        new = x(row) != x(rows[i+1])
  return out
#------------------------------------------------ --------- --------- ----------
def rules(bins,fun):
  best = 0
  for i in range(4): 
    some = bins[:i+1]
    _and = set.intersection
    _or  = set.union
    a    = {}
    for b in sorted(some, key=lambda b:b.at):
      s = set(b._rows)
      a[b.at] = _or(s, a[b.at]) if b.at in a else s
    a = _and(*map(set, a.values()))
    b,r = 0,0
    for row in a:
      b += (1 if row.y else 0)
      r += (0 if row.y else 1)
    now = fun(b,r)
    if now > best:
      best = now
      print(BAG(score=f"{now:.3f}",
                best=b,rest=r,rule=showBins(some)))
