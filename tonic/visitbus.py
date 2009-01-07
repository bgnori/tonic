#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
__all__ = ['VisitBus', 'VisitPassenger']
import re
from tonic.cache import hub, memoize


@memoize(hub, lambda x: x)
def vpath2regexp(vpath):
  assert isinstance(vpath, str)
  assert vpath.startswith('/')
  if vpath.endswith('<'):
    direction = '<'
    vpath = vpath[:-1]
  elif vpath.endswith('>'):
    direction = '>'
    vpath = vpath[:-1]
  else:
    '''defulat'''
    direction = '>'

  p = []
  for i, n in enumerate(vpath.split('/')):
    if i == 0:
      assert n == ''
      p.append('^')
    elif not n:
      p.append('((/[a-zA-Z][a-zA-Z0-9]*)*)')
    elif n == '*':
      p.append('(/[a-zA-Z][a-zA-Z0-9]*)')
    else:
      assert re.compile(n)
      p.append('/('+n+')')

  p = ''.join(p) + direction + '$'
  return re.compile(p)


def path2vpath(stack, direction):
  if direction == 'down':
    return '/' + '/'.join([node.tag for node in stack]) + '>'
  elif direction == 'up':
    return '/' + '/'.join([node.tag for node in stack]) + '<'
  else:
    assert False

class Requests(object):
  def __init__(self, *args):
    self._imp = dict(*args)

  def _append(self, dest, p):
    rs = self._imp.get(dest, [])
    assert isinstance(rs, list)
    rs.append(p)
    self._imp.update({dest: rs})

  def next(self, p, stack, matchobj, visitbus):
    assert isinstance(p, VisitPassenger)
    p.setresult(stack, matchobj, visitbus)
    try:
      dest = p.next()
      self._append(dest, p)
    except StopIteration:
      pass 

  def remove(self, dest):
    del self._imp[dest]

  def match(self, vpath):
    '''
      remark: SRE object is hashable.
    '''
    for dest in self._imp:
      match = getattr(dest, 'match', None)
      if match:
        mo = match(vpath)
        if mo:
          yield dest, mo
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
    self.requests = Requests()
    for p in passengers:
      self.requests.next(p, self.stack[:], None, self)
    # Every body get in, it is starting point

  def unload(self, getoff):
    for dest, matchobj in getoff:
      self.requests.remove(dest)

  def wicket(self, xs):
    r = Requests()
    for dest, matchobj in xs:
      for p in self.requests[dest]:
        assert isinstance(p, VisitPassenger)
        r.next(p, self.stack[:], matchobj, self)
        for c in p.spawn():
          r.next(c, self.stack[:], matchobj, self)
    return r

  def load(self, requests):
    self.requests = merge(self.requests, requests)

  def match(self, vpath):
    return self.requests.match(vpath)

  def dispatch(self, direction):
    wokeup = list(self.match(path2vpath(self.stack, direction)))
    r = self.wicket(wokeup)
    self.unload(wokeup)
    self.load(r)

  def visit(self, node):
    self.stack.append(node)
    self.dispatch('down')
    for n in node:
      self.visit(n)
    self.dispatch('up')
    self.stack.pop()


class VisitPassenger(object):
  def __init__(self):
    self.result = None
    self.match = None
    self.visitbus = None
    try:
      self._itinerary = self.itinerary()
    except StopIteration:
      self._itinerary = None

  def next(self):
    if self._itinerary is None:
      raise StopIteration
    try:
      t = self._itinerary.next()
      #vpath2regexp(t)
      assert hasattr(t, 'match')
      return t
    except StopIteration:
      self._itinerary = None
      raise

  def setresult(self, stack, matchobj, visitbus):
    self.result = stack
    self.match = matchobj
    self.visitbus = visitbus

  def spawn(self):
    return []

  def getresult(self):
    return self.result

  def __iter__(self):
    return self

  def itinerary(self):
    raise StopIteration

