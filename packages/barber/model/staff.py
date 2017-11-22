# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('staff',pkey='id',name_long='Staff',
                        name_plural='Staff',caption_field='identificativo',
                        partition_negozio_id='negozio_id')
        self.sysFields(tbl)
        tbl.column('identificativo',size=':20',name_long='Identificativo',indexed=True)
        tbl.column('negozio_id',size='22',name_long='Negozio').relation('negozio.id',relation_name='lavoranti', mode='foreignkey')
        tbl.column('anagrafica_id',size='22',name_long='Anagrafica').relation('anagrafica.id',mode='foreignkey', one_one='*')
        tbl.column('user_id',size='22', group='_', name_long='!!User'
                    ).relation('adm.user.id',one_one='*', mode='foreignkey', onDelete='raise')
        tbl.column('orario', dtype='X', name_long='!!Orario') 
        self.anagraficaAliases(tbl)

    
