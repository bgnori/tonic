#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import re
from tonic.cache import hub, memoize


@memoize(hub, lambda x: x)
def compile(xpath):
  assert xpath.startswith('/')

  p = []
  for i, n in enumerate(xpath.split('/')):
    if i == 0:
      assert n == ''
      p.append('^')
    elif not n:
      p.append('((/[a-zA-Z]+)*)')
    else:
      p.append('/'+n)

  p = ''.join(p)
  return re.compile(p)


def path2xpath(stack):
  return '/' + '/'.join([node.tag for node in stack])


class Requests(object):
  def __init__(self, *args):
    self._imp = dict(*args)

  def append(self, dest, p):
    rs = self._imp.get(dest, [])
    rs.append(p)
    self._imp.update({dest: rs})

  def match(self, xpath):
    '''
      remark: SRE object is hashable.
    '''
    for dest in self._imp:
      match = getattr(dest, 'match', None)
      if match and match(xpath):
        yield dest
      else:
        pass

  def __getitem__(self, dest):
    return self._imp[dest]

  def __contains__(self, dest):
    return dest in self._imp
    
  def get(self, dest, default=None):
    if default is not None and dest not in self._imp:
      src = default
    else:
      src = self._imp[dest]
    for r in src:
      yield r

  def pop(self, dest):
    self._imp.pop(dest)

  def keys(self):
    return self._imp.keys()

def merge(a, b):
  return Requests([
      (dest, list(a.get(dest, [])) + list(b.get(dest, [])))
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
      requests.append(dest, p)
    return requests

  def dispatch(self):
    for passengers in self.requests.match(path2xpath(self.stack)):
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
    self.result = None
    self._itinerary = self.itinerary()

  def next(self):
    return self._itinerary.next()

  def __iter__(self):
    return self

  def itinerary(self):
    raise StopIteration

