# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('listino',pkey='id',name_long='Listino',
                        name_plural='Listino',
                        caption_field='nome',
                        partition_negozio_id='negozio_id')
        self.sysFields(tbl)
        tbl.column('negozio_id',size='22', group='_', name_long='!![it]Negozio'
                    ).relation('negozio.id', relation_name='listino', mode='foreignkey', onDelete='raise')
        tbl.column('nome',size=':30',name_long='Nome',indexed=True)
        tbl.column('descrizione',name_long='Descrizione')
        tbl.column('durata_media',dtype='I',name_long='Durata media (minuti)',name_short='Minuti',indexed=True,validate_notnull=True)
        tbl.column('prezzo',dtype='money',name_long='Prezzo',validate_notnull=True)
