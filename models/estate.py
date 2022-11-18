from odoo import models, fields

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
    active = fields.Boolean(string='Ativo', active=True, default=True)
    garden_orientation = fields.Selection(
        string='Orientacao do Jardin',
        selection=[('norte', 'Norte'), ('sul', 'Sul'), ('leste', 'Leste'), ('oeste', 'Oeste')],Required=True,default="norte",
        help='Escolha a vista que mais lhe agrada'
    )