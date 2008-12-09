#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
from tonic.lineparser import EMPTY, LineParser

class MetaClassTest(unittest.TestCase):
  def test_metaclass(self):
    class A(LineParser):
      _first = '(first)'
      _last = '(last)'
    self.assertEqual(A.regexp_str, '''(first)|($^)|($^)|(last)''')

class ParserTest(unittest.TestCase):
  def setUp(self):
    class A(LineParser):
      _first = '(?P<first>first)'
      _last = '(?P<last>last)'
      def handle_first(self, match, matchobj):
        return True
      def handle_last(self, match, matchobj):
        return True
    self.p = A()
  def tearDown(self):
    pass

  def test_parse(self):
    p = self.p
    self.assert_(p.parse('first'))
    self.assert_(p.parse('last'))
    self.assert_(not p.parse('not'))

