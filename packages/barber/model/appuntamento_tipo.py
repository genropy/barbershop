#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('appuntamento_tipo', pkey='codice', 
                    name_long='!!Tipo appuntamento', 
                    name_plural='!!Tipi appuntamento',
                    caption_field='descrizione')
        self.sysFields(tbl,pkey='codice')
        tbl.column('codice', size=':10', name_long='!!Codice')
        tbl.column('descrizione', size=':20', name_long='!!Descrizione')
        tbl.column('colore', size=':100', name_long='!!Colore')
        tbl.column('indisponibile', dtype='B', name_long='!!Indisponibile')

    