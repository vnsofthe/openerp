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
from osv import osv
from report import report_sxw
from openeducat_erp import utils
import pooler

class op_student(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context={}):
        self.ctx = {}
        self.ctx = context.copy()
        super(op_student, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'render_image': self.render_image,
            'qr_data':self.qr_data,
            'get_obj': self.get_obj,
            'get_address':self.get_address,
        })

    def get_obj(self):
        student_list = []
        for student in pooler.get_pool(self.cr.dbname).get(self.ctx.get('active_model',False)).browse(self.cr, self.uid, self.ctx['active_ids']):
            student_list.append(student)
        return student_list

    def render_image(self,barcode):
        barcode = utils.get_barcode_image(value=barcode, code='QR')
        return barcode

    def get_address(self,student):
        student_data = {}
        address = student.street and student.street[0] or False
        addr = {
                'street': student.street or '',
                'street2': student.street2 or '',
                'city': student.city or '',
                'zip': student.zip or '',
                'phone': student.phone or '',
                'email': student.email or '',
                }
        print "__________ADDR___________",addr
        return [addr]

    def qr_data(self,student):
        student_data = {}
        address = student.street and student.street[0] or False
        student_data = {
                        'name': student.name + ' ' + student.middle_name + ' ' + student.last_name,
                        'roll_number': student.roll_number or '',
                        'blood_group': student.blood_group or '',
                        'course': student.course_id.name,
                        'birth_date': student.birth_date or '',
                        'address': '%s %s %s %s %s %s'%(student.street or '',
                                                        student.street2 or '',
                                                        student.city or '',
                                                        student.zip or '',
                                                        student.phone or '',
                                                        student.email or '',
                                                        )    
                        }
        print "_______________student_data__________________",student_data
        qr = utils.get_barcode_image(value=student_data, code='QR')
        return qr
report_sxw.report_sxw('report.op.student.report','op.student', 'addons/openeducat_erp/report/id_card.rml', parser=op_student, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
