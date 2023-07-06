# -*- coding: utf-8 -*-
from odoo import _, http
from datetime import datetime
import json

# import logging
# _logger = logging.getLogger(__name__)
# Ejemplo para hacer un logger: _logger.critical("TU MENSAJE AQUI")
# Para ver los logs ejecuta por consola: docker logs -f odoo

class Fonema(http.Controller):

    #### FUNCIONES PUBLICAS ####

    @http.route('/fonema/getContactByNumber', auth='user', methods=['POST'], csrf=False)
    def getContactByNumber(self, **post):
        # 0) Actualizar la fecha de la ultima conexion.
        self.refreshInfoLastConnection('getContactByNumber')

        # 1) Poner valores por defecto.
        is_contact_found = False
        contact_name = False
        contact_link = False
        msg_error = False

        # 2) Obtener valores necesarios del POST.
        callerNumber = post.get('callerNumber') # Llamante.

        # 3) Comprobar que los valores recibidos son correctos.
        if callerNumber is None or callerNumber == "":
            msg_error = "No caller number received"
        else:
            # 3.2) Obtener el nombre del contacto.
            contact = self.auxGetContactByNumber(callerNumber)
            if contact.id == False:
                msg_error = "No contact found"
            else:
                # 3.2.1) Rellenar los valores de la respuesta.
                is_contact_found = contact.id != False
                if is_contact_found:
                    domain = http.request.httprequest.host
                    contact_link = "http://{}/web#id={}&model=res.partner&view_type=form".format(domain, contact.id)
                    contact_name = contact.name
        
        # 4) Preparar respuesta y enviarla.
        res = {
            'found': is_contact_found,
            'name': contact_name,
            'link': contact_link,
            'error': msg_error
        }
        return json.dumps(res)
    
    @http.route('/fonema/addContactCallInfo', auth='user', methods=['POST'], csrf=False)
    def addContactCallInfo(self, **post):
        # 0) Actualizar la fecha de la ultima conexion.
        self.refreshInfoLastConnection('addContactCallInfo')

        # 1) Obtener valores necesarios del POST.
        callerNumber = post.get('callerNumber') # Llamante.
        calledNumber = post.get('calledNumber') # Llamado.
        isIncomingCall = post.get('type') == 'incoming' # Tipo (entrante o saliente).
        strType = 'entrante' if isIncomingCall else 'saliente'

        # 2) Comprobar que los valores recibidos son correctos.
        if callerNumber is None or callerNumber == "":
            callerNumber = "N/A"

        if calledNumber is None or calledNumber == "":
            calledNumber = "N/A"

        # 3) Obtener el contacto por su numero de telefono y añadir un mensaje en el chatter.
        numToSearch = callerNumber if isIncomingCall else calledNumber
        contact = self.auxGetContactByNumber(numToSearch)
        if contact.id != False:
            contact.message_post(body="Llamada {} de {} a {}".format(strType, callerNumber, calledNumber))
        
        # 4) Preparar respuesta y enviarla.
        res = {
            'success': contact.id != False,
            'error':  ('Contact with number ' + callerNumber + ' not found.') if contact.id is False else False
        }
        return json.dumps(res)
        
    @http.route('/fonema/test', auth='user', methods=['POST'], csrf=False)
    def testOdoo(self):
        # 0) Actualizar la fecha de la ultima conexion.
        self.refreshInfoLastConnection('test')

        # 1) Intentar acceder a un conctacto cualquiera.
        partners = http.request.env['res.partner'].sudo()
        contact = partners.search([], limit=1)
        resp = 'ok' if contact.id is not False else "error"

        # 2) Preparar respuesta y enviarla.
        res = { 'response': resp }
        return json.dumps(res)

    #### FUNCIONES INTERNAS ####

    def auxGetContactByNumber(self, number):
        # 3.2.1) Crear una cadena de busqueda con el numero para poder encontrarlo al buscarlo en contactos.
        # Ejemplo: 6%3%0%%0%0%0%%0%0%0%
        number = number.replace(' ', '')
        number = number.replace('+', '')
        number = number.replace('-', '')
        number = number.replace('(', '')
        number = number.replace(')', '')

        strFilterNumber = '%'
        for i in range(0, len(number)):
            strFilterNumber += number[i] + '%'
            i += 1

        # 3.2.2) Buscar por el telefono, si no se encuentra nada se busca por el movil.
        # Contact es un diccionario que devuelve valores mediante una clave. Ej: contacto.email, conctacto.website, etc.
        partners = http.request.env['res.partner'].sudo()
        contact = partners.search([('phone', 'ilike', strFilterNumber)], limit=1)
        if contact.id is False:
            contact = partners.search([('mobile', 'ilike', strFilterNumber)], limit=1)
        return contact

    # Actualizar la fecha de la ultima conexion (visible desde Ajustes > Fonema).
    def refreshInfoLastConnection(self, functionName):
        http.request.env['ir.config_parameter'].sudo().set_param('fonema.info_last_connection', datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' - ' + functionName)
    