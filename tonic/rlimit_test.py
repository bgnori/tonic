#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# 2-clause BSD license
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import time
import unittest

from tonic.rlimit import *

class LockTest(unittest.TestCase):
  def setUp(self):
    self.lock = Lock(10)

  def tearDown(self):
    try:
      os.remove(self.lock._path)
    except:
      pass

  def test_basic(self):
    t = time.time()
    self.lock.aquire()
    self.lock.release()

  def test_1(self):
    t = time.time()
    self.lock.aquire()
    self.lock.release()

    self.lock.aquire()
    s = time.time()
    print t, s
    self.assert_(t + 1 < s)
    self.lock.release()

