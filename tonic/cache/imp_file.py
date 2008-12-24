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

  def _path(self, path):
    assert os.path.exists(self.workdir)
    assert os.path.exists(path)
    return os.path.join(self.workdir, path[1:]) 
    #remove /
    #FIXME:  it works only on UNIX.

  def mtime(self, path):
    p = self._path(path)
    if not os.path.exists(p):
      raise NotInCache
    return os.path.getmtime(p)

  def get(self, path):
    p = self._path(path)
    if not os.path.exists(p):
      raise NotInCache
    f = file(p, 'r')
    try:
      return pickle.load(f)
    finally:
      f.close()

  def set(self, path, value, mtime=None):
    p = self._path(path)
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

