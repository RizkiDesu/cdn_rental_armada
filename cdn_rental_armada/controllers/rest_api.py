# -*- coding: utf-8 -*-
from odoo import http
import traceback
from odoo.http import Response, request
from odoo.loglevels import ustr
import requests
import sys
import json
from datetime import date
from requests.structures import CaseInsensitiveDict


# http://localhost:8069/pembayaran/invoice

# CREATED BY IAN
# MODIF BY RIZKI
# ------------------------------ KIRIM KE API PEMBAYARAN ---------------------------------------------
class pembayaran(http.Controller):
    @http.route('/pembayaran/invoice', type='http', auth='public', website=False, methods=['POST', 'GET'], csrf=False, cors='*')
    def tes(self, **kwargs):
        try:
            i_param   = request.get_json_data()
            i_va      = i_param['virtual_account']
            i_amount  = i_param['amount']
            i_date    = i_param['date']
            i_kp      = i_param['kode_pengesahan']
            datarow             = {
            'is_success'    : True,
            'code'          : 200,
            'va'            : i_va,
            'amount'        : i_amount,
            'date'          : i_date,
            'kode_p'        : i_kp,
            }
            
            # ------------------------------ MEMBUAT PEMBAYARAN BERDASARKAN INVOICE ---------------------------------------------
            invoice_id = request.env['account.move'].sudo().search([('name', '=', datarow['va'])])
            payment = request.env['account.payment'].sudo().create({
                'partner_id': invoice_id.partner_id.id,  # ID of the partner
                'amount': datarow['amount'],
                'date': datarow['date'],
            })
            payment.action_post()
        
            # action_data = invoice.action_register_payment()
            # invoice.payment_by_id = action_data['context']['default_journal_id'] = request.env.user.company_id.account_journal_id.id
            # wizard = Form(request.env['account.payment.register'].with_context(action_data['context'])).save()
            # action = wizard.action_create_payments()
            # # invoice.write({'payment_state': 'paid'})
            # success_invoice_payment.append(invoice)

        except Exception as e:
            traceback.print_exception(*sys.exc_info()) 
            datarow['is_success']   = ustr(e)
            datarow['code']         = 201
        finally:
            body = json.dumps(datarow)
            return Response(
                body, 
                status  = 200, 
                headers = [
                    ('Content-Type', 'application/json'), 
                    ('Content-Length', len(body))
                ]
            )


class gpsTracking(http.Controller):
    @http.route('/gpstrack', type='http', auth='public', website=False, methods=['GET'], csrf=False, cors='*')
    def gpstrack(self, **kwargs):
        # https://myprojects.geoapify.com/api/IeEMCUIaLGtrabHWJLu6/keys
        # https://www.geoapify.com/
        api_key = 'df672c8ae9854f32908a565119bfef15'
        lat     = kwargs.get('latitude')
        long    = kwargs.get('longitude')
        
        url = "https://api.geoapify.com/v1/geocode/reverse?lat="+lat+"&lon="+long+"&apiKey="+api_key+""

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        response =  requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return json.dumps(data)
        else:
            return {'status': 'error', 'message': 'API request failed'}

class wilayah(http.Controller):
    @http.route('/provinsi-api', type='http', auth='public', website=False, methods=['GET'], csrf=False, cors='*')
    def provinsiApi(self, **kwargs):
        url = "https://www.emsifa.com/api-wilayah-indonesia/api/provinces.json"

        headers = {'Content-Type'  : 'application/json'}

        result = requests.get(url, headers=headers)
        return json.dumps(result.json())
        # return json.dumps([{'id': province.id, 'name': province.name} for province in result.json()])

    @http.route('/kota-api', type='http', auth='public', website=False, methods=['GET'], csrf=False, cors='*')
    def kotaApi(self, **kwargs):
        provinsi_id = kwargs.get('provinsi_id')
        url = "https://www.emsifa.com/api-wilayah-indonesia/api/regencies/"+provinsi_id+".json"

        headers = {'Content-Type'  : 'application/json'}

        result = requests.get(url, headers=headers)
        return json.dumps(result.json())
    
    @http.route('/kecamatan-api', type='http', auth='public', website=False, methods=['GET'], csrf=False, cors='*')
    def kecamatanApi(self, **kwargs):
        kota_id = kwargs.get('kota_id')
        url = "https://www.emsifa.com/api-wilayah-indonesia/api/districts/"+kota_id+".json"

        headers = {'Content-Type'  : 'application/json'}

        result = requests.get(url, headers=headers)
        return json.dumps(result.json())

    @http.route('/desa-api', type='http', auth='public', website=False, methods=['GET'], csrf=False, cors='*')
    def desaApi(self, **kwargs):
        kecamatan_id = kwargs.get('kecamatan_id')
        url = "https://www.emsifa.com/api-wilayah-indonesia/api/villages/"+kecamatan_id+".json"

        headers = {'Content-Type'  : 'application/json'}

        result = requests.get(url, headers=headers)
        return json.dumps(result.json())
