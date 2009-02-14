#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#

import time
import cherrypy
from turbogears.decorator import weak_signature_decorator

def etaginate(etag):
  def entangle(func):
    def etaginate(func, *args, **kw):
      if callable(etag):
        etag_value = etag(*args, **kw)
      else:
        etag_value = etag
      request = cherrypy.request
      conditions = [str(x) for x in (request.headers.elements('If-Match') or [])]
      if conditions and not (conditions == ["*"] or etag_value in conditions):
        raise cherrypy.HTTPError(412, "If-Match failed: ETag %r did not match %r"
                                       % (etag_value, conditions))
      conditions = [str(x) for x in (request.headers.elements('If-None-Match') or [])]
      if conditions == ["*"] or etag_value in conditions:
        if request.method in ("GET", "HEAD"):
          raise cherrypy.HTTPRedirect([], 304)
        else:
          raise cherrypy.HTTPError(412, "If-None-Match failed: ETag %r matched %r"
                                        % (etag_value, conditions))
      cherrypy.response.headers['ETag'] = etag_value
      return func(*args, **kw)
    return etaginate
  return weak_signature_decorator(entangle)


def expires(delta_second):
  def entangle(func):
    def expires(func, *args, **kw):
      assert isinstance(delta_second, (float, int))
      cherrypy.response.headers["Expires"] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time()+ delta_second))
      return func(*args, **kw)
    return expires 
  return weak_signature_decorator(entangle)


def cache_control(*param):
  def entangle(func):
    def cache_control(func, *args, **kw):
      cherrypy.response.headers["Cache-Control"] = ','.join(param)
      return func(*args, **kw)
    return cache_control
  return weak_signature_decorator(entangle)

