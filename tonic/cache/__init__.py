#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
__all__ = ['hub', 'NotInCache']

from turbogears.decorator import weak_signature_decorator

from threading import local
serving = local()

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


def load(name, *args, **kws):
    modname = 'imp_' + name
    g = globals()
    exec 'import ' + modname in g
    return g[modname].Storage(*args, **kws)

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
  def connect(self, name, *args, **kws):
    self.storage = load(name, *args, **kws)


hub = Hub()


def memoize(hub):
  def entangle(func):
    def memoize(func, *args, **kws):
      return func(*args, **kws)
    return memoize
  return weak_signature_decorator(entangle)


