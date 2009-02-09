#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import time
import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.HashableKeyStorage):
  def __init__(self, *args, **kws):
    self.d = dict(**kws)

  def purge(self):
    self.d = dict()

  def close(self):
    pass
  
  def _get(self, key, default):
    v = self.d.get(key)
    if v is None:
      if default is None:
        raise NotInCache
      else:
        return default
    return v[0]
  
  def _mtime(self, key):
    v = self.d.get(key)
    if v is None:
      raise NotInCache
    return self.d.get(key)[1]

  def _set(self, key, value, mtime):
    if mtime is None:
      mtime = time.time()
    self.d[key] = value, mtime

