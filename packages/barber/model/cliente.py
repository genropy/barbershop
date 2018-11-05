# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('cliente',pkey='id',name_long='Cliente',
                        name_plural='Cliente',caption_field='ragione_sociale',
                        partition_negozio_id='negozio_id')
        self.sysFields(tbl)
        tbl.column('negozio_id',size='22',name_long='Negozio').relation('negozio.id',relation_name='clienti', mode='foreignkey')
        tbl.column('anagrafica_id',size='22',name_long='Anagrafica').relation('anagrafica.id',mode='foreignkey', one_one='*')
        tbl.column('user_id',size='22', group='_', name_long='!![it]User'
                    ).relation('adm.user.id',one_one='*', mode='foreignkey', onDelete='raise') 
        self.anagraficaAliases(tbl)

    def creaCliente(self,cognome=None,telefono=None,nome=None,email=None):
        anagrafica = dict(cognome=cognome,nome=nome,telefono=telefono,email=email,ragione_sociale='%s %s' %(cognome,nome) if cognome and nome else cognome)
        self.db.table('barber.anagrafica').insert(anagrafica)
        cliente = self.newrecord(anagrafica_id=anagrafica['id'],negozio_id=self.db.currentEnv['current_negozio_id'])
        self.insert(cliente)
        self.db.commit()
        return cliente