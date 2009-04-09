#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import unittest
from tonic.lastmodified import *

class Test(unittest.TestCase):
  def test_getid_ok(self):
    s = getid('VERSION')
    print s
    assert isinstance(s, str)

  def test_getid_files(self):
    v = getid('VERSION')
    s = getid('setup.py')
    print s
    print v
    assert v != s

  def test_getid_file_not_under_control_of_git(self):
    try:
      getid('hogehoge')
      assert False
    except:
      pass

  def test_mergedid_single(self):
    s = mergedid('VERSION')
    print s
    assert isinstance(s, str)

  def test_mergedid_two(self):
    s = mergedid('VERSION', 'setup.py')
    print s
    assert isinstance(s, str)

  def test_mergedid_mismatch(self):
    s1 = mergedid('VERSION')
    s2 = mergedid('VERSION', 'setup.py')
    assert s1 != s2

  def test_onMANIFEST(self):
    s = onMANIFEST()
    print s
    assert isinstance(s, str)


