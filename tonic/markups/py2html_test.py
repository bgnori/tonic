#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import unittest
import os.path
import StringIO

from tonic.rlimit import Lock

from tonic.markups.w3cutil import validate
from tonic.markups.py2html import *

class python2htmlTest(unittest.TestCase):
  def setUp(self):
    p = os.path.abspath(__file__)
    self.input = file(p)
    self.output = StringIO.StringIO()

  def tearDown(self):
    self.input.close()
    self.output.close()

  def test_regexp_function(self):
    print Formatter.regexp
    print Formatter.regexp_str
    self.assert_(Formatter.regexp.match('def foo():'))
    self.assert_(Formatter.regexp.match('  def foo():'))
    self.assert_(Formatter.regexp.match('  def foo(x):'))
    self.assert_(Formatter.regexp.match('  def foo(x, y):'))

  def test_as_file(self):
    formatter = Formatter(self.input, self.output)
    formatter.html()
    s = self.output.getvalue()
    self.assert_('<html' in s)
    self.assert_('/html>' in s)

  def test_as_html(self):
    formatter = Formatter(self.input, self.output)
    formatter.html()
    self.output.seek(0)
    lock = Lock(15)
    lock.aquire()
    r = validate(self.output)
    lock.release()
    c = 0
    for line in r:
      if '''class="msg_err"''' in line:
        c = 10
      if c > 0:
        print line,
        c -= 1
    print r.info()
    self.assertEqual(r.info()['X-W3C-Validator-Status'], 'Valid')
    self.assertEqual(int(r.info()['X-W3C-Validator-Errors']), 0)

