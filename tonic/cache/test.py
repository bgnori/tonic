#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import sys
import os
import time
import tempfile

import unittest

from tonic.cache import hub, memoize, NotInCache
from tonic.cache.imp import *
from tonic.cache.imp_memcache import MemcacheTestingServer

class NullTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect(Null())

  def tearDown(self):
    pass
    
  def test_HelloWorld(self):
    hw = 'Hello World!'
    hub.set('test1', hw)
    now = time.time()
    try:
      mtime = hub.mtime('test1')
      self.assert_(False)
    except NotInCache:
      pass
    try:
      value = hub.get('test1')
      self.assert_(False)
    except NotInCache:
      pass


class DictTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect(Dict())

  def tearDown(self):
    pass
    
  def test_HelloWorld(self):
    hw = 'Hello World!'
    hub.set('test1', hw)
    now = time.time()
    mtime = hub.mtime('test1')
    value = hub.get('test1')
    self.assert_(now - mtime < 1.0) #disk acess is so slow.
    self.assertEqual(value, hw)


class MemcacheTestingServerTest(unittest.TestCase):
  def testA(self):
    ip = '127.0.0.1'
    port = 22222
    self.server = MemcacheTestingServer(ip, port)
    self.assertEqual(self.server.s , 
          '/usr/bin/memcached -l 127.0.0.1 -p 22222')
    self.server.close()

  def testB(self):
    ip = '127.0.0.1'
    port = 22222
    self.server = MemcacheTestingServer(ip, port, memory=2048)
    self.assertEqual(self.server.s , 
          '/usr/bin/memcached -l 127.0.0.1 -p 22222 -m 2048')
    self.server.close()


class MemcacheTest(unittest.TestCase):
  def setUp(self):
    ip = '127.0.0.1'
    port = 22222
    self.server = MemcacheTestingServer(ip, port)
    hub.connect(Memcache(['%s:%i'%(ip, port)]))
    
  def tearDown(self):
    hub.purge()
    hub.close()
    self.server.close()

  def test_HelloWorld(self):
    hw = 'Hello World!'
    hub.set('test1', hw)
    value = hub.get('test1')
    mtime = hub.mtime('test1')
    now = time.time()
    self.assertAlmostEqual(now, mtime, 2)
    self.assertEqual(value, hw)


class DiskTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect(Disk(workdir=tempfile.mkdtemp()))

  def tearDown(self):
    pass
    
  def test_HelloWorld(self):
    hw = 'Hello World!'
    hub.set('test1', hw)
    now = time.time()
    mtime = hub.mtime('test1')
    value = hub.get('test1')
    self.assert_(now - mtime < 1.0) #disk acess is so slow.
    self.assertEqual(value, hw)


class FileTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect(File(workdir=tempfile.mkdtemp()))

  def tearDown(self):
    pass
    
  def test_HelloWorld(self):
    hw = 'Hello World!'
    hub.set('README', hw)
    now = time.time()
    mtime = hub.mtime('README')
    value = hub.get('README')
    self.assert_(now - mtime < 1.0) #disk acess is so slow.
    self.assertEqual(value, hw)


class HierachyTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect(Hierachy(levels=[Dict(),Dict()]))

  def tearDown(self):
    pass
    
  def test_HelloWorld(self):
    hw = 'Hello World!'
    hub.set('test1', hw)
    now = time.time()
    mtime = hub.mtime('test1')
    value = hub.get('test1')
    self.assert_(now - mtime < 1.0) 
    self.assertEqual(value, hw)


class MemoizeTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect(Dict())

  def tearDown(self):
    pass

  def testOne(self):
    @memoize(hub)
    def fact(n):
      if n == 0:
        return 1
      elif n == 1:
        return 1
      else:
        return fact(n-1)*n
    nocache = fact(10)
    cached = fact(10)
    self.assertEqual(nocache, cached)

  def testPreheat(self):
    @memoize(hub, preheat_range=[((i,), {}) for i in range(1000)])
    def fact(n):
      if n == 0:
        return 1
      elif n == 1:
        return 1
      else:
        return fact(n-1)*n
    fact(1024)

  def testHashProc(self):
    def proc(n, *args, **kws):
      return str(n)
    @memoize(hub, hash_proc=proc)
    def fact(n):
      if n == 0:
        return 1
      elif n == 1:
        return 1
      else:
        return fact(n-1)*n
    nocache = fact(10)
    cached = fact(10)
    self.assertEqual(nocache, cached)

