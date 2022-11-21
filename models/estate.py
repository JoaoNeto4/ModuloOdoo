from odoo import api, models, fields

from datetime import datetime

class RealState(models.Model):

    _name = 'estate.property'
    _description = "Test Model"
    

    name = fields.Char(string='Nome',required=True)
    description = fields.Text(string='Descrição', copy=False)
    state = fields.Selection(
        string='Status',
        selection=[('novo', 'Novo'), ('ofertaRecebida', 'Oferta Recebida'),
                    ('ofertaAceita', 'Oferta Aceita'), ('vendida', 'Vendida'), 
                    ('cancelada', 'Cancelada')],Required=True,default="novo",
        help='Escolha a vista que mais lhe agrada'
    )
    postcode = fields.Char(string='CEP')
    date_availability = fields.Date(string='Data disponibilidade', required=True, default=datetime.now())
    expected_price = fields.Float(string='Preço esperado', required=True, digits=0)
    selling_price = fields.Float(string='Preço de venda', digits=0)
    bedrooms = fields.Integer(string='Quartos', default=2)
    living_area = fields.Integer(string='Sala de estar')
    facades = fields.Integer(string='Fachadas')
    garage = fields.Boolean(string='Garagem', copy=False)
    garden  = fields.Boolean(string='Jardim', copy=False)
    garden_area = fields.Integer(string='Area de jardim')
    state = fields.Selection(
        selection=[
            ("nova", "Nova"),
            ("oferta_recebida", "Oferta Recebida"),
            ("oferta_aceita", "Oferta Aceita"),
            ("vendido", "Vendido"),
            ("cancelado", "Cancelado"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="nova",
    )
    active = fields.Boolean(string='Ativo', active=True, default=True)
    garden_orientation = fields.Selection(
        string='Orientacao do Jardin',
        selection=[('norte', 'Norte'), ('sul', 'Sul'), ('leste', 'Leste'), ('oeste', 'Oeste')],Required=True,default="norte",
        help='Escolha a vista que mais lhe agrada'
    )

    property_type_id = fields.Many2one("estate.property.type", string="Tipo de propriedade")
    user_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Comprador", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tag", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Oferta")

    total_area = fields.Integer("Total área", compute="_compute_total")
    best_price = fields.Float("Melhor oferta", compute="_compute_best_price")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for prop in self:
            prop.total_area = living_area + garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "norte"
        else:
            self.garden_area = 0
            self.garden_orientation = False
            '''
            return {'warning': {
                'title': _("Warning"),
                'message': ('Este return é opcional, apenas testando!!')}}
            '''