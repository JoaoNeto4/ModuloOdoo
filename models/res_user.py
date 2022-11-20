from odoo import fields, models


class ResUsers(models.Model):

    _name = 'res.users'
    _description = "Model user"

    property_ids = fields.One2many(
        "estate.property", "user_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])]
    )