# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api
from odoo.exceptions import UserError

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

    @api.model
    def create(self, vals):
        # Ensure unique reference code is generated
        record = super(TestModel, self).create(vals)
        if not record.reference_code:
            record._compute_reference_code()
        return record

    @api.depends('reference_code')
    def _compute_reference_code(self):

        for record in self:
            # Get the next available number
            max_id = self.env['test.model'].search([], order='id desc', limit=1)
            next_number = max_id.id + 1 if max_id else 1
            record.reference_code = f"TEST-{next_number:04d}"

    def action_confirm(self):
        if(self.state == 'draft'):
            self.state = 'confirmed'
    

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

