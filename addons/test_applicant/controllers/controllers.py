# -*- coding: utf-8 -*-
# from odoo import http


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

