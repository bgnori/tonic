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

class HashTest_n2_r1(unittest.TestCase):
  def test_C_Hash_range_10(self):
    h = C_Hash([1, 0], 1)
    self.assert_(C(2, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_01(self):
    h = C_Hash([0, 1], 1)
    self.assert_(C(2, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_id(self):
    d = dict()
    self.assert_(d.get(C_Hash([1, 0], 1), None) is None)
    d[C_Hash([1, 0], 1)] = [1, 0]
    self.assert_(d.get(C_Hash([0, 1], 1), None) is None)
    d[C_Hash([0, 1], 1)] = [0, 1]
    self.assertEqual(len(d), 2)

  def test_C_RHash_soundness_10(self):
      self.assertEqual(C_RHash(1, 2, 1), tuple([1, 0]))

  def test_C_RHash_soundness_01(self):
      self.assertEqual(C_RHash(0, 2, 1), tuple([0, 1]))

class HashTest_n3_r1(unittest.TestCase):
  def test_C_Hash_range_100(self):
    h = C_Hash([1, 0, 0], 1)
    self.assert_(C(3, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_010(self):
    h = C_Hash([0, 1, 0], 1)
    self.assert_(C(3, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_001(self):
    h = C_Hash([0, 0, 1], 1)
    self.assert_(C(3, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_id(self):
    d = dict()
    self.assert_(d.get(C_Hash([1, 0, 0], 1), None) is None)
    d[C_Hash([1, 0, 0], 1)] = [1, 0, 0]
    self.assert_(d.get(C_Hash([0, 1, 0], 1), None) is None)
    d[C_Hash([0, 1, 0], 1)] = [0, 1, 0]
    self.assert_(d.get(C_Hash([0, 0, 1], 1), None) is None)
    d[C_Hash([0, 0, 1], 1)] = [0, 0, 1]
    self.assertEqual(len(d), 3)

  def test_C_RHash_soundness_100(self):
      self.assertEqual(C_RHash(2, 3, 1), tuple([1, 0, 0]))

  def test_C_RHash_soundness_010(self):
      self.assertEqual(C_RHash(1, 3, 1), tuple([0, 1, 0]))

  def test_C_RHash_soundness_001(self):
      self.assertEqual(C_RHash(0, 3, 1), tuple([0, 0, 1]))

class HashTest_n3_r2(unittest.TestCase):
  def test_C_Hash_range_110(self):
    h = C_Hash([1, 1, 0], 2)
    self.assert_(C(3, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_101(self):
    h = C_Hash([1, 0, 1], 2)
    self.assert_(C(3, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_011(self):
    h = C_Hash([0, 1, 1], 2)
    self.assert_(C(3, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_id(self):
    d = dict()
    self.assert_(d.get(C_Hash([1, 1, 0], 2), None) is None)
    d[C_Hash([1, 1, 0], 2)] = [1, 1, 0]
    self.assert_(d.get(C_Hash([1, 0, 1], 2), None) is None)
    d[C_Hash([1, 0, 1], 2)] = [1, 0, 1]
    self.assert_(d.get(C_Hash([0, 1, 1], 2), None) is None)
    d[C_Hash([0, 1, 1], 2)] = [0, 1, 1]
    self.assertEqual(len(d), 3)

  def test_C_RHash_soundness_110(self):
      self.assertEqual(C_RHash(2, 3, 2), tuple([1, 1, 0]))

  def test_C_RHash_soundness_101(self):
      self.assertEqual(C_RHash(1, 3, 2), tuple([1, 0, 1]))

  def test_C_RHash_soundness_011(self):
      self.assertEqual(C_RHash(0, 3, 2), tuple([0, 1, 1]))

class HashTest_n4_r1(unittest.TestCase):
  def test_C_Hash_range_1000(self):
    h = C_Hash([1, 0, 0, 0], 1)
    self.assert_(C(4, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0100(self):
    h = C_Hash([0, 1, 0, 0], 1)
    self.assert_(C(4, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0010(self):
    h = C_Hash([0, 0, 1, 0], 1)
    self.assert_(C(4, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0001(self):
    h = C_Hash([0, 0, 0, 1], 1)
    self.assert_(C(4, 1)> h)
    self.assert_(h>=0)

  def test_C_Hash_id(self):
    d = dict()
    self.assert_(d.get(C_Hash([1, 0, 0, 0], 1), None) is None)
    d[C_Hash([1, 0, 0, 0], 1)] = [1, 0, 0, 0]
    self.assert_(d.get(C_Hash([0, 1, 0, 0], 1), None) is None)
    d[C_Hash([0, 1, 0, 0], 1)] = [0, 1, 0, 0]
    self.assert_(d.get(C_Hash([0, 0, 1, 0], 1), None) is None)
    d[C_Hash([0, 0, 1, 0], 1)] = [0, 0, 1, 0]
    self.assert_(d.get(C_Hash([0, 0, 0, 1], 1), None) is None)
    d[C_Hash([0, 0, 0, 1], 1)] = [0, 0, 0, 1]
    self.assertEqual(len(d), 4)

  def test_C_RHash_soundness_1000(self):
      self.assertEqual(C_RHash(3, 4, 1), tuple([1, 0, 0, 0]))

  def test_C_RHash_soundness_0100(self):
      self.assertEqual(C_RHash(2, 4, 1), tuple([0, 1, 0, 0]))

  def test_C_RHash_soundness_0010(self):
      self.assertEqual(C_RHash(1, 4, 1), tuple([0, 0, 1, 0]))

  def test_C_RHash_soundness_0001(self):
      self.assertEqual(C_RHash(0, 4, 1), tuple([0, 0, 0, 1]))

class HashTest_n4_r2(unittest.TestCase):
  def test_C_Hash_range_1100(self):
    h = C_Hash([1, 1, 0, 0], 2)
    self.assert_(C(4, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_1010(self):
    h = C_Hash([1, 0, 1, 0], 2)
    self.assert_(C(4, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0110(self):
    h = C_Hash([0, 1, 1, 0], 2)
    self.assert_(C(4, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_1001(self):
    h = C_Hash([1, 0, 0, 1], 2)
    self.assert_(C(4, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0101(self):
    h = C_Hash([0, 1, 0, 1], 2)
    self.assert_(C(4, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0011(self):
    h = C_Hash([0, 0, 1, 1], 2)
    self.assert_(C(4, 2)> h)
    self.assert_(h>=0)

  def test_C_Hash_id(self):
    d = dict()
    self.assert_(d.get(C_Hash([1, 1, 0, 0], 2), None) is None)
    d[C_Hash([1, 1, 0, 0], 2)] = [1, 1, 0, 0]
    self.assert_(d.get(C_Hash([1, 0, 1, 0], 2), None) is None)
    d[C_Hash([1, 0, 1, 0], 2)] = [1, 0, 1, 0]
    self.assert_(d.get(C_Hash([0, 1, 1, 0], 2), None) is None)
    d[C_Hash([0, 1, 1, 0], 2)] = [0, 1, 1, 0]
    self.assert_(d.get(C_Hash([1, 0, 0, 1], 2), None) is None)
    d[C_Hash([1, 0, 0, 1], 2)] = [1, 0, 0, 1]
    self.assert_(d.get(C_Hash([0, 1, 0, 1], 2), None) is None)
    d[C_Hash([0, 1, 0, 1], 2)] = [0, 1, 0, 1]
    self.assert_(d.get(C_Hash([0, 0, 1, 1], 2), None) is None)
    d[C_Hash([0, 0, 1, 1], 2)] = [0, 0, 1, 1]
    self.assertEqual(len(d), 6)

  def test_C_RHash_soundness_1100(self):
      self.assertEqual(C_RHash(5, 4, 2), tuple([1, 1, 0, 0]))

  def test_C_RHash_soundness_1010(self):
      self.assertEqual(C_RHash(4, 4, 2), tuple([1, 0, 1, 0]))

  def test_C_RHash_soundness_0110(self):
      self.assertEqual(C_RHash(2, 4, 2), tuple([0, 1, 1, 0]))

  def test_C_RHash_soundness_1001(self):
      self.assertEqual(C_RHash(3, 4, 2), tuple([1, 0, 0, 1]))

  def test_C_RHash_soundness_0101(self):
      self.assertEqual(C_RHash(1, 4, 2), tuple([0, 1, 0, 1]))

  def test_C_RHash_soundness_0011(self):
      self.assertEqual(C_RHash(0, 4, 2), tuple([0, 0, 1, 1]))

class HashTest_n4_r3(unittest.TestCase):
  def test_C_Hash_range_1110(self):
    h = C_Hash([1, 1, 1, 0], 3)
    self.assert_(C(4, 3)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_1101(self):
    h = C_Hash([1, 1, 0, 1], 3)
    self.assert_(C(4, 3)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_1011(self):
    h = C_Hash([1, 0, 1, 1], 3)
    self.assert_(C(4, 3)> h)
    self.assert_(h>=0)

  def test_C_Hash_range_0111(self):
    h = C_Hash([0, 1, 1, 1], 3)
    self.assert_(C(4, 3)> h)
    self.assert_(h>=0)

  def test_C_Hash_id(self):
    d = dict()
    self.assert_(d.get(C_Hash([1, 1, 1, 0], 3), None) is None)
    d[C_Hash([1, 1, 1, 0], 3)] = [1, 1, 1, 0]
    self.assert_(d.get(C_Hash([1, 1, 0, 1], 3), None) is None)
    d[C_Hash([1, 1, 0, 1], 3)] = [1, 1, 0, 1]
    self.assert_(d.get(C_Hash([1, 0, 1, 1], 3), None) is None)
    d[C_Hash([1, 0, 1, 1], 3)] = [1, 0, 1, 1]
    self.assert_(d.get(C_Hash([0, 1, 1, 1], 3), None) is None)
    d[C_Hash([0, 1, 1, 1], 3)] = [0, 1, 1, 1]
    self.assertEqual(len(d), 4)

  def test_C_RHash_soundness_1110(self):
      self.assertEqual(C_RHash(3, 4, 3), tuple([1, 1, 1, 0]))

  def test_C_RHash_soundness_1101(self):
      self.assertEqual(C_RHash(2, 4, 3), tuple([1, 1, 0, 1]))

  def test_C_RHash_soundness_1011(self):
      self.assertEqual(C_RHash(1, 4, 3), tuple([1, 0, 1, 1]))

  def test_C_RHash_soundness_0111(self):
      self.assertEqual(C_RHash(0, 4, 3), tuple([0, 1, 1, 1]))

