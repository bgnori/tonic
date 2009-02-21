#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import sys
import os.path
import ClientForm
import StringIO
from urllib2 import urlopen

def validate(f):
  res = urlopen('http://validator.w3.org/#validate_by_upload')
  forms = ClientForm.ParseResponse(res, backwards_compat=False)
  form = forms[1]
  form.add_file(f,
                content_type='text/xml; charset=us-ascii',
                name='uploaded_file', filename='test.xml')
  req = form.click()
  return urlopen(req)

if __name__ == '__main__':
  assert len(sys.argv) > 1
  f = file(sys.argv[1])
  try:
    res = validate(f)
  finally:
    f.close()
  print res.info()['X-W3C-Validator-Status']
  if int(res.info()['X-W3C-Validator-Errors']) > 0:
    c = 0
    for line in res:
      if '''class="msg_err"''' in line:
        c = 10
      if c > 0:
        print line,
        c -= 1

