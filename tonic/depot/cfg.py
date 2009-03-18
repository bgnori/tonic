#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import ConfigParser

import tonic.depot

class CFGProxy(tonic.depot.Proxy):
  def __repr__(self):
    return "<cfg.Proxy for %s of  %s>"%(self._apth, str(self._impl))

  def _is_in_(self, x):
    #print 'cfg.Proxy._is_in_', self._apth, x
    if self._apth:
      return self._impl.has_option(self._apth[0], x)
    else:
      return x in self._impl.sections()

  def _has_child_(self, x):
    return not bool(self._apth)

  def _get_by_x_(self, x):
    return self._impl.get(self._apth[0], x)

  def _set_by_x_(self, x, value):
    self._impl.set(self._apth[0], x, value)

  def __iter__(self):
    assert len(self._apth) in (0, 1)
    if not self._apth:
      for section in self._impl.sections():
        yield self[section]
    else:
      section = self._apth[0]
      for option in self._impl.options(section):
        yield self._impl.get(section, option)


def Proxy(filenames):
  config = ConfigParser.SafeConfigParser()
  config.read(filenames)
  return CFGProxy(config, [])
