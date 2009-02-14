#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import unittest

from tonic.math import fact, C, C_Hash, C_RHash

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

