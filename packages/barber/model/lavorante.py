# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('lavorante',pkey='id',name_long='Lavorante',
                        name_plural='Lavoranti',caption_field='identificativo',
                        partition_negozio_id='negozio_id')
        self.sysFields(tbl)
        tbl.column('identificativo',size=':20',name_long='Identificativo',indexed=True)
        tbl.column('negozio_id',size='22',name_long='Negozio').relation('negozio.id',relation_name='lavoranti', mode='foreignkey')
        tbl.column('anagrafica_id',size='22',name_long='Anagrafica').relation('anagrafica.id',mode='foreignkey', one_one='*')
        self.anagraficaAliases(tbl)