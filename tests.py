# vim: set ts=2:sw=2:et:
from ragworm import *

egs=[]
def eg(fun): global egs; egs += [fun]; return fun

@eg
def thed():
  "show options"
  print(str(the)[:30],"... ",end="")

@eg
def csvd():
  "read csv"
  return 3192==sum((len(a) for a in csv(the.file)))

@eg
def lohid():
  "find num ranges"
  num = NUM()
  [add(num,x) for x in range(20)]
  return 0==num.lo and 19==num.hi

@eg
def cache():
  "keep some nums"
  the.nums=16
  num = NUM()
  [add(num,x) for x in range(10**4)]
  has = ok(num)._has
  return 16==len(has) and has[0] <= has[4] <= has[8] <= has[12] <= has[-1]

@eg
def numd():
  "collect numeric stats"
  num = NUM()
  [add(num,r()) for x in range(10**4)]
  return the.nums==256 and .28 < div(num) < .32 and .46 < mid(num) < .54

@eg
def symd():
  "collect symbolic stats"
  sym = SYM()
  [add(sym,c) for c in "aaaabbc"]
  return 1.37 < div(sym) < 1.38 and mid(sym)=='a'

@eg
def statd():
  "collect stats from data"
  data0 = DATA("../data/auto93.csv")
  data1,data2 = betters(data0)
  s0 = stats(data0)
  s1 = stats(data1)
  s2 = stats(data2)
  a,l,m="Acc+", "Lbs-", "Mpg+"
  print(s2[m],s0[m],s1[m])
  return s1[a] > s2[a] and s1[m] >   s2[m] and s1[l] < s2[l] and \
         s0[a] > s2[a] and s0[m] >=  s2[m] and s0[l] < s2[l]

if __name__ == '__main__':
  sys.exit(runs(cli(the),egs))
