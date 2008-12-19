#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import time
import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.Storage):
  def __init__(self, *args, **kws):
    self.d = dict(**kws)

  def purge(self):
    self.d = dict()

  def close(self):
    pass
  
  def get(self, path):
    v = self.d.get(path)
    if v is None:
      raise NotInCache
    return v[0]
  
  def mtime(self, path):
    v = self.d.get(path)
    if v is None:
      raise NotInCache
    return self.d.get(path)[1]

  def set(self, path, value, mtime=None):
    if mtime is None:
      mtime = time.time()
    self.d[path] = value, mtime

