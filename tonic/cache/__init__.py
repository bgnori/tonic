#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
__all__ = ['hub', 'NotInCache']

import sys
import traceback
from turbogears.decorator import weak_signature_decorator

class NotInCache(Exception):
  pass
class VirtualMethod(Exception):
  pass

class Storage(object):
  def purge(self):
    raise VirtualMethod
  def close(self):
    raise VirtualMethod
  def set(self, key, value, mtime=None):
    raise VirtualMethod
  def get(self, key, default=None):
    raise VirtualMethod
  def mtime(self, key):
    raise VirtualMethod


'''
from threading import local
serving = local()
class _ThreadLocalProxy:
  def __init__(self, attrname):
    self.__dict__["__attrname__"] = attrname

  def __getattr__(self, name):
    try:
      childobject = getattr(serving, self.__attrname__)
    except AttributeError:
      raise AttributeError(
          "cache.%s has no such property " % self.__attrname__)
    return getattr(childobject, name)

  def __setattr__(self, name, value):
    try:
      childobject = getattr(serving, self.__attrname__)
    except AttributeError:
      raise AttributeError(
          "cache.%s has no such property" % self.__attrname__)
    setattr(childobject, name, value)
hub = _ThreadLocalProxy('hub')
'''


class Hub(object):
  '''
    ToDo: multi-threading support
  '''
  def __init__(self):
    self.storage = Storage()
  def close(self):
    self.storage.close()
  def purge(self):
    self.storage.purge()
  def get(self, key):
    return self.storage.get(key)
  def mtime(self, key):
    return self.storage.mtime(key)
  def set(self, value, mtime=None):
    self.storage.set(value, mtime)
  def connect(self, storage):
    assert isinstance(storage, Storage)
    self.storage = storage


hub = Hub()


def memoize(hub, hash_proc=None):
  def entangle(func):
    def memoize(func, *args, **kws):
      if hash_proc is None:
        key = str(hash((args, tuple(kws.items()))))
      else:
        key = hash_proc(*args, **kws)
        assert isinstance(key, str)
      try:
        return hub.get(key)
      except NotInCache:
        v = func(*args, **kws)
        hub.set(key, v)
      except Exception, e:
        traceback.print_exc(file=sys.stderr)
        v = func(*args, **kws)
      return v
    return memoize
  return weak_signature_decorator(entangle)



