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
  else:
    assert n > 1
    return n*fact(n-1)


def C(n, r):
  assert n > 0
  assert r > 0
  if n > r:
    return fact(n)/(fact(r) * fact(n-r))
  elif r > n:
    return fact(r)/(fact(n) * fact(r-n))
  else:
    assert n == r
    return 1


def C_Hash(xs, r):
  '''Bijection from combinatorial sequence to integer, such as
    i,e for C(5, 2),
    given xs = (1, 0, 1, 0, 0) , have 8.
  '''
  assert hasattr(xs, '__getitem__')
  assert r >= 0
  hash = 0
  n = len(xs) - 1
  i = 0
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
  assert n >= r
  assert r >= 0
  if n == r:
    return tuple([1 for i in range(n)])
  if r == 0:
    return tuple([0 for i in range(n)])
  if h >= C(n-1, r):
    return (1, ) + C_RHash(h - C(n-1, r), n-1, r-1)
  else:
    return (0, ) + C_RHash(h, n-1, r)

