from odoo import models, fields
from odoo.fields import One2many


class Owner(models.Model):
    _name = 'owner'

    name= fields.Char(required=True)
    phone = fields.Char(required=True)
    address = fields.Char()

    property_ids = fields.One2many('property','owner_id')