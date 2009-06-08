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


class Storage(tonic.cache.StringKeyStorage):
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
    assert os.path.isabs(self.workdir)
    return os.path.join(self.workdir, str(hash(key)))

  def _set(self, key, value, mtime):
    f = open(self._path(key), 'w+b')
    try:
      pickle.dump(value, f)
    finally:
      f.close()
    if mtime is not None:
      os.utime(self._path(key), (mtime, mtime))
  
  def _get(self, key):
    p = self._path(key)
    if not os.path.exists(p):
      raise NotInCache
    f = open(p, 'r+b')
    try:
      return pickle.load(f)
    finally:
      f.close()

  def _mtime(self, key):
    assert os.path.exists(self.workdir)
    p = self._path(key)
    if not os.path.exists(p):
      raise NotInCache
    return os.path.getmtime(p)

