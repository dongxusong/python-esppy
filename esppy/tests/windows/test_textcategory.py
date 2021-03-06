#!/usr/bin/env python
# encoding: utf-8
#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# NOTE: This test requires a running ESP server.  You must use an ~/.authinfo
#       file to specify your username and password.  The ESP host and port must
#       be specified using the ESPHOST and ESPPORT environment variables.
#       A specific protocol ('http' or 'https') can be set using
#       the ESPPROTOCOL environment variable.

import os
import unittest
import esppy
from . import utils as tm


class TestTextCategoryWindow(tm.WindowTestCase):

    @unittest.skip('Need mco file')
    def test_xml(self):
        self._test_model_file('textcategory_window.xml')

    @unittest.skip('Need mco file')
    def test_api(self):
        esp = self.s

        proj = esp.create_project('project_01_UnitTest', pubsub='auto', n_threads='4')

        cq = esp.ContinuousQuery(name='cq_01',
                                 trace='sourceWindow_01 textCategoryWindow')

        src = esp.SourceWindow(name='src_win',
                               schema=('ID*:int32','tstamp:date','msg:string'),
                               pubsub=True, collapse_updates=True)
        src.add_connector('fs',
                          conn_name='pub', conn_type='publish',
                          type='pub',
                          fstype='csv',
                          fsname='textcategory_window.csv',
                          dateformat='%Y-%m-%d %H:%M:%S')

        textCategory_win = esp.TextCategoryWindow(name='textCategoryWindow',
                                                  index_type='empty',
                                                  pubsub=True,
                                                  collapse_updates=True,
                                                  mco_file='@HOME@/mcoFile/IPTC.mco',
                                                  text_field='msg')
        textCategory_win.add_connector('fs',
                                       conn_name='sub', conn_type='subscribe',
                                       type='sub',
                                       fstype='csv',
                                       fsname='result.out',
                                       snapshot=True)

        proj.add_query(cq)
        cq.add_windows(src, textCategory_win)

        src.add_target(textCategory_win)

        self._test_model_file('textcategory_window.xml', proj)
