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
  has = ok(num)._has
  return 16==len(has) and  has[0] <= has[4] <= has[8] <= has[12] <= has[-1]

@go
def numd():
  "collect numeric stats"
  num = NUM()
  [add(num,r()) for x in range(10**4)]
  return the.nums==256 and .28 < div(num) < .32 and .46 < mid(num) < .54

@go
def symd():
  "collect symbolic stats"
  sym = SYM()
  [add(sym,c) for c in "aaaabbc"]
  return 1.37 < div(sym) < 1.38 and mid(sym)=='a'

@go
def statd():
  "collect stats from data"
  d0= DATA(the.file)
  d1,d2= betters(d0)
  s0=stats(d0)
  s1=stats(d1)
  s2=stats(d2)
  a,l,m="Acc+", "Lbs-", "Mpg+"
  return s1[a] > s2[a] and s1[m] >   s2[m] and s1[l] < s2[l] and \
         s0[a] > s2[a] and s0[m] >=  s2[m] and s0[l] < s2[l]


cli(the)
sys.exit(runs(the,funs))
