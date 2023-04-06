from lib import *

the=O(cohen=.35, file="../data/auto93.csv")

def COL(c,s):
   if s[0].isupper:
     w = -1 if s[-1]=="-" else 1
     return O(at=c,txt=s,n=0,w=w,nums=[],sorted=True, isNum=True) 
   else:
     return O(at=c,txt=s,n=0,syms={}, isNum=False)

def add(col,x):
  if x == "?" then return
  col.n += 1
  if col.isNum:
    col.syms[x] += get(col.syms,x,0) + 1
  else:
    col.nums += [x]
    col.sorted= False

def has(num):
  if not col.sorted(num): sorted(num.nums)

def COLS(a):
  names, x, y, all = a, [], [], [COL(c,s) for c,s in enumerate(a)]
  return O(x = [col for col in all if col.txt[-1] not in "X1"]
           y = [col for col in all if col.txt[-1]     in "1"]
           all=all, names=a)

def DATA(file):
  cols, rows = [],[]
  for a in csv(ile):
    if not cols:
       cols = COLS(a)
     else:
       rows += [a]
       for cols in [cols.x, cols.y]:
         [add(col, a[col.at] for col in cols]
  return O(rows=rows, cols=cols)

def sorts(data):
  for col in data.cols:
    x=lambda row: row.cells[col.at]
    a = sorted(data.rows, key=x)
    sd  = le

