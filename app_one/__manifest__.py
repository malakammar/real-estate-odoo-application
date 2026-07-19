{
    'name': 'App One',
    'author': 'Malak Amamr',
    'version': '17.0.0.1.0',
    'category': 'Real Estate',

    'depends': [
        'base',
        'mail',
        # 'sale_management',
        # 'account_accountant',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',

        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/building_view.xml',

        'reports/property_report.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}