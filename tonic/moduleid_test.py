#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#
import unittest
import StringIO

from tonic.moduleid import *


class TestRegister(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass
  def test_register(self):
    g = globals()
    register(g)
    self.assert_('__moduleid__' in g)

  def test_deps(self):
    g = globals()
    g.update({"__moduleid_deps__": ['tonic/moduleid_test.py']})
    register(g)
    self.assert_('__moduleid__' in g)
    
