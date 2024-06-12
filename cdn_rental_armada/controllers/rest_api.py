# -*- coding: utf-8 -*-
from odoo import http
import traceback
from odoo.http import Response, request
from odoo.loglevels import ustr
import sys
import json
from datetime import date


# http://localhost:8069/pembayaran/invoice

# CREATED BY RIZKI
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

