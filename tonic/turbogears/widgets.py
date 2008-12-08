#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#
from turbogears.widgets.forms import Form
#SelectionField

__all__ = ['HistoryListWithDiffSelection']

class HistoryListWithDiffSelection(Form):
    params = ["history"] + Form.params
    #params_doc = {'history':'changes in history'}.update(Form.params_doc)
    history = []
    def __init__(self, history=None, *args, **kw):
      super(Form, self).__init__(*args, **kw)
      if history: 
        self.history=history
      else:
        self.history=[]
      
    template = """
    <form xmlns:py="http://purl.org/kid/ns#"
        class="HistoryListWithDiffSelection"
        action="${action}" 
        method="${method}" 
     >
    <input type="submit" 
           value="show diff"
     />
    <table>
      <tr>
      <th colspan="2"> select for diff </th>
      <th rowspan="2">Editor</th>
      <th rowspan="2">modified</th>
      </tr>
      <tr>
      <th>Left</th>
      <th>Right</th>
      </tr>
      <tr py:for="change in history">
        <td>
          <input type="radio"
                id="${change.id}"
                value="${change.id}"
                name="left"
          />
        </td>
        <td>
          <input type="radio"
                id="${change.id}"
                value ="${change.id}"
                name="right"
          />
        </td>
        <td py:content="change.editor.display_name" />
        <td py:content="change.last_modified" />
        </tr>
    </table>
    </form>
    """

if __name__ == '__main__':
  from tonic.funny import LooseQuacker as ChangeMock
  from tonic.funny import LooseQuacker as UserMock
  from turbogears.view import load_engines
  load_engines()
  editor = UserMock(
               display_name='nori',
               )
  history=[
            ChangeMock(id=1,
                       last_modified='1001 10 10',
                       editor=editor,
                       after='after',
                       before='before',
                       wikiname='FrontPage',
                       ),
            ChangeMock(id=2,
                       last_modified='1111 11 11',
                       editor=editor,
                       after='after2',
                       before='before2',
                       wikiname='FrontPage',
                      ),
            ]
  hw = HistoryListWithDiffSelection(history=history)
  print hw.render()
