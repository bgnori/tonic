#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

import tonic.depot.dict

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

  def test(self):
    self.assertEqual(proxy.hoge, 'hoge')
    self.assertEqual(proxy.piyo, 'piyo')
    self.assertEqual(proxy.one, 1)
    self.assertEqual(proxy.double.child, 'this is a child')
    self.assertEqual(proxy.triple.double.child,
                     'this is a grand child')


