# -*- coding: utf-8 -*-
# from odoo import http


# class /odoo/odoo13/custom/bigBlueButton/bbbServers(http.Controller):
#     @http.route('//odoo/odoo13/custom/big_blue_button/bbb_servers//odoo/odoo13/custom/big_blue_button/bbb_servers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//odoo/odoo13/custom/big_blue_button/bbb_servers//odoo/odoo13/custom/big_blue_button/bbb_servers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/odoo/odoo13/custom/big_blue_button/bbb_servers.listing', {
#             'root': '//odoo/odoo13/custom/big_blue_button/bbb_servers//odoo/odoo13/custom/big_blue_button/bbb_servers',
#             'objects': http.request.env['/odoo/odoo13/custom/big_blue_button/bbb_servers./odoo/odoo13/custom/big_blue_button/bbb_servers'].search([]),
#         })

#     @http.route('//odoo/odoo13/custom/big_blue_button/bbb_servers//odoo/odoo13/custom/big_blue_button/bbb_servers/objects/<model("/odoo/odoo13/custom/big_blue_button/bbb_servers./odoo/odoo13/custom/big_blue_button/bbb_servers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/odoo/odoo13/custom/big_blue_button/bbb_servers.object', {
#             'object': obj
#         })
