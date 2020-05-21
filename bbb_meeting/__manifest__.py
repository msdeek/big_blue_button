# -*- coding: utf-8 -*-
#################################################################################
# Author      : codefish (<https://www.codefish.com.eg/>)
# Copyright(c): 2015-Present codefish.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://codefish.com.eg/>
#################################################################################
{
    'name': "BigBlueButton Online Meeting",

    'summary': """
        Engage Your Online Partners, BigBlueButton Meeting Module is a 
        web conferencing system designed for online meetings.""",

    'description': """
        Engage Your Online Partners, BigBlueButton Meeting Module is a web conferencing system designed for online meetings
    """,

    'author': "codefish",
    'website': "https://www.codefish.com.eg",


    'category': 'Tools',
    'version': '13.0.2',
    'images': ['static/description/banner.gif'],

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bbb_servers_views.xml',
        'views/bbb_meeting.xml',
        'views/bbb_records.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    "installable": True,
    "price": 20.0,
    "currency": "EUR",
}
