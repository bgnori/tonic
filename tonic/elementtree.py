#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#


class Requests(object):
  def __init__(self, *args, **kws):
    self._imp = dict(*args, **kws)

  def update(self, dest, p):
    r = self._imp.get(dest, None)
    r.append(p)
    self._imp.update({dest: r})

  def match(self, path):
    for key in self._imp:
      if key.match(path):
        yield key, self._imp[key]

def merge(a, b):
  return Requests([
      (dest, a.get(dest, []) + b.get(dest, []))
        for dest in set(a.keys() + b.keys())
      ])


class VisitBus(object):
  def __init__(self, passengers):
    self.stack = []
    self.requests = self.dropin(passengers)
    # Every body get in, it is starting point

  def dropin(self, passengers):
    requests = dict()
    for p in passengers:
      p.setresult(self.stack[:])
      try:
        dest = p.next()
      except StopIteration:
        continue
      update(requests, dest, p)
    return requests

  def dispatch(self):
    for dest, passengers in self.requests.match(self.stack[:]):
      requests = self.dropin(passengers)
    self.requests = merge(self.requests, requests)

  def visit(self, node):
    self.stack.append(node)
    self.dispatch()
    for n in node:
      self.visit(node)
    self.stack.pop()


class VisitPassenger(object):
  def __init__(self):
    self. = None
    self._itinerary = self.itinerary()

  def next(self):
    return self._itinerary.next()

  def __iter__(self):
    return self

  def itinerary(self):
    raise StopIteration

