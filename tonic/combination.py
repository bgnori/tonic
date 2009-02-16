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
  assert n >0
  assert r >0
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



def C_RHash_naive(h, n, r):
  '''Reverse function of C_Hash.
    Parameters are hash value h, and n, r of C(n, r)
    retuns xs

    this provides very naive implementation
  '''
  for i in range(2**n):
    xs = [i & 1 << mask and 1 or 0 for mask in range(n)]
    if sum(xs) == r:
      if h == C_Hash(xs, r):
        return tuple(xs)

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


if __name__ == '__main__':
  ''' unittest generator '''
  print ('''\
#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
# DO NOT EDIT. THIS FILE IS PROGRAM GENERATED.
#

import unittest

from tonic.combination import *
'''
  )
  def sum(xs):
    s = 0
    for n in xs:
      s +=n
    return s

  def makeTestCase(n, r):
    print '''\
class HashTest_n%i_r%i(unittest.TestCase):'''%(n, r)
    for i in range(2**n):
      xs = [i & 1 << mask and 1 or 0 for mask in range(n)] 
      if sum(xs) == r:
        print '''\
  def test_C_Hash_range_%s(self):'''%(''.join(['%i'%x for x in xs]))
        print '''\
      h = C_Hash(%s, %i)'''%(xs, r)
        print '''\
      self.assert_(C(%i, %i)> h)'''%(n, r)
        print '''\
      self.assert_(h>=0)'''
        print

    print '''\
  def test_C_Hash_id(self):'''
    print '''\
    d = dict()'''
    for i in range(2**n):
      xs = [i & 1 << mask and 1 or 0 for mask in range(n)] 
      if sum(xs) == r:
        print '''\
    self.assert_(d.get(C_Hash(%s, %i), None) is None)'''%(xs, r)
        print '''\
    d[C_Hash(%s, %i)] = %s'''%(xs, r, xs)
    print '''\
    self.assertEqual(len(d), %i)'''%(C(n, r))
    print

    for i in range(2**n):
      xs = [i & 1 << mask and 1 or 0 for mask in range(n)] 
      if sum(xs) == r:
        print '''\
  def test_C_RHash_soundness_%s(self):'''%(''.join(['%i'%x for x in xs]))
        print '''\
      self.assertEqual(C_RHash(%i, %i, %i), tuple(%s))'''%(C_Hash(xs, r), n, r, xs)
        print

  for n in range(12):
    for r in range(1, n):
      makeTestCase(n, r)

