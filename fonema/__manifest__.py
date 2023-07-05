# -*- coding: utf-8 -*-
{
    'name': "Fonema",

    'summary': """
        Módulo para integrar Odoo con la centralita de Fonema.
    """,

    'description': """
        Es necesario tener una cuenta en Fonema para poder utilizar este módulo.
        Este módulo permite: obtener el nombre de los contactos al realizar una llamada con el servicio de Fonema, almacenar en el chatter o historial de un contacto las llamadas realizadas y recibidas por el mismo (opcional). Si se tiene la extensión de Chrome instalada se podrá acceder a la ficha del cliente tanto al descolgar una llamada que figure como contacto en Odoo y al llamar a este.
        Funciona para Odoo 15 y 16.
    """,

    'author': "Monema",
    'website': "https://www.monema.es/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Telecomunicaciones',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'bus'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],
    # Controladores del modulo (el que recibe las peticiones de fuera).
    'controllers': [
        'controllers/controllers.py',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'images': ['static/description/main_screenshot.png'],
}
