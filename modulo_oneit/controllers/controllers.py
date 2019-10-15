# -*- coding: utf-8 -*-
from odoo import http

# class Oneit(http.Controller):
#     @http.route('/oneit/oneit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oneit/oneit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('oneit.listing', {
#             'root': '/oneit/oneit',
#             'objects': http.request.env['oneit.oneit'].search([]),
#         })

#     @http.route('/oneit/oneit/objects/<model("oneit.oneit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oneit.object', {
#             'object': obj
#         })