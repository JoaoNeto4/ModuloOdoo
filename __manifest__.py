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
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}