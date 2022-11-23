from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "Oferta "
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Price must be greater than zero"),
    ]


    price = fields.Float(string="Preço", required=True)
    status = fields.Selection(string="Status", selection=[('aceito', 'Aceito'), ('recusado', 'Recusado')])
    partner_id = fields.Many2one("res.partner", string="Parceiro", required=True)
    property_id = fields.Many2one("estate.property", string="Preço", required=True)
    validity = fields.Integer(string="Validade", default=7)
    date_deadline = fields.Date(string='Data validade', compute="_compute_date_deadline", inverse="_compute_date_deadline")
    description = fields.Char(string="Descrição", compute="_compute_description")
    state = fields.Selection(
        selection=[
            ("aceito", "Aceito"),
            ("recusado", "Rescusado"),
        ],
        string="Status",
        copy=False,
        default=False,
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )

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

    def action_accept_offer(self):
        if "aceito" in self.mapped("property_id.offer_ids.state"):
            raise UserError("A ofeta ja foi aceita.")
        self.write(
            {
                "state": "aceito",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "oferta_aceita",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )
    
    def action_reject(self):
        return self.write(
            {
                "state": "recusado",
            }
        )