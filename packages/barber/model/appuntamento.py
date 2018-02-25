# encoding: utf-8
from gnr.core.gnrdecorator import metadata
from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('appuntamento', pkey='id', name_long='!!Appuntamento', name_plural='!!Appuntamenti',
                        caption_field='caption_appuntamento',broadcast='data')
        self.sysFields(tbl)
        tbl.column('calendario_id',size='22', group='_', name_long='!!Calendario'
                    ).relation('calendario.id', relation_name='appuntamenti', mode='foreignkey', onDelete='raise')
        tbl.column('cliente_id',size='22', group='_', name_long='!!Cliente'
                    ).relation('cliente.id', relation_name='appuntamenti', mode='foreignkey', onDelete='raise') 
        tbl.column('tipo_appuntamento',size=':10', group='_', name_long='!!Tipo appuntamento'
                    ).relation('appuntamento_tipo.codice', mode='foreignkey', onDelete='raise')  
        tbl.column('data', dtype='D', name_long='!!Data')
        tbl.column('ora_inizio', dtype='H', name_long='!!Ora inizio')
        tbl.column('ora_fine', dtype='H', name_long='!!Ora fine')
        tbl.column('durata', dtype='L', name_long='!!Durata')
        tbl.column('indisponibile', dtype='B', name_long='!!Indisponibile')
        tbl.column('cognome', size=':50', name_long='!!Cognome')
        tbl.column('nome', size=':50', name_long='!!Nome')
        tbl.column('telefono', size=':50', name_long='!!Telefono')
        tbl.column('email', size=':50', name_long='!!Email')
        tbl.column('listini_pkeys', name_long='!!Prestazioni')
        tbl.aliasColumn('colore','@tipo_appuntamento.colore')
        tbl.formulaColumn('prestazioni_prenotate',"array_to_string(ARRAY(#list_desc),';')",
                            select_list_desc=dict(table='barber.listino',columns='$nome',
                            where="$id = ANY(string_to_array(#THIS.listini_pkeys,','))",order_by='$nome'))

    def trigger_onInserting(self,record=None):
        if (record['cognome'] and record['telefono']) and not record['cliente_id']:
            clitable = self.db.table('barber.cliente')
            cliente = clitable.query(where='$cognome=:cogn AND $telefono=:tel',cogn=record['cognome'],
                                    tel=record['telefono']).fetch()
            if not cliente:
                cliente = clitable.creaCliente(cognome=record['cognome'],
                                    telefono=record['telefono'],
                                    nome=record['nome'],email=record['email'])
            else:
                cliente = cliente[0]
            record['cliente_id'] = cliente['id']
        calendario_id = record['calendario_id']
        self.db.deferToCommit(self.db.table('barber.calendario').aggiornaSlots, calendario_id=calendario_id,
                              _deferredId=calendario_id)

    def trigger_onUpdated(self,record=None, old_record=None):
        calendario_id = record['calendario_id']
        self.db.deferToCommit(self.db.table('barber.calendario').aggiornaSlots, calendario_id=calendario_id,
                              _deferredId=calendario_id)

    def trigger_onDeleted(self,record=None, old_record=None):
        calendario_id = record['calendario_id']
        self.db.deferToCommit(self.db.table('barber.calendario').aggiornaSlots, calendario_id=calendario_id,
                              _deferredId=calendario_id)

