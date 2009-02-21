#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import StringIO
import unittest

from tonic.html.w3cutil import *

MINIMAL = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head><title>unittest</title></head>
<body>empty</body></html>
'''
class w3cvalidateTest(unittest.TestCase):
  def setUp(self):
    self.html = StringIO.StringIO(MINIMAL)
  def tearDown(self):
    pass

  def test(self):
    r = validate(self.html)
    c = 0
    for line in r:
      if '''class="msg_err"''' in line:
        c = 10
      if c > 0:
        print line,
        c -= 1
    print r.info()
    self.assertEqual(r.info()['X-W3C-Validator-Status'], 'Valid')


