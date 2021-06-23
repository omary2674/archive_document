from odoo import models, fields, api
from odoo import tools


class ArchiveTagAnalysis(models.Model):
    _name = 'archive.tag.analysis'
    _auto = False
    _description = 'Archive Tag Analysis'
    
    name = fields.Char('Name')
    tag_cnt = fields.Integer('Tag')
    

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'archive_tag_analysis')
        self.env.cr.execute("""
                                CREATE OR REPLACE VIEW archive_tag_analysis AS 
                                        select 
                                               row_number() OVER () AS id,
                                               t.name , 
                                               count(*) as tag_cnt 
                                        from archive_document_archive_tag_rel r , archive_document a , archive_tag t 
                                        where r.archive_document_id = a.id
                                        and t.id = r.archive_tag_id
                                        group by t.name
                            """)
