from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "Descrição tipo propriedade"


    name = fields.Char(string="Nome", required=True)
    