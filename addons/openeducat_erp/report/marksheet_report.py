# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from datetime import datetime
from report import report_sxw

class marksheet_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(marksheet_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_lines':self.get_lines,
            'get_date': self.get_date,
            'get_total': self.get_total
        })
    
    def get_lines(self, objects):
        lines = []
        for o in objects:
            lines.extend(o.marksheet_line)
        return lines
    
    def get_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) +'/'+ str(date1.year)
    
    def get_total(self, marksheet_line):
        total = [x.total_marks for x in marksheet_line.result_line]
        return sum(total)
     

report_sxw.report_sxw('report.op.marksheet','op.marksheet.register', 'addons/openeducat_erp/report/marksheet_report.rml', parser=marksheet_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
