# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json
import base64


class TestApplicant(http.Controller):

    def _authenticate_user(self):
        
        auth_header = request.httprequest.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return None 

        encoded_credentials = auth_header.replace("Basic ", "").strip()
        
        try:
            decoded_credentials = base64.b64decode(encoded_credentials.strip()).decode("utf-8").strip()
            username, password = decoded_credentials.split(":", 1)
        except Exception:
            return None

        user = request.env['res.users'].sudo().search([('login', '=', username)], limit=1)
        
        if not user: #or not user._check_credentials({'type': 'password', 'password': password}, env):
            return None

        return user
        
    @http.route('/test_model',auth='public', methods=['GET'])
    def list(self, **kw):
        records = http.request.env['test.model'].search([])
        data = []
        for record in records:
            data.append({'reference_code' : record.reference_code,
            'name' : record.name,
            'description' : record.description,
            'state' : record.state})
        return Response(json.dumps({'data' : data}), content_type='application/json', status=200)

    @http.route('/test_model', auth='public', methods=['POST'], csrf=False)
    def add_new(self, **kw):
        user = self._authenticate_user()
        if not user:
            return Response(json.dumps({'error' : 'Invalid username/password'}), content_type='application/json', status=401)
        obj = json.loads(request.httprequest.data.decode('utf-8'))
        
        name = obj.get('name')
        description = obj.get('description')
        state = obj.get('state', 'draft')
        result = http.request.env['test.model'].sudo().create({
            'name' : name,
            'description' : description,
            'state' : state
        })
        response = {'name' : result.name, 'reference_code' : result.reference_code, 'description' : result.description, 'state' : result.state}
        return Response(json.dumps({'data' : response}), content_type='application/json', status=200)
#
# class TestApplicant(http.Controller):
#     @http.route('/test_applicant/test_applicant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_applicant/test_applicant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_applicant.listing', {
#             'root': '/test_applicant/test_applicant',
#             'objects': http.request.env['test_applicant.test_applicant'].search([]),
#         })

#     @http.route('/test_applicant/test_applicant/objects/<model("test_applicant.test_applicant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_applicant.object', {
#             'object': obj
#         })

