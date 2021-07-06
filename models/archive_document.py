from odoo import models, fields, api, _
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import get_lang


class ArchiveBranch(models.Model):
    _name = 'archive.branch'
    _description = "Archive Branch"

    name = fields.Char(string='Branch Name', required=True, translate=True)
    color = fields.Integer(string='Color')

    _sql_constraints = {
        ('arc_branch_name_uk',
         'unique (name)',
         'The Branch Name should be unique')}


class ArchiveTag(models.Model):
    _name = 'archive.tag'
    _description = "Archive Tag"

    name = fields.Char(string='Tag Name', required=True, translate=True)
    color = fields.Integer(string='Color')

    _sql_constraints = {
        ('arc_tag_name_uk',
         'unique (name)',
         'The Tag Name should be unique')}


class ArchiveCategory(models.Model):
    _name = 'archive.category'
    _description = "Archive Category"

    name = fields.Char(string='Category Name', required=True, translate=True)
    color = fields.Integer(string='Color')

    _sql_constraints = {
        ('arc_cat_name_uk',
         'unique (name)',
         'The Category Name should be unique')}


class SecurityLevel(models.Model):
    _name = 'security.level'
    _description = "Security Level"

    name = fields.Char(string='Security Level', required=True, translate=True)
    color = fields.Integer(string='Color')

    _sql_constraints = {
        ('sec_level_name_uk',
         'unique (name)',
         'The Security Level Name should be unique')}


class ArchiveDocument(models.Model):
    _name = 'archive.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Archive Document"
    # _rec_name = "arc_name"

    arc_code = fields.Char(string="Arc Code", required=True,
                           index=True, copy=False, readonly=True, default=_('New'))

    doc_no = fields.Char(string='Doc No.', index=True, required=True)
    doc_date = fields.Date('Doc Date', default=fields.Date.today(), required=True)
    doc_name = fields.Char(string='Doc Name', required=True, tracking=True)
    ref_no = fields.Char(string='Ref No.')
    ref_date = fields.Date(string='Ref Date')

    branch_id = fields.Many2one('archive.branch', string='Branch')
    cat_id = fields.Many2one('archive.category', string='Category')
    tag_id = fields.Many2many('archive.tag', string='Tag')
    sec_id = fields.Many2one(
        'security.level', string="Security Level", default=1)

    doc_file = fields.Binary(string="Documents", attachment=True)
    doc_file_name = fields.Char(string="File Name", tracking=True)
    # doc_description = fields.Html(string="Description")
    doc_description = fields.Char(string="Description", tracking=True)
    color = fields.Integer()
    doc_cnt = fields.Integer(default=1)
    tag_cnt = fields.Integer(string="Tag count", store=True, compute='_get_tag_count')
    attachment_ids = fields.One2many('archive.document.attachment', 'doc_id', string="Attchments", copy=True, auto_join=True)

    @api.depends('tag_id')
    def _get_tag_count(self):
        for r in self:
            r.tag_cnt = len(r.tag_id)

    # Constraint to accept only pdf file
    # @api.constrains('doc_file')
    # def _check_file(self):
    #     if str(self.doc_file_name.split(".")[1]) != 'pdf':
    #         raise ValidationError("Cannot upload file different from .pdf file")

    @api.model
    def create(self, vals):
        if vals.get('arc_code', _('New')) == _('New'):
            doc_date = vals.get('doc_date')
            vals['arc_code'] = self.env['ir.sequence'].next_by_code(
                'archive.document', sequence_date=doc_date)
        return super(ArchiveDocument, self).create(vals)

    _sql_constraints = {
        ('arc_code_uk',
         'unique (arc_code)',
         'The arc_code should be unique')}

    _sql_constraints = {
        ('doc_no_uk',
         'unique (doc_no)',
         'The doc_no should be unique')}

class ArchiveDocumentAttachment(models.Model):
    _name = "archive.document.attachment"
    _description = "Archive Document Attachment"

    doc_id = fields.Many2one('archive.document', string='Doc id', ondelete='cascade', required=True, index=True, copy=False)
    attachment_file = fields.Binary(string="Attachment", attachment=True)
    attachment_name = fields.Char(string="Name" , tracking=True)
    attachment_description = fields.Char(string="Description")


class ResUsers(models.Model):
    _inherit = 'res.users'

    branch_ids = fields.Many2many('archive.branch', string="Branches")
    cat_ids = fields.Many2many('archive.category', string="Categories")
    tag_ids = fields.Many2many('archive.tag', string="Tags")
    sec_ids = fields.Many2many('security.level', string="Security Level")
