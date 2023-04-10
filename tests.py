# vim: set ts=2:sw=2:et:
from ragworm import *
import traceback
from copy import deepcopy
from termcolor import colored

funs=[]
def go(fun): global funs; funs += [fun]; return fun

@go
def thed(): 
  "print options"
  print(the)

@go
def csvd():
  "read csv"
  n=0
  for a in csv(the.file): n += len(a)
  return n==3192

@go
def lohid():
  "find num ranges"
  num = NUM() 
  [add(num,x) for x in range(20)]
  return 0==num.lo and 19==num.hi

@go
def reservoir():
  "keep some nums"
  the.nums=16
  num = NUM() 
  [add(num,x) for x in range(10**4)]
  print(ok(num).has)

@go
def numd():
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

#------------------------------------------------------
def yell(s,c): 
  print(colored(s,"light_"+c,attrs=["bold"]),end="")

def isWanted(f)
  return f.__name__ == the.go or the.go=="all":

def run(f):
  global the
  name,doc=f.__name__ or "fun", f.__doc__ or "do it"
  seed(the.seed)
  yell(name+" ","yellow")
  cache = deepcopy(the)
  try:
    assert f() != False
    yell("PASS\n","green")
  except:
    print(traceback.format_exc())
    yell("FAIL can't "+doc+"\n","red")
  for k,v in cache.items(): the[k] = v

cli(the)
[run(fun) for fun in funs if isWanted(fun)]
