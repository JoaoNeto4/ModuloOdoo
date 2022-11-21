from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "Oferta "


    price = fields.Float(string="Preço", required=True)
    status = fields.Selection(string="Oferta", selection=[('aceito', 'Aceito'), ('recusado', 'Recusado')])
    partner_id = fields.Many2one("res.partner", string="Parceira", required=True)
    property_id = fields.Many2one("estate.property", string="Preço", required=True)
    validity = fields.Integer(string="Validade", default=7)
    date_deadline = fields.Date(string='Data validade', compute="_compute_date_deadline", inverse="_compute_date_deadline")
    description = fields.Char(compute="_compute_description", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.depends("partner_id.name")
    def _compute_description(self):
        for record in self:
            record.description = "Parceiro %s" % record.partner_id.name
