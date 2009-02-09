#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

import tonic.cache 
from tonic.cache import NotInCache

class Storage(tonic.cache.HashableKeyStorage):
  def __init__(self, *args, **kws):
    pass

  def purge(self):
    pass

  def close(self):
    pass

  def _get(self, key, default):
    raise NotInCache

  def _mtime(self, key):
    raise NotInCache

  def _set(self, key, value, mtime=None):
    pass

