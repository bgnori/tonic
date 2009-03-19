#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#

import unittest

import turbogears
import cherrypy
from tonic.tg.cc import *
import time
from datetime import datetime as dt
from datetime import timedelta as delta

from turbogears import controllers, testutil, expose


class Root(controllers.RootController):
  @expose()
  @expires(100.0)
  def expires(self):
    return 'expires!'

  @expose()
  @cache_control('cache_control_param')
  def cache_control(self):
    return 'cache control!'

  @expose()
  @etaginate('revistion_or_tag')
  def etaged(self):
    return 'etaged!'

  @expose()
  @etaginate(lambda x : 'dynamic-etag')
  def dynamic_etaged(self):
    return 'dynamic etaged!'

cherrypy.root = Root()


class CCTest(unittest.TestCase):
  def setUp(self):
    turbogears.startup.startTurboGears()

  def tearDown(self):
    turbogears.startup.stopTurboGears()

  def test_expires(self):
    requested = dt.utcnow()
    testutil.create_request("/expires")
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("200" in cherrypy.response.status)
    self.assert_("expires!" in  response)
    self.assert_(headers['Expires'])

    'Thu, 19 Mar 2009 01:21:34 GMT'
    generated = dt(*time.strptime(headers['Expires'],
                              '%a, %d %b %Y %H:%M:%S GMT')[:7]
                  )
    print requested
    print generated
    print generated - requested
    self.assert_(generated < requested + delta(seconds=101.0))
    self.assert_(generated > requested + delta(seconds=99.0))

  def test_cache_control(self):
    testutil.create_request("/cache_control")
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("200" in cherrypy.response.status)
    self.assert_("cache_control_param" in headers['Cache-Control'])

  def test_etaginage_none(self):
    testutil.create_request("/etaged")
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("200" in cherrypy.response.status)
    self.assert_("etaged!" in  response)
    self.assert_("revistion_or_tag" in headers['Etag'])

  def test_etaginage_if_match_fail(self):
    testutil.create_request("/etaged",
                            headers={'If-Match':'bad etag'}
                           )
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("412" in cherrypy.response.status)


  def test_etaginage_if_none_match_with_GET(self):
    testutil.create_request("/etaged",
                            headers={'If-None-Match':'*'}
                           )
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("304" in cherrypy.response.status)

  def test_etaginage_if_none_match_with_POST(self):
    testutil.create_request("/etaged",
                            method="POST",
                            headers={'If-None-Match':'*'}
                           )
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("412" in cherrypy.response.status)

  def test_etaginage_dynamic(self):
    testutil.create_request("/dynamic_etaged")
    response = cherrypy.response.body[0]
    headers = cherrypy.response.headers
    print headers
    print response
    self.assert_("200" in cherrypy.response.status)
    self.assert_("dynamic etaged!" in  response)
    self.assert_("dynamic-etag" in headers['Etag'])

