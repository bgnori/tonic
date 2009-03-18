#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

from tonic.depot.dict import Proxy

class DictTest(unittest.TestCase):
  def setUp(self):
    self.proxy = Proxy(hoge='hoge',
                       piyo='piyo',
                       one=1,
                       double=dict(
                         child='this is a child'),
                       triple=dict(
                         double=dict(
                           child='this is a grand child'),
                  )
                )
  def tearDown(self):
    pass

  def test_attr(self):
    self.assertEqual(self.proxy.hoge, 'hoge')
    self.assertEqual(self.proxy.piyo, 'piyo')
    self.assertEqual(self.proxy.one, 1)

  def test_attr_nested(self):
    self.assertEqual(self.proxy.double.child, 'this is a child')
    self.assertEqual(self.proxy.triple.double.child,
                     'this is a grand child')

  def test_repr(self):
    self.assertEqual(repr(self.proxy),
    """<dict.Proxy for [] of  {'double': {'child': 'this is a child'}, 'hoge': 'hoge', 'piyo': 'piyo', 'triple': {'double': {'child': 'this is a grand child'}}, 'one': 1}>""")


