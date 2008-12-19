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
import random

from tonic.cache import hub
from tonic.cache.imp_memcache import MemcacheTestingServer


class Perf(object):
  def __init__(self, count):
    self.count = count
    self.to_set = 0.0
    self.to_get = 0.0

  def setUp(self):
    pass
  def tearDown(self):
    pass

  def time_set(self, key, value):
    a = time.time()
    hub.set(key, value)
    b = time.time()
    return b - a
  
  def time_get(self, key):
    a = time.time()
    hub.get(key)
    b = time.time()
    return b - a
    
  def load(self):
    self.data = [(n, n) for n in range(0, self.count)]

  def shoot(self):
    for key, value in self.data:    
      self.to_set += self.time_set(key, 'X'*10**5)

    for key, value in self.data:    
      self.to_get += self.time_get(key)

  def report(self):
    print '='*10, self.__class__.__name__, '='*10
    print 'set:', self.to_set / self.count
    print 'get:', self.to_get / self.count

  def run(self):
    self.load()
    self.setUp()
    try:
      self.shoot()
    finally:
      self.tearDown()
    

class PerfMemcached(Perf):
  def setUp(self):
    IP = '127.0.0.1'
    PORT = 22222
    self.memcached = MemcacheTestingServer(IP, PORT)
    hub.connect('memcache', ['%s:%i'%(IP, PORT)])
  def tearDown(self):
    hub.purge()
    self.memcached.close()


class PerfDict(Perf):
  def setUp(self):
    hub.connect('dict')
  def tearDown(self):
    hub.purge()

class PerfDisk(Perf):
  def setUp(self):
    self.workdir = tempfile.mkdtemp()
    hub.connect('disk', self.workdir)
  def tearDown(self):
    hub.purge()
    hub.close()
    os.rmdir(self.workdir)


#hub.connect('file', workdir=tempfile.mkdtemp())

pdisk = PerfDisk(10**4)
pdisk.run()
pdisk.report()

pm = PerfMemcached(10**4)
pm.run()
pm.report()

pdict = PerfDict(10**4)
pdict.run()
pdict.report()


