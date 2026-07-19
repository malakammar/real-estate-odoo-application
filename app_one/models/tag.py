from odoo import models, fields
from odoo.fields import One2many


class Tag(models.Model):
    _name = 'tag'

    name= fields.Char(required=True)

