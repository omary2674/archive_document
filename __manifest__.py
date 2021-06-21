{
    'name': "Archive Document",
    'version': '14.0.01',
    'depends': ['base','mail'],
    'author': "Mohammad Omari",
    'website': "adawliah.com",
    'category': 'Accounting/Accounting',
    'description': """
        Archive Document
    """,
    # data files always loaded at installation
    'data': [
        'security/res_groups.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
        'views/archive_document.xml',
        'data/ir_sequence.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': ['demo/archive_demo.xml'],
    'images': ['static/images/documents.png'],
    'installable': True,
    'application': True,
    'auto_install': False,

}
