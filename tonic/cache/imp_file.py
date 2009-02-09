#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import os
import os.path
import pickle
import shutil
import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.Storage):
  def __init__(self, workdir, *args, **kws):
    assert os.path.isabs(workdir)
    assert os.path.exists(workdir)
    self.workdir = workdir

  def purge(self):
    shutil.rmtree(self.workdir, ignore_errors=True)
    os.mkdir(self.workdir)

  def close(self):
    pass

  def _path(self, key):
    assert os.path.exists(self.workdir)
    assert os.path.exists(key)
    return os.path.join(self.workdir, key[1:]) 
    #remove /
    #FIXME:  it works only on UNIX.

  def _mtime(self, key):
    p = self._path(key)
    if not os.path.exists(p):
      raise NotInCache
    return os.path.getmtime(p)

  def _get(self, key, default):
    p = self._path(key)
    if not os.path.exists(p):
      if default is None:
        raise NotInCache
      else:
        return default
    f = file(p, 'r')
    try:
      return pickle.load(f)
    finally:
      f.close()

  def _set(self, key, value, mtime):
    p = self._path(key)
    try:
      os.makedirs(os.path.dirname(p))
    except OSError:
      pass
    f = file(p, 'w')
    try:
      pickle.dump(value, f)
    finally:
      f.close()
    if mtime:
      os.utime(mtime, mtime)

