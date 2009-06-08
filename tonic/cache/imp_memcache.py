#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
'''
memcache is not available in py3k yet.

import time
import memcache


import subprocess
import tempfile
import os
import signal
import re

import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.StringKeyStorage):
  def __init__(self, *args, **kws):
    self.client = memcache.Client(*args, **kws)

  def hash(self, key):
    return str(hash(key))

  def purge(self):
    self.client.flush_all()
    #print dir(self.client)

  def close(self):
    pass

  def _set(self, key, value, mtime):
    if mtime is None:
      mtime = time.time()
    self.client.set(self.hash(key), (value, mtime))

  def _get(self, key):
    v = self.client.get(self.hash(key))
    if v:
      return v[0]
    raise NotInCache

  def mtime(self, key):
    v = self.client.get(self.hash(key))
    if v:
      return v[1]
    raise NotInCache


class MemcacheTestingServer(object):
  def __init__(self, ip, port, memory=None):
    if memory is None:
      self.s = '/usr/bin/memcached -l %s -p %i'%(ip, port)
    else:
      self.s = '/usr/bin/memcached -l %s -p %i -m %i'%(ip, port, memory)
    r = re.compile(self.s)
    subprocess.call(
        [self.s+' &'],
        shell=True)

    buf = tempfile.TemporaryFile()
    p = subprocess.call(
        ['ps -ef | grep memcached'],
        stdout=buf,
        shell=True)
    buf.seek(0)
    for line in buf:
      if r.search(line):
        self.pid = int(line.split()[1])
    buf.close()

  def close(self):
    os.kill(self.pid, signal.SIGKILL)


'''
