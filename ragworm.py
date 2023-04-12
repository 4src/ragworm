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

def freqs(best,rest):
  out = {}
  for col in best.cols.x:
    def x(row): return row.cells[col.at]
    def inc(lo, hi, row):
      if  lo != "?" and hi != "?" :
         k = (col.at, x, x, row.y)
         out[k] = out.get(k,0) + 1
    #----------------
    if col.ako is NUM:
      [inc(b.lo, b.hi, r) for b in merges(bins1(x,best,rest)) for r in b.rows]
    else:
      [inc(x(r), x(r), r) for r in best.rows+rest.rows]
  return out

def bins1(x,best,rest):
  bin   = lambda lo: BAG(rows=[], lo=lo, hi=lo, ys=SYM())
  rows  = sorted([row for row in best.rows+rest.rows if x(row) != "?"])
  eps   = stdev(rows, x) * the.cohen
  small = int(len(rows) / the.bins)
  bags += [bin(x(rows[0]))]
  for i,row in enumerate(rows):
    now       = all[-1]
    now.hi    = x(row)
    now.rows += [row]
    add(now.ys, row.y)
    if now.hi - now.lo > eps and now.ys.n > small and i < len(rows) - small:
      bags += [bin(x(row))]
  return bags

def merges(b4):
  i,now = 0,[]
  while i < len(b4):
    one = b4[i]
    if i < len(b4) - 1:
      two = b4[i+1]
      if ys := merged(one.ys, two.ys):
        one = BAG(rows=one.rows + two.rows, lo=one.lo, hi=two.hi, ys=ys)
        i += 1
    now += [one]
    i += 1
  return fillInTheGaps(b4) if len(b4) == len(now) else merges(now)

def merged(col1, col2):
  col12 = deepcopy(col1)
  [add(col12,s,n) for s,n in col2._has.items()]
  if div(col12) <= (col1.n*div(col1) + col2.n*div(col2))/col12.n:
    return col12

def fillInTheGaps(a):
  a[0].lo, a[-1].hi = -inf, inf
  for i in ranges(len(a)-1): a[i].hi = a[i+1].lo
  return a

# def showBins(bins):
#   tmp={}
#   for b in bins:
#     if b.txt not in tmp: tmp[b.txt] = []
#     tmp[b.txt] += [(b.x.lo, b.x.hi)]
#   return {k:sorted(v) for k,v in tmp.items()}
#
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
