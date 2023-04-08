# vim: set et sts=2 sw=2 ts=2 :
from lib import *
import math
from copy import deepcopy
from functools import cmp_to_key
#------------------------------------------------ --------- --------- ----------
the = bag(cohen=.35, bins=9, file="../data/auto93.csv")
#------------------------------------------------ --------- --------- ----------
def SYM(c=0,s=" "):
   return bag(ako=SYM, at=c, txt=s, n=0, tally={})

def NUM(c=0,s=" "):
  return bag(ako=NUM, at=c, txt=s, n=0, mu=0, m2=0,
              lo=inf, hi=-inf, w = -1 if s[-1]=="-" else 1)

def COLS(a):
  cols = bag(ako = COLS, names = a, x=[], y=[], all=[])
  for c,s in enumerate(a):
    col = (NUM if s[0].isupper() else SYM)(c,s)
    cols.all += [col]
    if s[-1] != "X":
      (cols.y if s[-1] in "-+" else cols.x).append(col)
  return cols

def DATA(src, rows=[]):
  data = bag(ako=DATA, cols=[], rows=[])
  if type(src)==str:    [dataAdd(data,a) for a in csv(src)]
  elif src.ako is DATA: dataAdd(data,src.cols.names)
  [dataAdd(data,r) for r in rows]
  return data

def ROW(a):
  return bag(ako=ROW, cells=a, cooked=a[:])
#------------------------------------------------ --------- --------- ----------
def dataAdd(data,a):
  if not data.cols:
    data.cols = COLS(a)
  else:
    data.rows += [ROW([colAdd(col,x) for col,x in zip(data.cols.all,a)])]

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

def norm(num,x):
  return x if x=="?" else (x - num.lo)/(num.hi - num.lo + 1/inf)

def syms(rows, x=lambda z:z):
  s=SYM(); [colAdd(s,x(row)) for row in rows]; return s
#------------------------------------------------ --------- --------- ----------
def BIN(col):
  return bag(ako=BIN, rows=[], at=col.at, txt=col.txt, lo=inf, hi=-inf, klasses=SYM())

def binAdd(bin,row,x,y):
  add(bin.klasses, y)
  bin.rows += [row]
  bin.xlo = min(x, bin.xlo)
  bin.xhi = max(x, bin.xhi)

def bins(data):
  out = []
  for cols in [data.cols.x, data.cols.y]:
    for col in cols:
      if col.ako is NUM:
        x = lambda row: row.cells[col.at]
        a = sorted([row for row in data.rows if x(row) != "?"], key=x)
        n = len(a)
        print(out, _bins(a,col,x,eps=the.cohen*stdev(a,x),tiny=n/the.bins))
        out += _bins(a,col,x,eps=the.cohen*stdev(a,x),tiny=n/the.bins)
  return out

def _bins(rows, col, x, eps=.35, tiny=4):
  out, new = [BIN(col)], True
  for i,row in enumerate(rows):
    if new:
      new = False
      out += [BIN(col)]
    bin = out[-1]
    binAdd(bin, row, row.y)
    if len(bin.rows) > tiny and len(rows) - i > tiny:
      if x(row) - x(bin.rows[0]) > eps:
        new = x(row) != x(rows[i+1])
  return out

def better(data, row1, row2):
  s1, s2, cols, n = 0, 0, data.cols.y, len(data.cols.y)
  for col in cols:
    x    = lambda row: row.cells[col.at]
    a, b = norm(col,row1.cells[col.at]), norm(col,row2.cells[col.at])
    s1  -= math.exp(col.w * (a - b) / n)
    s2  -= math.exp(col.w * (b - a) / n)
  return s1 / n < s2 / n

def betters(data, rows=None):
  rows = rows or data.rows
  def fun(r1, r2): return better(data, r1, r2)
  return sorted(rows or data.rows, key=cmp_to_key(fun))

def stdev(a,fun):
  return (fun(a[ int(len(a)*.9) ]) - fun(a[ int(len(a)*.1) ]))/2.56
