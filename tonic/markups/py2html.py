#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# 2-clause BSD license
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import sys
import os.path
from htmlentitydefs import entitydefs

_d = dict([(value, '&'+key+';') for key, value in entitydefs.items()])

def escape(s):
  return ''.join([_d.get(c, c) for c in s])

def resource(name):
  if not name.startswith(os.path.sep):
    name = os.path.join(os.path.split(
                      os.path.abspath(__file__))[0], name)
  f = file(name, 'rb')
  try:
    return f.read(-1)
  finally:
    f.close()

class Formatter(object):
  css_src = resource('python.css')
  def __init__(self, instream, outstream):
    self.instream = instream
    self.outstream = outstream

  def write(self, s):
    return self.outstream.write(s)
  def flush(self):
    self.outstream.flush()

  def name(self):
    return self.instream.name
    
  def css(self):
    self.write(self.css_src)

  def style(self):
    self.write('''<style type="text/css"><!--\n''')
    self.css()
    self.write('''--></style>\n''')

  def codeblock(self):
    self.write('<pre class="codeblock">')
    for line in self.instream:
      self.write('<code>' + escape(line.strip('\n')) + '</code>\n')
    self.write('</pre>')

  def doctype(self):
    self.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
  def html(self):
    self.doctype()
    self.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
    self.write('<head><title>%s</title>\n'%self.name())
    self.style()
    self.write('</head>\n')
    self.write('<body>\n')
    self.codeblock()
    self.write('</body>')
    self.write('</html>\n')
    self.flush()

if __name__ == '__main__':
  assert len(sys.argv) > 1
  f = file(sys.argv[1])
  formatter = Formatter(f, sys.stdout)
  try:
    formatter.html()
  finally:
    f.close()

