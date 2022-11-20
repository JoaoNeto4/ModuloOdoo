from odoo import fields, models


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "Oferta "


    price = fields.Float(string="PReço", required=True)
    status = fields.Selection(string="Oferta", selection=[('aceito', 'Aceito'), ('recusado', 'Recusado')])
    partner_id = fields.Many2one("res.partner", string="Parceira", required=True)
    property_id = fields.Many2one("estate.property", string="Preço", required=True)
