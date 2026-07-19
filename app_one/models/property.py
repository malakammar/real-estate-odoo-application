from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    maloka = fields.Char()
    name = fields.Char(required=1, default='Name', size=8, tracking=1)
    description = fields.Text()
    post_code = fields.Char(required=True, tracking=True)
    data_availability = fields.Date()
    accepted_price = fields.Float()
    selling_price = fields.Float(tracking=1)
    diff = fields.Float(compute='_compute_diff', store=True ,readonly=0)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    garden_orientation = fields.Selection([
    #('Stored in DataBase(Small letters)', 'Showed for the user (first letter upper case')
    #selection is a dropdown list
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West'),
    ])
    ref = fields.Char(readonly=True, default='New')

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')

    owner_address = fields.Char(related='owner_id.address' ,readonly=0 , store=1)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0, store=1)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default ='draft')

    _sql_constraints = \
        [
            ('unique_name', 'unique("name")', 'This name is exist please enter unique name'),
        ]
    line_ids = fields.One2many('property.line','property_id')
    active = fields.Boolean(default=True)

    @api.depends('accepted_price','selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print('inside _compute_diff')
            rec.diff = rec.accepted_price- rec.selling_price

    @api.constrains('bedrooms')
    def _check_room_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError("Number of bedrooms must be greater than 0")


    def action_draft(self):
        for rec in self:
            print("action draft function")
            rec.state ='draft'

    def action_pending(self):
        for rec in self:
            print("action pending function")
            rec.write({'state':'pending'})

    def action_sold(self):
        for rec in self:
            print("Action sold function")
            rec.state='sold'

    def action_close(self):
        for rec in self:
            rec.state ='closed'

    def check_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True


    def action(self):
        print(self.env['owner'].create({
            'name': 'name_one',
            "phone" : '09876',
        }))
        print(self.env['property'].search([('name', '=' , 'prop1')]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
            print("sequence func")
        return res

'''
    @api.model_create_multi
    def create(self, vals_list):
        res= super(Property, self).create(vals_list)
        print("inside create method")
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property,self)._search(domain, offset, limit, order, access_rights_uid)
        print("inside search")
        return res

    def write(self, vals):
        res = super(Property,self).write(vals)
        print("inside WRITE")
        return res

    def unlink(self):
        res = super(Property,self).unlink()
        print("inside unlink")
        return res
'''

class property_line(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Integer()
    description = fields.Char()


