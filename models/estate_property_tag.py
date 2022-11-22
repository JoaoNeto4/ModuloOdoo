from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = 'estate.property.tag'
    _description = "Característica da propriedade"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(string="Nome", required=True)

   