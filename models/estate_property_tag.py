from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = 'estate.property.tag'
    _description = "Característica da propriedade"


    name = fields.Char(string="Nome", required=True)

   