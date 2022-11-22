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
        'views/estate_property/tree.xml',
        'views/estate_property/search.xml',
        'views/estate_property/form.xml',

        'views/estate_property_tag/tree.xml',
        'views/estate_property_type/tree.xml',
        'views/estate_property_offer/form.xml',
        'views/estate_property_offer/tree.xml',
        'views/res_user/form.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}