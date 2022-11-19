{
    'name': 'Modulo Teste',
    'summary': 'Teste de aplicativo',
    'version': '1.0.2',
    'sequence': 1,
    'author': 'João',
    'depends': [
        'base', 'web'
        ],
    'data': [
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}