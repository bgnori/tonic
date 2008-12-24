#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.Storage):
  def __init__(self, *args, **kws):
    pass

  def purge(self):
    pass
  def close(self):
    pass
  def get(self, path):
    raise NotInCache

  def mtime(self, path):
    raise NotInCache

  def set(self, path, value, mtime=None):
    pass

