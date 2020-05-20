# -*- coding: utf-8 -*-
# from odoo import http


# class /odoo/odoo13/custom/bigBlueButton/bbbMeeting(http.Controller):
#     @http.route('//odoo/odoo13/custom/big_blue_button/bbb_meeting//odoo/odoo13/custom/big_blue_button/bbb_meeting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//odoo/odoo13/custom/big_blue_button/bbb_meeting//odoo/odoo13/custom/big_blue_button/bbb_meeting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/odoo/odoo13/custom/big_blue_button/bbb_meeting.listing', {
#             'root': '//odoo/odoo13/custom/big_blue_button/bbb_meeting//odoo/odoo13/custom/big_blue_button/bbb_meeting',
#             'objects': http.request.env['/odoo/odoo13/custom/big_blue_button/bbb_meeting./odoo/odoo13/custom/big_blue_button/bbb_meeting'].search([]),
#         })

#     @http.route('//odoo/odoo13/custom/big_blue_button/bbb_meeting//odoo/odoo13/custom/big_blue_button/bbb_meeting/objects/<model("/odoo/odoo13/custom/big_blue_button/bbb_meeting./odoo/odoo13/custom/big_blue_button/bbb_meeting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/odoo/odoo13/custom/big_blue_button/bbb_meeting.object', {
#             'object': obj
#         })
