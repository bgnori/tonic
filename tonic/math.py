#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
from tonic.cache import memoize
from tonic.cache import Hub
from tonic.cache.imp import Dict

_fact = Hub()
_fact.connect(Dict())

PRECALC_FACT = 1000

@memoize(_fact, preheat_range=[((i,), {}) for i in range(PRECALC_FACT)])
def fact(n):
  if n == 0:
    return 1
  elif n == 1:
    return 1
  else:
    return fact(n-1)*n

def C(n, r):
  return fact(n)/(fact(r) * fact(n-r))


def C_Hash(xs, r):
  '''Bijection from combinatorial sequence to integer, such as
    i,e for C(5, 2),
    given xs = (1, 0, 1, 0, 0) , have 8.
  '''
  assert hasattr(xs, '__getitem__')
  n = len(xs) - 1
  i = 0
  hash = 0
  while n >= r and r > 0:
    if xs[i]:
      hash += C(n, r)
      r-=1
    i+=1
    n-=1
  return hash

def C_RHash(h, n, r):
  '''Reverse function of C_Hash.
    Parameters are hash value h, and n, r of C(n, r)
    retuns xs
  '''
  xs = list()
  for i in range(n, 0, -1):
    if h >= C(i - 1, r):
      xs.append(1)
      h -= C(i - 1, r)
      r -= 1
    else:
      xs.append(0)
  return tuple(xs)

