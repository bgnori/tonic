#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#


import unittest
from tonic.isbn import *

class ISBN10Test(unittest.TestCase):
  def test_cls_isvalid_foobar(self):
    self.assertFalse(ISBN10.isvalid('foobar'))
  def test_cls_isvalid_4101092052(self):
    self.assert_(ISBN10.isvalid('4101092052'))
  def test_cls_isvalid_4101092053(self):
    self.assertFalse(ISBN10.isvalid('4101092053'))
  def test_cls_bad_new_None(self):
    try:
      ISBN10('abcdefg')
      assert False
    except ValueError:
      pass
  def test_cls_bad_new_4101092053(self):
    try:
      ISBN10('4101092053')
      assert False
    except ValueError:
      pass
  def test_hash(self):
    isbn = ISBN10('4101092052')
    hash(isbn)
    d = {}
    d[isbn] = 0


class ISBN13Test(unittest.TestCase):
  def test_cls_isvalid_foobar(self):
    self.assertFalse(ISBN13.isvalid('foobar'))
  def test_cls_isvalid_9784101092058(self):
    self.assert_(ISBN13.isvalid('9784101092058'))
  def test_cls_isvalid_9784101092057(self):
    self.assertFalse(ISBN13.isvalid('9784101092057'))
  def test_cls_bad_new_None(self):
    try:
      ISBN13('abcdefg')
      assert False
    except ValueError:
      pass
  def test_cls_bad_new_9784101092057(self):
      try:
        ISBN13('9784101092057')
        assert False
      except ValueError:
        pass

  def test_hash(self):
    isbn = ISBN13('9784101092058')
    hash(isbn)
    d = {}
    d[isbn] = 0

  def convert_test(self):
    x = ISBN10('4101092052')
    y = convert(x)
    self.assertEqual(y.value, '978410109205')

