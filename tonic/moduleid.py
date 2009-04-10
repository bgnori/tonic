#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#
import os.path
import sha
import glob

def register(g):
  path = g["__file__"]
  if path.endswith("pyc") or path.endswith("pyo"):
    path = path[:-1]
  path = os.path.abspath(path)
  dir = os.path.dirname(path)
  h = sha.new()
  px = [path] 
  for n in g.get("__moduleid_deps__", []):
    x = glob.glob(os.path.join(dir, n))
    if not len(x):
      raise ValueError("Empry glob with %s %s"%(dir, n))
    px.extend(x)

  for p in px:
    f = open(p, 'r+b') 
    try:
      for read in f.read():
        h.update(read)
    finally:
      f.close()
  g.update({'__moduleid__': h.hexdigest()})

