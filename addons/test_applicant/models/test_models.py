# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)
class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'
    _rec_name = 'reference_code'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    
    reference_code = fields.Char(string='Reference Code', compute='_compute_reference_code', store=True, readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='State', default='draft')

    confirm_datetime = fields.Datetime(string='Confirmed Date', readonly=True, copy=False)

    @api.model
    def create(self, vals_list):
        record = super(TestModel, self).create(vals_list)
        if not record.reference_code:
            record._compute_reference_code()
        return record

    @api.depends('reference_code')
    def _compute_reference_code(self):
        
        today_midnight = datetime.combine(datetime.today(), datetime.min.time())
        for record in self:
            max_ref = None
            data = self.env['test.model'].search([('create_date', '>=', today_midnight)], order='id desc')
            if len(data) > 1:
                last_ref = data[1].reference_code.split('-')[1]
                max_ref = int(last_ref)
            else:
                max_ref = 0
            next_number = max_ref + 1 if max_ref else 1
            record.reference_code = f"TEST-{next_number:04d}"

    def action_confirm(self):
        if(self.state == 'draft'):
            self.state = 'confirmed'
            self.confirm_datetime = fields.Datetime.now()
    
    @api.model
    def mark_confirm(self):
        datetime_query = datetime.now() - timedelta(minutes=30)
        records = self.env['test.model'].search([
            ('state', '=', 'confirmed'),
            ('confirm_datetime', '<=', datetime_query)
        ])
        records.write({'state': 'done'})
# class test_applicant(models.Model):
#     _name = 'test_applicant.test_applicant'
#     _description = 'test_applicant.test_applicant'


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

