# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('aderente',pkey='id',name_long='Aderente',name_plural='Aderenti',caption_field='codice_aderente')
        self.sysFields(tbl)
        tbl.column('codice_aderente',size=':10',name_long='Codice aderente',unique=True,indexed=True)
        tbl.column('identificativo',size=':20',name_long='Identificativo',indexed=True,unique=True)
        tbl.column('anagrafica_id',size='22',name_long='Anagrafica').relation('anagrafica.id',mode='foreignkey', one_one='*')
        self.anagraficaAliases(tbl)