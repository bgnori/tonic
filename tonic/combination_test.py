#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import unittest

from tonic.combination import *

def sum(xs):
  s = 0
  for n in xs:
    s +=n
  return s


class HashTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def hash1_test(self):
    xs = [1, 0, 1, 0, 0]
    self.assertEqual(C_Hash(xs, r=2), 8)

  def hash2_test(self):
    xs = [0, 0, 0, 1, 1]
    self.assertEqual(C_Hash(xs, r=2), 0)

  def hash3_test(self):
    self.assertEqual(C_RHash(8, 5, 2), (1, 0, 1, 0, 0))

  def hash4_test(self):
    self.assertNotEqual(C_RHash(0, 5, 2), (0, 0, 0, 0, 0))

  def hash5_test(self):
    for i in range(C(5, 2)):
      generated = C_RHash(i, 5, 2)
      expected = C_RHash_naive(i, 5, 2)
      print generated
      #self.assertEqual(sum(generated), 2)
      self.assertEqual(generated, expected)

  def hash6_test(self):
    for i in range(2**5):
      xs = [i & 1 << mask and 1 or 0 for mask in range(5)]
      if sum(xs) == 2:
        h = C_Hash(xs, 2)
        print h
        print xs
        self.assertEqual(C_RHash(h, 5, 2), tuple(xs))






