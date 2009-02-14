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
  assert n >= 0
  if n == 0:
    return 1
  elif n == 1:
    return 1
  elif n > 1:
    return n*fact(n-1)
  else:
    assert False

def C(n, r):
  assert n >= 0
  assert r >= 0
  if n > r:
    return fact(n)/(fact(r) * fact(n-r))
  elif r > n:
    return fact(r)/(fact(n) * fact(r-n))
  elif n == r:
    return 1
  else:
    assert False

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
    assert xs[i] in (1, 0)
    if xs[i]:
      hash += C(n, r)
      r-=1
    i+=1
    n-=1
  return hash


_r_hash = Hub()
_r_hash.connect(Dict())
@memoize(_r_hash)
def C_RHash(h, n, r):
  '''Reverse function of C_Hash.
    Parameters are hash value h, and n, r of C(n, r)
    retuns xs
  '''
  assert n >= r
  assert r >= 0
  xs = list()
  for i in range(n, 0, -1):
    if h >= C(i - 1, r):
      xs.append(1)
      h -= C(i - 1, r)
      r -= 1
    else:
      xs.append(0)
  return tuple(xs)

if __name__ == '__main__':
  import sys
  for r in range(10):
    for n in range(r, 20, 1):
      sys.stdout.write('.')
      for i in range(C(n, r)):
        assert i == C_Hash(C_RHash(i, n, r), r)

