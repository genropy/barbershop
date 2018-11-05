#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('appuntamento_tipo', pkey='codice', 
                    name_long='!![it]Tipo appuntamento', 
                    name_plural='!![it]Tipi appuntamento',
                    caption_field='descrizione')
        self.sysFields(tbl,pkey='codice')
        tbl.column('codice', size=':10', name_long='!![it]Codice')
        tbl.column('descrizione', size=':20', name_long='!![it]Descrizione')
        tbl.column('colore', size=':100', name_long='!![it]Colore')
        tbl.column('indisponibile', dtype='B', name_long='!![it]Indisponibile')

    