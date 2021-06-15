from odoo import models, fields, api, _
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import get_lang


# class ArchiveDept(models.Model):
#     _name = 'archive.dept'
#     _description = "Archive Departments"
#
#     name = fields.Char(string='Dept Name', required=True, Translate=True)
#
#     _sql_constraints = {
#         ('arc_dept_name_uk',
#          'unique (name)',
#          'The Dept Name should be unique')}


class ArchiveTag(models.Model):
    _name = 'archive.tag'
    _description = "Archive Tag"

    name = fields.Char(string='Tag Name', required=True, Translate=True)
    color = fields.Integer()

    _sql_constraints = {
        ('arc_tag_name_uk',
         'unique (name)',
         'The Tag Name should be unique')}


class ArchiveCategory(models.Model):
    _name = 'archive.category'
    _description = "Archive Category"

    name = fields.Char(string='Category Name', required=True, Translate=True)

    _sql_constraints = {
        ('arc_cat_name_uk',
         'unique (name)',
         'The Category Name should be unique')}


class ArchiveDocument(models.Model):
    _name = 'archive.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Archive Document"
    # _rec_name = "arc_name"

    arc_code = fields.Char(string="Arc Code", required=True, index=True, copy=False, readonly=True, default=_('New'))

    doc_no = fields.Char(string='Doc No.', required=True, Translate=True)
    doc_date = fields.Date('Doc Date', required=True, default=fields.Date.today())
    doc_name = fields.Char(string='Doc Name', required=True, Translate=True)
    ref_no = fields.Char(string='Ref No.', Translate=True)
    ref_date = fields.Date(string='Ref Date')

    # dept_id = fields.Many2one('archive.dept', string='Dept', Translate=True)
    tag_id = fields.Many2many('archive.tag', string='Tag', Translate=True)
    cat_id = fields.Many2one('archive.category', string='Category', Translate=True)

    is_secret = fields.Boolean(string="Is Secret")
    doc_file = fields.Binary(string="Documents")
    doc_file_name = fields.Char(string="File Name")
    doc_description = fields.Html(string="Description")
    color = fields.Integer()

    # Constraint to accept only pdf file
    # @api.constrains('doc_file')
    # def _check_file(self):
    #     if str(self.doc_file_name.split(".")[1]) != 'pdf':
    #         raise ValidationError("Cannot upload file different from .pdf file")

    @api.model
    def create(self, vals):
        if vals.get('arc_code', _('New')) == _('New'):
            doc_date = vals.get('doc_date')
            vals['arc_code'] = self.env['ir.sequence'].next_by_code('archive.document', sequence_date=doc_date)
        return super(ArchiveDocument, self).create(vals)

    _sql_constraints = {
        ('arc_code_uk',
         'unique (arc_code)',
         'The arc_code should be unique')}


class ResUsers(models.Model):
    _inherit = 'res.users'

    cat_ids = fields.Many2many('archive.category', string="Allowed Categories")
    tag_ids = fields.Many2many('archive.tag', string="Allowed Tags")
