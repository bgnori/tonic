#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import os.path
import time

class Lock(object):
  def __init__(self, duration, path=None):
    self._duration = duration
    if path is None:
      path = 'tonic.xxx'
    self._path = os.path.abspath(path)

  def _write(self):
    f = file(self._path, 'w')
    until = time.time() + self._duration
    f.write('%f'% until)
    f.close()
    return until

  def _read(self):
    f = file(self._path, 'r')
    expires = float(f.read(-1))
    f.close()
    return expires

  def _clean(self):
    os.remove(self._path)

  def aquire(self):
    try:
      expires = self._read()
    except IOError:
      self._write()
      return
    now = time.time()
    if expires < now:
      self._write()
    else:
      time.sleep(expires - now)

  def release(self):
    if self._read() < time.time():
      self._clean()


