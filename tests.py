# vim: set ts=2:sw=2:et:
from ragworm import *

seed(the.seed)
d=  DATA(the.file)
d1,fun= betters(DATA(the.file))
rules( bins(d1,fun),fun)
