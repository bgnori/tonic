#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tonic.depot

class CRLFProxy(tonic.depot.Proxy):
  def __repr__(self):
    return "<lines.Proxy for %s of  %s>"%(self._apth, str(self._impl))

  def _is_in_(self, x):
    if len(self._apth) > 0:
      return x in self._impl[self._apth[0]]
    else:
      return x in self._impl

  def _has_child_(self, x):
    return len(self._apth) < 1

  def _get_by_x_(self, x):
    return self._impl[self._apth[0]][x]


def Proxy(filename):
  config  = dict()
  f = file(filename)
  try:
    for line in f.readlines():
      x = line.split()
      if x:
        d = config.get(x[0], dict())
        try:
          e = (int(x[2]), int(x[3]))
        except:
          e = x[2]
        d.update({x[1]: e})
        config.update({x[0]: d})
      else:
        continue
  finally:
    f.close()

  return CRLFProxy(config, [])


