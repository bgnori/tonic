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

from tonic.cache import hub, load, memoize
from tonic.cache.imp_memcache import MemcacheTestingServer

class DictTest(unittest.TestCase):
  def setUp(self):
    os.stat_float_times(True)
    hub.connect('dict')

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
    hub.connect('memcache', ['%s:%i'%(ip, port)])
    
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
    hub.connect('disk', workdir=tempfile.mkdtemp())

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
    hub.connect('file', workdir=tempfile.mkdtemp())

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
    hub.connect(name='hierachy',
        levels=[
         load('dict'),
         load('dict')
        ])

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
    hub.connect('dict')

  def tearDown(self):
    pass

  def testNoneProc(self):
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

  def testProc(self):
    def proc(n, *args, **kws):
      return n
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





