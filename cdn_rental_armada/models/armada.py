from odoo import _, api, fields, models


#adi
class CdnArmada(models.Model):
    _name = 'cdn.armada'
    _description = 'Cdn Armada'

    merek_id = fields.Many2one(comodel_name='cdn.merek', string='merek kendaraan',required=True)
    jenis_kendaraan = fields.Many2one(comodel_name='cdn.jenis.kendaraan', string='Jenis kendaraan',required=True,domain="[('merek_id', '=', merek_id)]")
    jumlah_kursi = fields.Integer(string='Jumlah Kursi', required=True)
    jenis_armada = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
    tahun_pembuatan = fields.Date(string='Tahun Pembuatan', required=True)
    no_plat = fields.Char(string='Plat Nomor', required=True)
    no_mesin = fields.Char(string='No Rangka & No Mesin',required=True)
    kondisi = fields.Boolean(string='Kondisi Armada', default="True")
    
    def name_get(self):
        return [(record.id, "[ %s ] %s %s" % (record.jenis_armada, record.merek_id.name, record.jenis_kendaraan.name)) for record in self]
    
    @api.model
    def create(self, vals):
        if 'jenis_kendaraan' in vals and isinstance(vals['jenis_kendaraan'], str):
            jenis_kendaraan_name = vals['jenis_kendaraan']
            merek_id = vals.get('merek_id')
            jenis_kendaraan = self.env['cdn.jenis.kendaraan'].create({
                'name': jenis_kendaraan_name,
                'merek_id': merek_id,
            })
            vals['jenis_kendaraan'] = jenis_kendaraan.id
        return super(CdnArmada, self).create(vals)