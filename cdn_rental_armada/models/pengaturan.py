from odoo import _, api, fields, models



class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    
    jangka_waktu = fields.Integer(string='Jangka Waktu', config_parameter="cdn_rental_armada.jangka_waktu")
 
