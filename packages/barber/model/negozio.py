# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('negozio',pkey='id',name_long='Negozio',
                        name_plural='Negozi',
                        caption_field='identificativo',
                        partition_aderente_id='aderente_id')
        self.sysFields(tbl)
        tbl.column('identificativo',size=':20',name_long='Identificativo',indexed=True)
        tbl.column('codice_negozio',size=':10',name_long='Codice negozio',indexed=True)
        tbl.column('anagrafica_id',size='22',name_long='Anagrafica').relation('anagrafica.id',mode='foreignkey', one_one='*')
        tbl.column('aderente_id',size='22',name_long='Aderente').relation('aderente.id',relation_name='negozi', mode='foreignkey')
        self.anagraficaAliases(tbl)