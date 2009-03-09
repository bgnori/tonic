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

from tonic.lineparser import LineParser

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

class Formatter(LineParser):
  css_src = resource('python.css')
  _first = (r'(?P<function>(\A *def +'
            r'(?P<func_name>(\w+))'
            r'\((?P<func_args>[^)]*)\):))'
            )
  def __init__(self, instream, outstream):
    super(Formatter, self).__init__()
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

  def handle_function(self, match, matchobj):
    rest = match.strip()
    self.write('<code>')
    self.write(' '*(len(match) - len(rest)))
    self.write('<span class="python-def">def</span>')
    assert rest.startswith('def ')
    rest = rest[4:]
    d = matchobj.groupdict()
    self.write('<span class="python-func-name">')
    self.write(d['func_name'])
    self.write('</span>(')
    args = d.get('func_args', None)
    if args:
      self.write(escape(args))
    self.write('):')
    self.write('</code>\n')
    return True
    
  def codeblock(self):
    self.write('<pre class="codeblock">')
    for line in self.instream:
      if not self.parse(line):
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

