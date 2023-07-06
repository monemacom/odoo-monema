# -*- coding: utf-8 -*-

from odoo import api, models, fields

# Los datos se almacenan en Ajustes > Tecnico > Parámetros del sistema > Busca por Fonema.
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def get_version(self):
        module = self.env['ir.module.module'].search([('name', '=', 'fonema')])
        return module.installed_version if module else 'N/A'

    # Datos a almacenar.
    info_last_connection = fields.Char(string="Información sobre la última conexión", config_parameter='fonema.info_last_connection', required=False)
    info_version = fields.Char(string="Versión del módulo", default=get_version, required=False)

    def btn_help(self):
        return {
            "url": "https://www.monema.es/knowledge-base/como-configurar-odoo-con-fonema/",
            "type": "ir.actions.act_url"
        }
    
    
