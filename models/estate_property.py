from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


from datetime import datetime
from dateutil.relativedelta import relativedelta



class RealState(models.Model):

    _name = 'estate.property'
    _description = "Test Model"
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Price must be greater than zero"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive"),
    ]
    

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
    '''date_availability = fields.Date(string='Data disponibilidade', required=True, default=datetime.now())'''
    date_availability = fields.Date(string='Data disponibilidade', default=lambda self: self._default_date_availability(), copy=False)
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
    user_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user.id)
    buyer_id = fields.Many2one("res.partner", string="Comprador", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tag", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Oferta")

    total_area = fields.Integer("Total área", compute="_compute_total")
    best_price = fields.Float("Melhor oferta", compute="_compute_best_price")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

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

    def action_cancel_state(self):
        if "vendido" in self.mapped("state"):
            raise UserError("Propriedades canceladas não podem ser vendidas.")
        return self.write({"state": "cancelado"})

    def action_sale_state(self):
        if "canceledo" in self.mapped("state"):
            raise UserError("Propriedades canceladas não podem ser vendidas.")
        return self.write({"state": "vendido"})

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)