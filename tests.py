# vim: set ts=2:sw=2:et:
from ragworm import *
funs=[]
def go(fun): global funs; funs += [fun]; return fun

@go
def thed():
  "show options"
  print(str(the)[:30],"... ",end="")

@go
def csvd():
  "read csv"
  return 3192==sum((len(a) for a in csv(the.file)))

@go
def lohid():
  "find num ranges"
  num = NUM()
  [add(num,x) for x in range(20)]
  return 0==num.lo and 19==num.hi

@go
def cache():
  "keep some nums"
  the.nums=16
  num = NUM()
  [add(num,x) for x in range(10**4)]
  has = ok(num).has
  return 16==len(has) and  has[0] <= has[4] <= has[8] <= has[12] <= has[-1]

@go
def numd():
  "collect stats"
  num = NUM()
  [add(num,r()) for x in range(10**4)]
  return the.nums==256 and .28 < div(num) < .32 and .46 < mid(num) < .54

#@go
def symd():
  sym = SYM()
  [add(sym,c) for c in "aaaabbc"]
  return 1.37 < div(sym) < 1.38 and mid(sym)=='a'

#@go
def statd():
  d=  DATA(the.file)
  print(d.cols.y[1])
  d1,fun= betters(DATA(the.file))
  s0  = stats(d0); a0 = s0.__dict__['Acc+']
  return  15.5 < a0 < 15.6

cli(the)
sys.exit(runs(the,funs))
