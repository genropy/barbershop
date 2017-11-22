#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('prestazione', pkey='id', name_long='!!Prestazione', name_plural='!!Prestazioni')
        self.sysFields(tbl)
        tbl.column('appuntamento_id',size='22', group='_', name_long='!!Appuntamento'
                    ).relation('appuntamento.id', relation_name='prestazioni', mode='foreignkey', onDelete='cascade')
        tbl.column('listino_id',size='22', group='_', name_long='!!Listino'
                    ).relation('listino.id', relation_name='prestazioni', mode='foreignkey', onDelete='raise')
        
        tbl.column('data', dtype='D', name_long='!!Data')
        tbl.column('durata_media',dtype='I',name_long='Durata (minuti)',name_short='Minuti',indexed=True)
        tbl.column('prezzo',dtype='money',name_long='Prezzo')

        