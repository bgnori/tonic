#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

from tonic.combination import *

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
''')
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

for n in range(5):
  for r in range(1, n):
    makeTestCase(n, r)

