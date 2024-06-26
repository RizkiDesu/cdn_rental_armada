from odoo import _, api, fields, models
from datetime import date
from dateutil import relativedelta
import logging

_logger = logging.getLogger(__name__)

# CREATED BY TRIADI
# ------------------------------- PERAWATAN ARMADA ATAU SERVICE --------------------------------
class CdnService(models.Model):
    _name           = 'cdn.service'
    _description    = 'Service'
    _rec_name       = 'tanggal'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    
    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True)
    tanggal         = fields.Date(string='Tanggal service', tracking=True)
    jenis_service   = fields.Char(string='Jenis Perawatan', tracking=True)
    harga           = fields.Integer(string='Pengeluran', tracking=True)
    deskripsi       = fields.Text(string='Deskripsi', tracking=True)
    

    # @api.model
    # def create(self, vals):
    #     record      = super(CdnService, self).create(vals)
    #     hari_ini    = date.today()
    #     if 'tanggal' in vals:    
    #         jangka_waktu = self.env['ir.config_parameter'].get_param('cdn_rental_armada.jangka_waktu')
    #         hari_batal_wajar = hari_ini - relativedelta.relativedelta(days=int(jangka_waktu))
    #         tgl     = fields.Date.from_string(vals['tanggal'])
    #         cek     = self.env['cdn.armada'].search([('id', '=', record.armada_id.id)])
    #         if hari_batal_wajar < tgl:
    #             cek.state       = 'siap'
    #             cek.kondisi     = True
    #         else :
    #             cek.state       = 'tidak_siap'
    #             cek.kondisi     = False
    #     return record


# CREATED BY RIZKI
# ------------------------------- UJI KIR --------------------------------
class CdnUjiKir(models.Model):
    _name           = 'cdn.uji.kir'
    _description    = 'Cdn Uji Kir'
    _rec_name       = 'tanggal_berakhir'
    _inherit        = ['mail.thread', 'mail.activity.mixin']

    foto_uji        = fields.Image('Foto Uji Kir', tracking=True)
    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True)
    tanggal         = fields.Date(string='Tanggal Uji Kir', tracking=True)
    tanggal_berakhir = fields.Date(string='Berlaku Sampai', tracking=True)
    deskripsi       = fields.Text(string='Deskripsi', tracking=True)


