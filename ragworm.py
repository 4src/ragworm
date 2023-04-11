# vim: set et sts=2 sw=2 ts=2 :
from lib import *
import math
import random
from copy import deepcopy
from functools import cmp_to_key

#------------------------------------------------ --------- --------- ----------
the = BAG(cohen=.5, nums=256, bins=7, k=1, m=2, go=".",
          min=.5, rest=3, file="../data/auto93.csv", seed=1234567891)
#------------------------------------------------ --------- --------- ----------
def SYM(c=0,s=" "):
   return BAG(ako=SYM, at=c, txt=s, n=0, _has={},mode=None,most=0)

def NUM(c=0,s=" "):
  return BAG(ako=NUM, at=c, txt=s, n=0, _has=[], ok=False,
              lo=inf, hi=-inf, w = -1 if s[-1]=="-" else 1)

def COLS(words):
  cols = BAG(ako=COLS, names=words, named={}, x=[], y=[], all=[], klass=None)
  for c,s in enumerate(words):
    col = (NUM if s[0].isupper() else SYM)(c,s)
    cols.named[s] = col
    cols.all += [col]
    if s[-1] != "X":
      if s[-1]=="!": klass=col
      (cols.y if s[-1] in "-+" else cols.x).append(col)
  return cols

def DATA(src, rows=[]):
  data = BAG(ako=DATA, cols=[], rows=[])
  if type(src)==str:
    [adds(data, ROW(a)) for a in csv(src)]
  elif src.ako is DATA:
    data.cols = COLS(src.cols.names)
  [adds(data,row) for row in rows]
  return data

def ROW(a):
  return BAG(ako=ROW, cells=a, cooked=a[:])
#------------------------------------------------ --------- --------- ----------
def adds(data,row):
  if data.cols:
    data.rows += [row]
    for col in data.cols.all: add(col,row.cells[col.at])
  else:
    data.cols = COLS(row.cells)

def add(col,x,inc=1):
  if x == "?": return x
  col.n += inc
  if col.ako is SYM:
    tmp = col._has[x] = col._has.get(x,0) + inc
    if tmp > col.most:
      col.most,col.mode = tmp,x
  else:
    col.lo = min(x, col.lo)
    col.hi = max(x, col.hi)
    if len(col._has) < the.nums:
      col.ok=False
      col._has += [x]
    elif r() < the.nums/col.n:
      col.ok=False
      col._has[int(len(col._has)*r())] = x

def ok(col):
  if col.ako is NUM and not col.ok: 
    col._has=sorted(col._has)
    col.ok=True
  return col

def mid(col):
  return col.mode if col.ako is SYM else median(ok(col)._has)

def div(col):
  return ent(col._has) if col.ako is SYM else stdev(ok(col)._has)

def stats(data, cols=None, fun=mid):
  tmp = {col.txt: fun(col) for col in (cols or data.cols.y)}
  tmp["N"] = len(data.rows)
  return BAG(**tmp)

def norm(num,x):
  return x if x=="?" else (x - num.lo)/(num.hi - num.lo + 1/inf)
#------------------------------------------------ --------- --------- ----------
def better(data, row1, row2):
  s1, s2, cols, n = 0, 0, data.cols.y, len(data.cols.y)
  for col in cols:
    a, b = norm(col,row1.cells[col.at]), norm(col,row2.cells[col.at])
    s1  -= math.exp(col.w * (a - b) / n)
    s2  -= math.exp(col.w * (b - a) / n)
  return s1 / n < s2 / n

def betters(data, rows=None):
  rows = sorted(rows or data.rows,
               key = cmp_to_key(lambda r1,r2:better(data,r1,r2)))
  cut = len(rows) - int(len(rows))**the.min
  best,rest = [],[]
  for i,row in enumerate(rows):
    row.y = i > cut
    (best if i > cut else rest).append(row)
  return DATA(data,best), DATA(data,random.sample(rest, len(best)*the.rest))

# def colv(data,row):
#   if type(row) is dict:
#     for k in row:
#       yield data.cols.named[k], row[k]
#   else:
#     for col in data.cols.x:
#       v = row.cells[col.at]
#       if v != "?" : yield col, [v]
#
# def classify(datas, row):
#   most, out, n = -inf, datas[0], sum(len(data.rows) for data in datas)
#   for klass,,data in datas.items():
#     prior = (len(data.rows) + the.k) / (n + the.k*len(datas))
#     tmp   = math.log(prior)
#     for col,vs in colv(data,row):
#       f    = sum((col.has.get((klass, col.at, v),0) for v in vs))
#       tmp += math.log((f + the.m*prior) / (col.n + the.m))
#     if tmp > most:
#       most, out = tmp, data
#   return klass,out,math.e**mostlike
# #------------------------------------------------ --------- --------- ----------
# def discretize(col,x)
#   if x=="?" or col.ako == SYM: return x
#   tmp = (col.hi - col.lo)/(the.bins - 1)
#   return col.hi == col.lo and 1 or int(x/tmp + .5)*tmp
#
def bins(best,rest):
  for col in best.cols.x:
    if col.ako is NUM:
      x = lambda row: row.cells[col.at]
      rows  = sorted([row for row in best.rows+rest.rows if x(row) != "?"])
      eps   =  stdev(rows, x) * the.cohen
      small = int(len(a) / the.bins)
      ys0,ys1,ys12,xs = SYM(),SYM(),SYM(),NUM()
      for i,row in enumerate(rows):
        row.cooked[col].at = label
        add(xs,x(row))
        add(ys1, row.y)
        add(ys12,row)
        new = x(row) - x0 > eps and xs.n > small and len(rows) - small > i and
        ys0=ys1
        ys1=SYM()

# def tally(best,rest):
#   out={}
#   for col in best.cols.x:
#     for rows in [best.row, rest.rows]:
#       for row in rows:
#         x = row.cells[col.at]
#         if x != "?":
#           k = (row.y, col.at, discretize(col,x))
#           out[k] = out.get(k,0) + 1
#   return out
#
# def BIN(col):
#   return BAG(ako=BIN, _rows=[], at=col.at, txt=col.txt,
#              score=0, x=BAG(lo=inf, hi=-inf), y=SYM())
#
# def binAdd(bin, row, x, y, fun=lambda b,r: b):
#   add(bin.y, y)
#   bin.score  = fun(bin.y.has.get(True,10**-30), bin.y.has.get(False,10**-30))
#   bin._rows += [row]
#   bin.x.lo   = min(x, bin.x.lo)
#   bin.x.hi   = max(x, bin.x.hi)
#
# def showBins(bins):
#   tmp={}
#   for b in bins:
#     if b.txt not in tmp: tmp[b.txt] = []
#     tmp[b.txt] += [(b.x.lo, b.x.hi)]
#   return {k:sorted(v) for k,v in tmp.items()}
#
# def bins(data,fun):
#   out = []
#   for cols in [data.cols.x] : #  data.cols.y]:
#     for col in cols:
#       if col.ako is NUM:
#         x    = lambda row: row.cells[col.at]
#         a    = sorted([row for row in data.rows if x(row) != "?"], key=x)
#         n    = len(a)
#         out += _bins(a,col,x,fun, eps=the.cohen*div(col), tiny=n/the.bins)
#   return sorted(out, key=lambda b:b.score,reverse=True)
#
# def _bins(rows,col,x, fun, eps=.35, tiny=4):
#   out, new = [BIN(col)], True
#   for i,row in enumerate(rows):
#     if new:
#       new = False
#       out += [BIN(col)]
#     bin = out[-1]
#     binAdd(bin, row, x(row), row.y, fun)
#     if len(bin._rows) > tiny and len(rows) - i > tiny:
#       if x(row) - x(bin._rows[0]) > eps:
#         new = x(row) != x(rows[i+1])
#   return out
# #------------------------------------------------ --------- --------- ----------
# def rules(bins,fun):
#   best = 0
#   for i in range(4): 
#     some = bins[:i+1]
#     _and = set.intersection
#     _or  = set.union
#     a    = {}
#     for b in sorted(some, key=lambda b:b.at):
#       s = set(b._rows)
#       a[b.at] = _or(s, a[b.at]) if b.at in a else s
#     a = _and(*map(set, a.values()))
#     b,r = 0,0
#     for row in a:
#       b += (1 if row.y else 0)
#       r += (0 if row.y else 1)
#     now = fun(b,r)
#     if now > best:
#       best = now
#       print(BAG(score=f"{now:.3f}",
#                 best=b,rest=r,rule=showBins(some)))
