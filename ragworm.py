# vim: set et sts=2 sw=2 ts=2 :
"""
ragworm.py : the smallest AI brain I can imagine.    
(c) 2023 Tim Menzies <timm@ieee.og> BSD-2

USAGE:    
  python3 -B tests.py [OPTIONS] [-g ACTION]   

OPTIONS:  

  -b --bins   default number of bins                       = 16  
  -c --cohen  cohen's delta                                = .5  
  -f --file   data file                                    = ../data/auto93.csv  
  -g --go     start up action                              = nothing  
  -h --help   show help                                    = False  
  -k --k      Naive Bayes, low class frequency control     = 1  
  -m --m      Naive Bayes, low attribute frequency control = 2  
  -M --Min    recursion stops at N**M                      = .5  
  -r --rest   look at rest*|best| items                    = 3  
  -s --seed   random number seed                           = 1234567891   
  -S --Some   keep at least this number of numbers         = 256
"""
from lib import *
the=settings(__doc__)
#------------------------------------------------ --------- --------- ----------
def SYM(c=0,s=" "):
  "Summarize stream of symbols."
  return BAG(ako=SYM, at=c, txt=s, n=0, _has={},mode=None,most=0)

def NUM(c=0,s=" "):
  "Summarize stream of numbers."
  return BAG(ako=NUM, at=c, txt=s, n=0, _has=[], sorted=False,
              lo=inf, hi=-inf, w = -1 if s[-1]=="-" else 1)

def COLS(words):
  """Factory for generating summary objects. Should be called  on the row
  columns names, top of a csv file. Upper case words become NUMs, others 
  are SYMs. Goals (ending in `+-!`) are added to a `y` list and others are 
  added to `x`. Anything ending in `X` is something to ignore."""
  cols = BAG(ako=COLS, names=words, x=[], y=[], all=[], klass=None)
  for c,s in enumerate(words):
    col = (NUM if s[0].isupper() else SYM)(c,s)
    cols.all += [col]
    if s[-1] != "X":
      if s[-1]=="!": klass=col
      (cols.y if s[-1] in "-+" else cols.x).append(col)
  return cols

def DATA(src, rows=[]):
  """Factory for making a `data` object either from a csv file (if `src` is a
  file name) or copying the structure of another `data` (f `src` is a `data`).
  Optionally, the new data can be augmented with `rows`."""
  data = BAG(ako=DATA, cols=[], rows=[])
  if type(src)==str   : [adds(data, ROW(a)) for a in csv(src)]
  elif src.ako is DATA: data.cols = COLS(src.cols.names)
  [adds(data,row) for row in rows]
  return data

def ROW(a):
  "Make a row containing `cells` to store data."
  return BAG(ako=ROW, cells=a)

def BIN():
  """Create a `bin` for some column that stores rows. This is a place  to remember
  the labels seen in every row, and the `lo,hi` values seen in that column."""
  return BAG(ako=BIN, rows=[], lo=inf, hi=-inf, ys=SYM())
#------------------------------------------------ --------- --------- ----------
def adds(data,row):
  "Summarize `row` inside `data` (and  keep `row` in `data.rows`)."
  if data.cols:
    data.rows += [row]
    for col in data.cols.all: add(col,row.cells[col.at])
  else:
    data.cols = COLS(row.cells)

def add(col,x,inc=1):
  "Increment counts of symbols seen (in SYMs), or numbers kept (in NUMs)."
  if x == "?": return x
  col.n += inc
  if col.ako is SYM:
    tmp = col._has[x] = col._has.get(x,0) + inc
    if tmp > col.most: col.most,col.mode = tmp,x
  else:
    col.lo = min(x, col.lo)
    col.hi = max(x, col.hi)
    a = col._has
    if   len(a) < the.Some    : col.sorted=False; a += [x]
    elif r() < the.Some/col.n : col.sorted=False; a[int(len(a)*r())] = x

def ok(col):
  "Make the column update to date. Return the column."
  if col.ako is NUM and not col.sorted:
    col._has = sorted(col._has)
    col.sorted=True
  return col

def mid(col):
  "Return central tendency."
  return col.mode if col.ako is SYM else median(ok(col)._has)

def div(col):
  "Return diversity (tendency NOT to be at the central point)"
  return ent(col._has) if col.ako is SYM else stdev(ok(col)._has)

def stats(data, cols=None, fun=mid):
  "Return a summary of `cols` in `data`, using `fun` (defaults to `mid`)."
  tmp = {col.txt: fun(col) for col in (cols or data.cols.y)}
  tmp["N"] = len(data.rows)
  return BAG(**tmp)

def norm(num,x):
  "Normalize `x` 0..1 for min..max."
  return x if x=="?" else (x - num.lo)/(num.hi - num.lo + 1/inf)
#------------------------------------------------ --------- --------- ----------
def better(data, row1, row2):
  "`Row1` is better than `row2` if moving to it losses less than otherwise."
  s1, s2, cols, n = 0, 0, data.cols.y, len(data.cols.y)
  for col in cols:
    a, b = norm(col,row1.cells[col.at]), norm(col,row2.cells[col.at])
    s1  -= math.exp(col.w * (a - b) / n)
    s2  -= math.exp(col.w * (b - a) / n)
  return s1 / n < s2 / n

def betters(data, rows=None):
  "Divide `data` into `best` and `rest`. Returns `best` and `rest` as `datas`."
  rows = sorted(rows or data.rows,
               key = cmp_to_key(lambda r1,r2:better(data,r1,r2)))
  cut = len(rows) - int(len(rows))**the.Min
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

def like(rule, klass, freq, prior):
  f={}
  for col,bins in rule:
    f[col] = f.get(col,0) + freq.get((klass,col,bins.lo,bins.hi),0) # pre-compute?
  cols = data.cols.all
  return log(prior) + sum(math.log((f[c]+the.m*prior)/(cols[c]+the.m)) for c in f)

def freqs(best, rest, also=lambda *_:True):
  out = {}
  def remember(y,col,lo,hi): k=(y,col,lo,hi); out[k]=out.get(k,0)+1; also(col,lo,hi)
  for col in best.cols.x:
    x = lambda row: row.cells[col.at]
    rows  = [row for row in best.rows + rest.rows if x(row) != "?"]
    if col.ako is NUM:
      for bin in discretize(rows,x):
        for row in bin.rows:
          remember(row.y, col.at, bin.lo, bin.hi)
    else:
      for row in rows:
        remember(row.y,col.at, x(row), x(row))
  return out

def discretize(rows,x):
  rows  = sorted(rows,key=x)
  eps   = stdev(rows, x) * the.cohen
  small = int(len(rows) / the.bins)
  bins  = [BIN()]
  for i,row in enumerate(rows):
    now       = bins[-1]
    now.lo    = min(x(row),now.lo)
    now.hi    = max(x(row),now.hi)
    now.rows += [row]
    add(now.ys, row.y)
    if now.hi - now.lo > eps and now.ys.n > small and i < len(rows) - small:
      bins += [BIN()]
  return merges(bins)

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
  return fillInTheGaps(sorted(b4,key=lambda x:x.lo)) \
         if len(b4) == len(now) else merges(now)

def merged(col1, col2):
  col12 = deepcopy(col1)
  [add(col12,s,n) for s,n in col2._has.items()]
  if div(col12) <= (col1.n*div(col1) + col2.n*div(col2))/col12.n:
    return col12

def fillInTheGaps(a):
  a[0].lo, a[-1].hi = -inf, inf
  #print("")
  #[print(">> ",x.lo, x.hi) for x in a]
  for i in range(len(a)-1): a[i].hi = a[i+1].lo
  #for x in a: print("<< ",x.lo, x.hi) 
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
#     some = bins[:i+1]))))
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
