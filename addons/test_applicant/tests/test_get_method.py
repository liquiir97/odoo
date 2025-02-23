from odoo.tests import HttpCase
from odoo import fields


class TestModelApi(HttpCase):
    
    def test_get(self):

        self.env['test.model'].create({
            'name': 'Test Record 1',
            'description': 'Description for test record 1',
            'state': 'draft'
        })
        self.env['test.model'].create({
            'name': 'Test Record 2',
            'description': 'Description for test record 2',
            'state': 'confirmed'
        })

        response = self.client.get('/test_model')

        data = response.json()

        self.assertTrue(len(data['data']), 2)
