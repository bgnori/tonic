#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import tonic.cache 
from tonic.cache import NotInCache

    
class Storage(tonic.cache.HashableKeyStorage):
  def __init__(self, levels, *args, **kws):
    self.levels = levels

  def bringUpFrom(self, nth, key):
    if nth > 0:
      self.levels[nth - 1].set(
          self.levels[nth].get(key),
          self.levels[nth].mtime(key)
        )
      self.bringUpFrom(nth - 1, key)

  def _mtime(self, key):
    '''
      FIXME:
        Implement entry bring up from Level n to Level m where m < n.
    '''
    for nth, storage in enumerate(self.levels):
      try:
        mtime = storage.mtime(key)
        self.bringUpFrom(nth, key)
        return mtime
      except NotInCache:
        pass
    raise NotInCache
    
  def _get(self, key, default):
    '''
      FIXME:
        Implement entry bring up from Level n to Level m where m < n.
    '''
    for nth, storage in enumerate(self.levels):
      try:
        value = storage.get(key)
        self.bringUpFrom(nth, key)
        return value
      except NotInCache:
        pass
    raise NotInCache

  def _set(self, key, value, mtime):
    '''
      write through
    '''
    self.levels[-1].set(key, value, mtime=None)
    self.get(key)# triggers bring up.

