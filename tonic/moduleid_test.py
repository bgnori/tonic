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
    g = dict(globals())
    register(g)
    self.assert_('__moduleid__' in g)

  def test_deps(self):
    g = dict(globals())
    g.update({"__moduleid_deps__": ['moduleid_test.py']})
    register(g)
    self.assert_('__moduleid__' in g)
    
  def test_glob_nonemty(self):
    g = dict(globals())
    g.update({"__moduleid_deps__": ['../*.py']})
    register(g)
    self.assert_('__moduleid__' in g)
    

  def test_glob_empty(self):
    g = dict(globals())
    g.update({"__moduleid_deps__": ['foobar/*.py']})
    try:
      register(g)
      self.assert_(False)
    except ValueError:
      pass

  def test_glob_basedir(self):
    g = dict(globals())
    g.update({"__moduleid_deps__": ['*.py']})
    g.update({"__moduleid_basedir__": '/usr/lib/python2.4/site-packages/'})
    register(g)
    self.assert_('__moduleid__' in g)

