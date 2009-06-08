#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2009 Noriyuki Hosaka bgnori@gmail.com
#
import os.path
import hashlib
import glob

def register(g):
  path = g["__file__"]
  if path.endswith("pyc") or path.endswith("pyo"):
    path = path[:-1]
  path = os.path.abspath(path)
  basedir = g.get("__moduleid_basedir__")
  if basedir is None:
    basedir = os.path.dirname(path)
  h = hashlib.sha1()
  px = [path] 
  for n in g.get("__moduleid_deps__", []):
    x = glob.glob(os.path.join(basedir, n))
    if not len(x):
      raise ValueError("Empry glob with %s %s"%(basedir, n))
    px.extend(x)

  for p in px:
    f = open(p, 'rb') 
    assert f
    try:
      for read in f:
        h.update(read)
    finally:
      f.close()
  g.update({'__moduleid__': h.hexdigest()})

