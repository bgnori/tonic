#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import time
import memcache


import subprocess
import tempfile
import os
import signal
import re

import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.Storage):
  def __init__(self, *args, **kws):
    self.client = memcache.Client(*args, **kws)

  def hash(self, key):
    return str(hash(key))

  def purge(self):
    pass

  def close(self):
    pass

  def set(self, key, value, mtime=None):
    if mtime is None:
      mtime = time.time()
    self.client.set(self.hash(key), (value, mtime))

  def get(self, key):
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
  def __init__(self, ip, port):
    self.s = '/usr/bin/memcached -l %s -p %i -m 2048'%(ip, port)
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


