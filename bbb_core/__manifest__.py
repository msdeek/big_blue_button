# -*- coding: utf-8 -*-
{
    'name': "BigBlueButton",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "codefish",
    'website': "https://www.codefish.com.eg",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'version': '13.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website_slides'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/server.xml',
        'views/meeting.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
